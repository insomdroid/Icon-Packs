#!/usr/bin/env node
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { FigmaDocument, FigmaRenderer } from "@grida/refig";
import { parseFig, nodeId } from "openfig-core";

const input = process.argv[2] ?? "references/kitkat-archives/App & Brand Icons Pack (Community).fig";
const output = process.argv[3] ?? "build/nothink-figma-export";
await mkdir(output, { recursive: true });
console.log("FIGMA_SOURCE=" + input);

const bytes = new Uint8Array(await readFile(input));
const parsed = parseFig(bytes);
const document = FigmaDocument.fromFile(input);
const renderer = new FigmaRenderer(document);
const exported = [];
const failures = [];
const seen = new Set();

try {
  for (const node of parsed.nodes) {
    const id = nodeId(node);
    const name = typeof node.name === "string" ? node.name.trim() : "";
    const width = Number(node.size?.x ?? 0);
    const height = Number(node.size?.y ?? 0);
    const kind = node.type;
    const renderableContainer = kind === "FRAME" || kind === "COMPONENT" || kind === "INSTANCE" || kind === "GROUP" || kind === 3 || kind === 4 || kind === 15 || kind === 16;
    if (!id || !name || !renderableContainer || width < 12 || height < 12 || width > 1024 || height > 1024) continue;
    const key = id;
    if (seen.has(key)) continue;
    seen.add(key);
    try {
      const rendered = await renderer.render(id, { format: "png", scale: 2 });
      const filename = `${name.replace(/[^a-zA-Z0-9._-]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 72) || "unnamed"}__${id.replace(/:/g, "_")}.png`;
      await writeFile(path.join(output, filename), rendered.data);
      exported.push({ id, name, width, height, file: filename, type: String(node.type ?? "") });
      console.log(`FIGMA_EXPORTED ${id} ${name}`);
    } catch (error) {
      failures.push({ id, name, error: String(error).slice(0, 500) });
    }
  }
} finally {
  renderer.dispose();
}

const manifest = {
  source: input,
  figVersion: parsed.header?.version ?? null,
  parsedNodes: parsed.nodes.length,
  renderedNodes: exported.length,
  failedNodes: failures.length,
  icons: exported,
  failures,
};
await writeFile(path.join(output, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log(`FIGMA_NODES=${parsed.nodes.length} RENDERED=${exported.length} FAILED=${failures.length}`);
if (exported.length === 0) process.exitCode = 1;
