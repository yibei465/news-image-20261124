// news-image-20261124 — entrypoint (Node 22, standard library only).
//
// The image itself is drawn once by gen_image.py (a local Pillow build tool)
// and shipped in this repository as entry.png. This program only places that
// exact file at /output/entry.png, so every run writes the same bytes and the
// judge sees exactly the file in the repository. The copy is byte for byte:
// no re-encoding, no timestamps, nothing that could differ between runs.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
