// news-image-20261124 — entrypoint (Node 22, standard library only).
//
// The image itself is drawn once by gen_image.py (a local Pillow build tool)
// and shipped in this repository as entry.png. This program only places that
// exact file at /output/entry.png, so every run writes the same bytes and the
// judge sees exactly the file in the repository. The copy is byte for byte:
// no re-encoding, no timestamps, nothing that could differ between runs.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify what was written: it must be a whole PNG, 1024x1024 at most,
// and no bigger than 1 MiB, or the gate refuses the entry.
const bytes = readFileSync(target);
const size = statSync(target).size;
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error('entry.png is not a PNG');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
}
console.log(`entry.png: ${size} bytes, ${width}x${height}, PNG OK`);
