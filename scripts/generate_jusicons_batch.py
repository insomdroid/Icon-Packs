#!/usr/bin/env python3
"""JusIcons-based build-time generator using real launcher icons from APK files."""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, html, json, re, shutil, subprocess, time, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg, requests
from PIL import Image

ANDROID = "{http://schemas.android.com/apk/res/android}"
N, ANALYZE_SIZE = 192, 50
VALID_ALPHA, ALPHA_GATE, CLAMP_GRAY, CLAMP_SQ, GAIN, BUCKETS = 40, 110, 248, 61504, 210.0, 32
VISUAL_SCALE = 0.72

CATALOG = [
("Google","Gmail","com.google.android.gm"),
("Google","YouTube","com.google.android.youtube"),
("Google","Maps","com.google.android.apps.maps"),
("Google","Photos","com.google.android.apps.photos"),
("Google","Drive","com.google.android.apps.docs"),
("Google","Docs","com.google.android.apps.docs.editors.docs"),
("Google","Sheets","com.google.android.apps.docs.editors.sheets"),
("Google","Slides","com.google.android.apps.docs.editors.slides"),
("Google","Calendar","com.google.android.calendar"),
("Google","Contacts","com.google.android.contacts"),
("Google","Phone","com.google.android.dialer"),
("Google","Messages","com.google.android.apps.messaging"),
("Google","Meet","com.google.android.apps.meetings"),
("Google","Translate","com.google.android.apps.translate"),
("Google","Keep","com.google.android.keep"),
("Google","Authenticator","com.google.android.apps.authenticator2"),
("Google","Wallet","com.google.android.apps.walletnfcrel"),
("Google","Home","com.google.android.apps.chromecast.app"),
("Google","Files","com.google.android.apps.nbu.files"),
("Google","Google TV","com.google.android.videos"),
("Google","Google One","com.google.android.apps.subscriptions.red"),
("Google","News","com.google.android.apps.magazines"),
("Google","Fit","com.google.android.apps.fitness"),
("Google","Calculator","com.google.android.calculator"),
("Google","Camera","com.google.android.GoogleCamera"),
("Google","Recorder","com.google.android.apps.recorder"),
("Google","Lens","com.google.ar.lens"),
("Google","Chat","com.google.android.apps.dynamite"),
("Google","Voice","com.google.android.apps.googlevoice"),
("Google","Family Link","com.google.android.apps.kids.familylink"),
("Google","Classroom","com.google.android.apps.classroom"),
("Google","Earth","com.google.earth"),
("Google","Street View","com.google.android.street"),
("Google","Play Books","com.google.android.apps.books"),
("Google","Play Games","com.google.android.play.games"),
("Google","Google Fi","com.google.android.apps.tycho"),
("Google","Gboard","com.google.android.inputmethod.latin"),
("Google","Android Auto","com.google.android.projection.gearhead"),
("Google","Wear OS","com.google.android.apps.wear.companion"),
("Google","Find My Device","com.google.android.apps.adm"),
("Google","Tasks","com.google.android.apps.tasks"),
("Google","Gemini","com.google.android.apps.bard"),
("Google","Play Store","com.android.vending"),
("Google","Voice Access","com.google.android.apps.accessibility.voiceaccess"),
("Google","Wallpapers","com.google.android.apps.wallpaper"),
("Google","Google","com.google.android.googlequicksearchbox"),
("Google","YouTube Music","com.google.android.apps.youtube.music"),
("Google","Clock","com.google.android.deskclock"),
("Google","Chrome","com.android.chrome"),
("Google","Digital Wellbeing","com.google.android.apps.wellbeing"),
("Popular","WhatsApp","com.whatsapp"),
("Popular","WhatsApp Business","com.whatsapp.w4b"),
("Popular","Instagram","com.instagram.android"),
("Popular","Facebook","com.facebook.katana"),
("Popular","Messenger","com.facebook.orca"),
("Popular","Telegram","org.telegram.messenger"),
("Popular","Signal","org.thoughtcrime.securesms"),
("Popular","Discord","com.discord"),
("Popular","X","com.twitter.android"),
("Popular","TikTok","com.zhiliaoapp.musically"),
("Popular","Snapchat","com.snapchat.android"),
("Popular","Pinterest","com.pinterest"),
("Popular","Reddit","com.reddit.frontpage"),
("Popular","Spotify","com.spotify.music"),
("Popular","Netflix","com.netflix.mediaclient"),
("Popular","Prime Video","com.amazon.avod.thirdpartyclient"),
("Popular","Disney+","com.disney.disneyplus"),
("Popular","Max","com.hbo.hbonow"),
("Popular","Crunchyroll","com.crunchyroll.crunchyroid"),
("Popular","Twitch","tv.twitch.android.app"),
("Popular","Amazon Shopping","com.amazon.mShop.android.shopping"),
("Popular","Shopee","com.shopee.id"),
("Popular","Lazada","com.lazada.android"),
("Popular","AliExpress","com.alibaba.aliexpresshd"),
("Popular","eBay","com.ebay.mobile"),
("Popular","PayPal","com.paypal.android.p2pmobile"),
("Popular","Outlook","com.microsoft.office.outlook"),
("Popular","Microsoft Teams","com.microsoft.teams"),
("Popular","OneDrive","com.microsoft.skydrive"),
("Popular","Word","com.microsoft.office.word"),
("Popular","Excel","com.microsoft.office.excel"),
("Popular","PowerPoint","com.microsoft.office.powerpoint"),
("Popular","LinkedIn","com.linkedin.android"),
("Popular","Microsoft Edge","com.microsoft.emmx"),
("Popular","Firefox","org.mozilla.firefox"),
("Popular","Brave","com.brave.browser"),
("Popular","Opera","com.opera.browser"),
("Popular","Zoom","us.zoom.videomeetings"),
("Popular","Slack","com.Slack"),
("Popular","Dropbox","com.dropbox.android"),
("Popular","Notion","notion.id"),
("Popular","Canva","com.canva.editor"),
("Popular","CapCut","com.lemon.lvoverseas"),
("Popular","Picsart","com.picsart.studio"),
("Popular","Lightroom","com.adobe.lrmobile"),
("Popular","Acrobat","com.adobe.reader"),
("Popular","Duolingo","com.duolingo"),
("Popular","ChatGPT","com.openai.chatgpt"),
("Popular","Claude","com.anthropic.claude"),
("Popular","Perplexity","com.perplexity.ai"),
]

def lname(tag): return tag.rsplit("}", 1)[-1]

def color_value(value):
    if not value or not value.startswith("#"): return "#FFFFFF", 1.0
    raw = value[1:]
    if len(raw) == 8: alpha, rgb = int(raw[:2],16)/255.0, raw[2:]
    elif len(raw) == 6: alpha, rgb = 1.0, raw
    elif len(raw) == 4: alpha, rgb = int(raw[0]*2,16)/255.0, "".join(c*2 for c in raw[1:])
    elif len(raw) == 3: alpha, rgb = 1.0, "".join(c*2 for c in raw)
    else: return "#FFFFFF", 1.0
    return "#" + rgb, alpha

def vector_to_image(path):
    try:
        root = ET.parse(path).getroot()
        if lname(root.tag) != "vector": return None
        vw = float(root.attrib.get(ANDROID+"viewportWidth", "0"))
        vh = float(root.attrib.get(ANDROID+"viewportHeight", "0"))
        if vw <= 0 or vh <= 0: return None
        def render(node):
            tag = lname(node.tag)
            if tag == "group":
                rot=float(node.attrib.get(ANDROID+"rotation","0")); px=float(node.attrib.get(ANDROID+"pivotX","0")); py=float(node.attrib.get(ANDROID+"pivotY","0"))
                sx=float(node.attrib.get(ANDROID+"scaleX","1")); sy=float(node.attrib.get(ANDROID+"scaleY","1"))
                tx=float(node.attrib.get(ANDROID+"translateX","0")); ty=float(node.attrib.get(ANDROID+"translateY","0"))
                transform=f"translate({tx} {ty}) translate({px} {py}) rotate({rot}) scale({sx} {sy}) translate({-px} {-py})"
                return f'<g transform="{transform}">'+"".join(render(c) for c in node)+"</g>"
            if tag == "path":
                d=node.attrib.get(ANDROID+"pathData","")
                if not d: return ""
                fill, fa=color_value(node.attrib.get(ANDROID+"fillColor"))
                falpha=float(node.attrib.get(ANDROID+"fillAlpha","1"))*fa
                attrs=f' d="{html.escape(d,quote=True)}" fill="{fill}" fill-opacity="{falpha}"'
                if node.attrib.get(ANDROID+"fillType")=="evenOdd": attrs+=' fill-rule="evenodd"'
                stroke_raw=node.attrib.get(ANDROID+"strokeColor")
                if stroke_raw:
                    stroke, sa=color_value(stroke_raw)
                    attrs+=f' stroke="{stroke}" stroke-opacity="{float(node.attrib.get(ANDROID+"strokeAlpha","1"))*sa}" stroke-width="{node.attrib.get(ANDROID+"strokeWidth","1")}"'
                    if node.attrib.get(ANDROID+"strokeLineCap"): attrs+=f' stroke-linecap="{node.attrib[ANDROID+"strokeLineCap"]}"'
                    if node.attrib.get(ANDROID+"strokeLineJoin"): attrs+=f' stroke-linejoin="{node.attrib[ANDROID+"strokeLineJoin"]}"'
                return "<path"+attrs+"/>"
            return "".join(render(c) for c in node)
        body="".join(render(c) for c in root)
        alpha=float(root.attrib.get(ANDROID+"alpha","1"))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{N}" height="{N}" viewBox="0 0 {vw} {vh}"><g opacity="{alpha}">{body}</g></svg>'
        import io
        data=cairosvg.svg2png(bytestring=svg.encode(),output_width=N,output_height=N)
        return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        return None

def public_resource_map(decoded):
    result={}
    for file in (decoded/"res"/"values").glob("public.xml"):
        try:
            for item in ET.parse(file).getroot():
                rid,typ,name=item.attrib.get("id"),item.attrib.get("type"),item.attrib.get("name")
                if rid and typ and name: result[rid.lower()]=f"@{typ}/{name}"
        except Exception: pass
    return result

def find_resource(decoded, ref, public_map):
    if not ref: return None
    ref=public_map.get(ref.strip(),ref.strip())
    match=re.fullmatch(r"@(?:[A-Za-z0-9_.]+:)?([A-Za-z0-9_]+)/([A-Za-z0-9_.]+)",ref)
    if not match: return None
    name=match.group(2); candidates=[]
    for path in (decoded/"res").glob("**/"+name+".*"):
        if path.suffix.lower() not in {".xml",".png",".webp",".jpg",".jpeg"}: continue
        parent=str(path.parent).lower()
        if "anydpi-v26" in parent: rank=0 if path.suffix==".xml" else 4
        elif "anydpi" in parent: rank=1 if path.suffix==".xml" else 5
        elif "xxxhdpi" in parent: rank=2
        elif "xxhdpi" in parent: rank=3
        elif "xhdpi" in parent: rank=4
        elif "hdpi" in parent: rank=5
        elif "mdpi" in parent: rank=6
        else: rank=7 if path.suffix==".xml" else 8
        candidates.append((rank,path))
    return sorted(candidates,key=lambda x:(x[0],str(x[1])))[0][1] if candidates else None

def image_for_resource(decoded, ref, public_map, adaptive=False, depth=0):
    if depth>8: return None,adaptive
    path=find_resource(decoded,ref,public_map)
    if path is None: return None,adaptive
    if path.suffix.lower() in {".png",".webp",".jpg",".jpeg"}:
        try: return Image.open(path).convert("RGBA"),adaptive
        except Exception: return None,adaptive
    try: root=ET.parse(path).getroot()
    except Exception: return None,adaptive
    kind=lname(root.tag)
    if kind=="adaptive-icon":
        fg=next((c for c in root if lname(c.tag)=="foreground"),None)
        fg_ref=fg.attrib.get(ANDROID+"drawable") if fg is not None else None
        return image_for_resource(decoded,fg_ref,public_map,True,depth+1) if fg_ref else (None,True)
    if kind=="vector": return vector_to_image(path),adaptive
    if kind in {"bitmap","inset"}:
        child_ref=root.attrib.get(ANDROID+"src") or root.attrib.get(ANDROID+"drawable")
        if not child_ref:
            child=next(iter(root),None); child_ref=child.attrib.get(ANDROID+"drawable") if child is not None else None
        return image_for_resource(decoded,child_ref,public_map,adaptive,depth+1) if child_ref else (None,adaptive)
    if kind=="layer-list":
        for item in reversed([c for c in root if lname(c.tag)=="item"]):
            child_ref=item.attrib.get(ANDROID+"drawable")
            if child_ref:
                image,is_adaptive=image_for_resource(decoded,child_ref,public_map,adaptive,depth+1)
                if image is not None: return image,is_adaptive
    return None,adaptive

def find_launcher_components(manifest, package):
    found=[]
    for activity in list(manifest.findall("activity"))+list(manifest.findall("activity-alias")):
        for intent in activity.findall("intent-filter"):
            actions={x.attrib.get(ANDROID+"name") for x in intent.findall("action")}
            categories={x.attrib.get(ANDROID+"name") for x in intent.findall("category")}
            if "android.intent.action.MAIN" not in actions or "android.intent.category.LAUNCHER" not in categories: continue
            name=activity.attrib.get(ANDROID+"name","")
            if not name: continue
            if name.startswith("."): name=package+name
            elif "." not in name: name=package+"."+name
            found.append(f"ComponentInfo{{{package}/{name}}}")
            break
    return sorted(set(found))

def normalize(source, adaptive):
    source=source.convert("RGBA")
    if adaptive: return source.resize((N,N),Image.Resampling.LANCZOS)
    source.thumbnail((int(N*.93),int(N*.93)),Image.Resampling.LANCZOS)
    canvas=Image.new("RGBA",(N,N),(0,0,0,0))
    canvas.alpha_composite(source,((N-source.width)//2,(N-source.height)//2))
    return canvas

def mono_process(source):
    source=source.resize((N,N),Image.Resampling.BILINEAR).convert("RGBA")
    sample=source.resize((ANALYZE_SIZE,ANALYZE_SIZE),Image.Resampling.BILINEAR)
    hist=[0]*BUCKETS
    for r,g,b,a in sample.getdata():
        if a>ALPHA_GATE: hist[int(r*.3+g*.59+b*.11)//8]+=1
    dominant=(max(range(BUCKETS),key=lambda i:hist[i])+1)*8-1
    threshold=255-dominant
    gray_values=[]; alpha_values=[]; min_gray=255
    for r,g,b,a in source.getdata():
        gray=int(r*.3+g*.59+b*.11); alpha_values.append(a)
        if a==0: gray_values.append(gray); continue
        mapped=(510-(gray+threshold)) if gray+threshold>255 else gray+threshold
        if a>ALPHA_GATE and mapped<min_gray: min_gray=mapped
        gray_values.append(mapped)
    denom=CLAMP_SQ-min_gray*min_gray
    factor=GAIN/denom if denom else 0.0
    out_alpha=[]
    for gray,alpha in zip(gray_values,alpha_values):
        if alpha>ALPHA_GATE and min_gray<CLAMP_GRAY:
            alpha=max(0,min(255,int((gray*gray-CLAMP_SQ)*factor+255)))
        out_alpha.append(255 if alpha>127 else 0)
    coords=[(i%N,i//N) for i,a in enumerate(out_alpha) if a>VALID_ALPHA]
    if not coords: return None
    left=min(x for x,_ in coords); right=max(x for x,_ in coords)
    top=min(y for _,y in coords); bottom=max(y for _,y in coords)
    pad=min(left,top,N-1-right,N-1-bottom)
    if pad>=N//2: return None
    mask=Image.new("RGBA",(N,N),(255,255,255,0))
    mask.putdata([(255,255,255,a) for a in out_alpha])
    cropped=mask.crop((pad,pad,N-pad,N-pad))
    side=max(1,int(N*VISUAL_SCALE))
    resized=cropped.resize((side,side),Image.Resampling.BILINEAR)
    output=Image.new("RGBA",(N,N),(255,255,255,0))
    output.alpha_composite(resized,((N-side)//2,(N-side)//2))
    return output

def vectorize(mask):
    alpha=mask.getchannel("A").load(); scale=48.0/N; runs=[]
    for y in range(N):
        x=0
        while x<N:
            if alpha[x,y]>127:
                start=x
                while x<N and alpha[x,y]>127: x+=1
                width=(x-start)*scale
                runs.append(f"M{start*scale:.2f},{y*scale:.2f}h{width:.2f}v{scale:.2f}h{-width:.2f}Z")
            else: x+=1
    return " ".join(runs)

def drawable_name(package):
    safe=re.sub(r"[^a-z0-9_]","_",package.lower())
    return "jus_"+safe[:78]+"_"+hashlib.sha1(package.encode()).hexdigest()[:6]

def download_apk(package, folder):
    url=f"https://d.apkpure.com/b/APK/{package}?version=latest"
    target=folder/(hashlib.sha1(package.encode()).hexdigest()[:12]+".apk")
    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
    for attempt in range(3):
        try:
            with requests.get(url,headers=headers,stream=True,timeout=(25,180),allow_redirects=True) as response:
                response.raise_for_status(); total=0
                with target.open("wb") as out:
                    for chunk in response.iter_content(1024*1024):
                        if not chunk: continue
                        total+=len(chunk)
                        if total>350*1024*1024: raise RuntimeError("APK/XAPK exceeds 350 MB")
                        out.write(chunk)
            if not zipfile.is_zipfile(target): raise RuntimeError("response is not an APK/XAPK archive")
            return response.url,target,""
        except Exception as exc:
            target.unlink(missing_ok=True)
            if attempt==2: return url,None,str(exc)
            time.sleep(2**attempt)
    return url,None,"download failed"

def extract_base_apk(downloaded,destination):
    with zipfile.ZipFile(downloaded) as archive:
        names=archive.namelist()
        if "AndroidManifest.xml" in names:
            shutil.copyfile(downloaded,destination); return destination
        candidates=[n for n in names if n.lower().endswith(".apk")]
        if not candidates: raise RuntimeError("archive contains no APK")
        selected=next((n for n in candidates if Path(n).name.lower()=="base.apk"),None) or max(candidates,key=lambda n:archive.getinfo(n).file_size)
        with archive.open(selected) as src,destination.open("wb") as dst: shutil.copyfileobj(src,dst)
    return destination

def process_apk(group,label,package,apk,work,drawable_dir):
    key=hashlib.sha1(package.encode()).hexdigest()[:12]
    decoded=work/(key+"_decoded")
    result={"group":group,"label":label,"package":package,"status":"failed"}
    try:
        base=work/(key+"_base.apk"); extract_base_apk(apk,base)
        proc=subprocess.run(["apktool","d","-f","-s","-o",str(decoded),str(base)],capture_output=True,text=True,timeout=240)
        if proc.returncode: raise RuntimeError("apktool decode failed: "+proc.stderr[-600:])
        manifest=ET.parse(decoded/"AndroidManifest.xml").getroot()
        actual=manifest.attrib.get("package","")
        if actual!=package: raise RuntimeError(f"package mismatch: expected {package}, got {actual}")
        components=find_launcher_components(manifest,actual)
        if not components: raise RuntimeError("no MAIN/LAUNCHER activity")
        application=manifest.find("application")
        icon_ref=application.attrib.get(ANDROID+"icon","") if application is not None else ""
        image,adaptive=image_for_resource(decoded,icon_ref,public_resource_map(decoded))
        if image is None: raise RuntimeError(f"could not extract launcher icon resource {icon_ref}")
        mono=mono_process(normalize(image,adaptive))
        if mono is None: raise RuntimeError("MonoProcessor returned empty artwork")
        path_data=vectorize(mono)
        if not path_data: raise RuntimeError("vector output is empty")
        name=drawable_name(package)
        xml=('<?xml version="1.0" encoding="utf-8"?>\n'
             '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="48dp" android:height="48dp" android:viewportWidth="48" android:viewportHeight="48">\n'
             f'    <path android:fillColor="#FFFFFFFF" android:pathData="{path_data}" />\n</vector>\n')
        (drawable_dir/f"{name}.xml").write_text(xml,encoding="utf-8")
        result.update({"status":"generated","drawable":name,"components":components,"component_count":len(components),
                       "icon_source":"adaptive_foreground" if adaptive else "application_icon",
                       "apk_sha256":hashlib.sha256(base.read_bytes()).hexdigest(),"vector_path_characters":len(path_data)})
    except Exception as exc: result["error"]=str(exc)
    finally: shutil.rmtree(decoded,ignore_errors=True)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--minimum",type=int,default=70)
    parser.add_argument("--output",default="pack-nothing/src/main/res")
    parser.add_argument("--work",default="build/jusicons-work")
    args=parser.parse_args()
    if len(CATALOG)!=100 or len({x[2] for x in CATALOG})!=100: raise SystemExit(f"Catalog must have 100 unique packages; got {len(CATALOG)}")
    res=Path(args.output); drawable_dir=res/"drawable"; xml_dir=res/"xml"
    drawable_dir.mkdir(parents=True,exist_ok=True); xml_dir.mkdir(parents=True,exist_ok=True)
    work=Path(args.work); downloads_dir=work/"downloads"; downloads_dir.mkdir(parents=True,exist_ok=True)
    downloads={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures={pool.submit(download_apk,row[2],downloads_dir):row[2] for row in CATALOG}
        for future in concurrent.futures.as_completed(futures):
            package=futures[future]
            try: downloads[package]=future.result()
            except Exception as exc: downloads[package]=("",None,str(exc))
    results=[]
    for index,(group,label,package) in enumerate(CATALOG,1):
        url,apk,error=downloads.get(package,("",None,"download missing"))
        if apk is None:
            results.append({"group":group,"label":label,"package":package,"status":"download_failed","source_url":url,"error":error})
            print(f"[{index:03d}/100] SKIP {package}: {error}",flush=True); continue
        item=process_apk(group,label,package,apk,work,drawable_dir); item["source_url"]=url; results.append(item)
        print(f"[{index:03d}/100] {item['status'].upper()} {package}: {item.get('drawable',item.get('error',''))}",flush=True)
        apk.unlink(missing_ok=True)
    generated=[x for x in results if x["status"]=="generated"]
    app_items=[]; drawable_items=[]
    for item in generated:
        name=item["drawable"]
        drawable_items.append(f'  <item drawable="{name}" name="{html.escape(item["label"],quote=True)}" />')
        for component in item["components"]:
            app_items.append(f'  <item component="{html.escape(component,quote=True)}" drawable="{name}" name="{html.escape(item["label"],quote=True)}" />')
    (xml_dir/"appfilter.xml").write_text('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'+"\n".join(app_items)+"\n</resources>\n",encoding="utf-8")
    (xml_dir/"drawable.xml").write_text('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n  <version>1</version>\n'+"\n".join(drawable_items)+"\n</resources>\n",encoding="utf-8")
    report={"generator":"JusIcons MonoProcessor adapted for build-time APK extraction",
            "source_repository":"https://github.com/shubh72010/JusIcons",
            "apk_source":"APKPure direct APK endpoint; APKs are temporary CI inputs",
            "target_applications":len(CATALOG),"generated_applications":len(generated),
            "failed_applications":len(CATALOG)-len(generated),"appfilter_component_mappings":len(app_items),
            "unique_drawables":len(drawable_items),"apps":results}
    report_dir=Path("build/jusicons-report"); report_dir.mkdir(parents=True,exist_ok=True)
    (report_dir/"report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    with (report_dir/"report.md").open("w",encoding="utf-8") as stream:
        stream.write("# JusIcons 100-app generation report\n\n")
        stream.write(f"- Target packages: {len(CATALOG)}\n- Generated unique app icons: {len(generated)}\n- Appfilter mappings: {len(app_items)}\n- Failed packages: {len(CATALOG)-len(generated)}\n\n")
        stream.write("| Group | Application | Package | Result | Source type | Detail |\n|---|---|---|---|---|---|\n")
        for item in results:
            detail=str(item.get("error",item.get("drawable",""))).replace("|","/").replace("\n"," ")
            cols=[str(item.get(k,"")).replace("|","/") for k in ("group","label","package","status","icon_source")]
            stream.write("| "+" | ".join(cols+[detail])+" |\n")
    print(f"TARGET={len(CATALOG)} GENERATED={len(generated)} MAPPINGS={len(app_items)}")
    if len(generated)<args.minimum:
        print(f"ERROR: generated {len(generated)}; minimum is {args.minimum}")
        return 1
    return 0

if __name__=="__main__": raise SystemExit(main())
