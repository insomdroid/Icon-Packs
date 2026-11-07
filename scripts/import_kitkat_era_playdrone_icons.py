#!/usr/bin/env python3
"""Extract unchanged launcher icons from APKs in the Playdrone 2014 Google Play snapshot."""
from __future__ import annotations
import concurrent.futures, csv, hashlib, html, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.request, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESOURCE_DIR=ROOT/"pack-kitkat/src/main/res/drawable-nodpi"
APPFILTER=ROOT/"pack-kitkat/src/main/res/xml/appfilter.xml"
DRAWABLES=ROOT/"pack-kitkat/src/main/res/xml/drawable.xml"
ASSET_DIR=ROOT/"pack-kitkat/src/main/assets"
INVENTORY=ASSET_DIR/"kitkat-era-playdrone-icons.csv"
SNAPSHOT_URL="https://archive.org/download/playdrone-snapshots/2014-10-31.json"
MIN_ICONS=int(os.environ.get("KITKAT_MIN_ARCHIVE_ICONS","500"))
MAX_CANDIDATES=int(os.environ.get("KITKAT_MAX_ARCHIVE_CANDIDATES","6000"))
WORKERS=int(os.environ.get("KITKAT_DOWNLOAD_WORKERS","12"))
MAX_APK=100*1024*1024
BEGIN="<!-- BEGIN GENERATED PLAYDRONE 2014 ICONS -->"
END="<!-- END GENERATED PLAYDRONE 2014 ICONS -->"
PNG=b"\x89PNG\r\n\x1a\n"
UA="Insomdroid-KitKat-Icon-Importer/1.0 (+https://github.com/insomdroid/Icon-Packs)"
def fetch(url,dest=None,attempts=3):
    req=urllib.request.Request(url,headers={"User-Agent":UA}); error=None
    for i in range(attempts):
        try:
            with urllib.request.urlopen(req,timeout=90) as response: data=response.read(MAX_APK+1) if dest else response.read()
            if dest:
                if len(data)>MAX_APK: raise ValueError("APK too large")
                dest.write_bytes(data)
            return data
        except (urllib.error.URLError,TimeoutError,OSError,ValueError) as exc:
            error=exc
            if i+1<attempts: time.sleep(i+1)
    print(f"WARNING download failed {url}: {error}",file=sys.stderr); return None
def main():
    print("Downloading Playdrone Google Play snapshot 2014-10-31")
    raw=fetch(SNAPSHOT_URL)
    if not raw: raise RuntimeError("Unable to download 2014 Playdrone snapshot")
    snapshot=json.loads(raw)
    if not isinstance(snapshot,list): raise RuntimeError("Unexpected snapshot format")
    print(f"Snapshot records: {len(snapshot):,}")
    queue=[]
    for app in snapshot:
        package=str(app.get("app_id") or "").strip(); url=str(app.get("apk_url") or "").strip()
        if package and url.startswith("https://archive.org/download/"):
            queue.append({"package":package,"name":str(app.get("title") or package),
                "version":str(app.get("version_string") or ""),"version_code":str(app.get("version_code") or ""),
                "downloads":int(app.get("downloads") or 0),"date":str(app.get("snapshot_date") or "2014-10-31"),"url":url})
    queue.sort(key=lambda x:x["downloads"],reverse=True); queue=queue[:MAX_CANDIDATES]
    print(f"Most popular downloadable candidates queued: {len(queue)}")
    sdk=Path(os.environ.get("ANDROID_HOME",os.environ.get("ANDROID_SDK_ROOT",""))); aapt=os.environ.get("AAPT")
    if not aapt:
        tools=sorted((sdk/"build-tools").glob("*/aapt"),reverse=True)
        if not tools: raise RuntimeError("Android build-tools aapt not found")
        aapt=str(tools[0])
    RESOURCE_DIR.mkdir(parents=True,exist_ok=True); ASSET_DIR.mkdir(parents=True,exist_ok=True)
    for pattern in ("fdroid_*.png","playdrone_*.png"):
        for old in RESOURCE_DIR.glob(pattern): old.unlink()
    unique={}; app_items=[]; drawable_items=[]; rows=[]; imported=set(); attempted=0; compatible=0
    with tempfile.TemporaryDirectory(prefix="kitkat-playdrone-") as temp:
        tmp=Path(temp)
        for offset in range(0,len(queue),WORKERS):
            if len(unique)>=MIN_ICONS: break
            batch=queue[offset:offset+WORKERS]; futures={}
            with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for app in batch:
                    attempted+=1; apk=tmp/f"{attempted}.apk"
                    futures[pool.submit(fetch,app["url"],apk)]=(app,apk)
                for future in concurrent.futures.as_completed(futures):
                    app,apk=futures[future]
                    try: data=future.result()
                    except Exception as exc:
                        print(f"WARNING {app['package']}: {exc}",file=sys.stderr); continue
                    if data is None: continue
                    try: out=subprocess.run([aapt,"dump","badging",str(apk)],check=True,capture_output=True,text=True,timeout=45).stdout
                    except (subprocess.SubprocessError,OSError): continue
                    pkg=re.search(r"^package: name='([^']+)'",out,re.M)
                    target=re.search(r"^targetSdkVersion:'(\d+)'",out,re.M)
                    activity=re.search(r"^launchable-activity: name='([^']+)'",out,re.M)
                    if not pkg or pkg.group(1)!=app["package"] or not target or int(target.group(1))>19 or not activity: continue
                    compatible+=1
                    icons=sorted([(int(d),p) for d,p in re.findall(r"^application-icon-(\d+):'([^']+)'",out,re.M)],reverse=True)
                    if not icons:
                        m=re.search(r"^application:.*?\bicon='([^']+)'",out,re.M)
                        if m: icons=[(0,m.group(1))]
                    image=None
                    try:
                        with zipfile.ZipFile(apk) as z:
                            for _,path in icons:
                                if path.endswith(".png"):
                                    try: candidate=z.read(path)
                                    except KeyError: continue
                                    if candidate.startswith(PNG): image=candidate; break
                    except (OSError,zipfile.BadZipFile): pass
                    if not image: continue
                    digest=hashlib.sha256(image).hexdigest(); resource=unique.get(digest)
                    if resource is None:
                        resource="playdrone_"+digest[:20]; unique[digest]=resource
                        (RESOURCE_DIR/f"{resource}.png").write_bytes(image)
                        drawable_items.append(f'  <item drawable="{resource}" name="{resource}" />')
                    package=pkg.group(1); act=activity.group(1)
                    if act.startswith("."): act=package+act
                    elif "." not in act: act=package+"."+act
                    label=html.escape(app["name"],quote=True)
                    app_items.append(f'  <item component="ComponentInfo{{{package}/{act}}}" drawable="{resource}" name="{label}" />')
                    imported.add(package)
                    rows.append([package,app["name"],app["version"],app["version_code"],app["downloads"],app["date"],
                        target.group(1),app["url"],hashlib.sha256(data).hexdigest(),digest,f"drawable-nodpi/{resource}.png"])
                    if len(unique)%50==0: print(f"Unique original icons: {len(unique)}; mapped apps: {len(rows)}")
                    if len(unique)>=MIN_ICONS:
                        for pending in futures:
                            if not pending.done(): pending.cancel()
                        break
    if len(unique)<MIN_ICONS:
        raise RuntimeError(f"Only {len(unique)} unique PNG icons from {compatible} compatible APKs / {attempted} downloads; need {MIN_ICONS}")
    original=APPFILTER.read_text(encoding="utf-8"); kept=[]
    for line in original.splitlines():
        match=re.search(r"ComponentInfo\{([^/}]+)/",line)
        if match and match.group(1) in imported: continue
        kept.append(line)
    app_text=re.sub(re.escape(BEGIN)+r".*?"+re.escape(END),"","\n".join(kept),flags=re.S).rstrip()
    app_text=app_text.replace("</resources>","\n"+BEGIN+"\n"+"\n".join(app_items)+"\n"+END+"\n</resources>")
    APPFILTER.write_text(app_text+"\n",encoding="utf-8")
    draw_text=DRAWABLES.read_text(encoding="utf-8")
    draw_text=re.sub(re.escape(BEGIN)+r".*?"+re.escape(END),"",draw_text,flags=re.S).rstrip()
    draw_text=draw_text.replace("</resources>","\n"+BEGIN+"\n"+"\n".join(drawable_items)+"\n"+END+"\n</resources>")
    DRAWABLES.write_text(draw_text+"\n",encoding="utf-8")
    with INVENTORY.open("w",newline="",encoding="utf-8") as stream:
        writer=csv.writer(stream)
        writer.writerow(["package_name","app_name","version_name","version_code","downloads_2014","snapshot_date","target_sdk","source_apk_url","apk_sha256","icon_sha256","resource_path"])
        writer.writerows(rows)
    print(f"SUCCESS: {len(unique)} unique original 2014 APK icons; {len(imported)} apps mapped.")
    print(f"Compatible APKs: {compatible}; downloads attempted: {attempted}; inventory: {INVENTORY}")
    return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}",file=sys.stderr); raise SystemExit(1)
