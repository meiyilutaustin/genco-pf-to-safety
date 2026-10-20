# From Power Flow to Safety — figure and animation source

Five editable figures and short conceptual animations accompanying Dr. Meiyi Li's GENCO power-flow-to-safety study (LSU).

This repository accompanies the GENCO Challenge submission. It reproduces the five visual presentations from editable SVG masters and derived aggregate values. It does not reproduce the complete scientific experiment pipeline, regenerate the private small-grid dataset, fit probes, or run GENCO inference.

View the ready-to-use high-resolution assets in `media/`. Their filenames are stable; the short WebP loops play automatically in compatible image viewers. Editable vector previews are also checked in.

## Contents

- `masters/`: the five editable SVG masters. Their physical diagrams are schematic; the first, second and fourth include conceptual illustrations.
- `data/`: aggregate Texas ranking curves and selected review-budget endpoints; aggregate boundary counts; eight paired hidden/output feature comparisons. No raw private scenarios, labels, model weights or activations are included.
- `build.py`, `probe_overlay.py`, `reuse_overlay.py`, `article.py`: build the vector HTML animation previews and combined post preview.
- `export_stills.cjs`: render 3840×2160 static PNGs and editable final SVGs.
- `post.md`: the accompanying five-section narrative candidate.

The animations interpolate between recorded curve points and use schematic motion. They are not optimization histories or new measurements. The hidden/output comparison uses layer 11, four grids, two probe heads, and Q limits in both feature sets. The case5 linear comparison ties. The comparison does not isolate a benefit caused by pretraining. Raw-input controls also recover information absent from the tested compressed output.

## Rebuild vector previews

Python 3.10 or newer is sufficient:

```sh
python3 build.py
python3 -m http.server 8000
```

Open `http://localhost:8000/02-design-and-probe.html` through `05-probe-results.html`. These SVG-based pages play automatically and retain vector sharpness. The first figure is static. The combined `index.html` references the ready-to-use exports checked into `media/`.

## Rebuild static exports

Use Node.js 18 or newer:

```sh
npm install
npx playwright install chromium
node export_stills.cjs
```

To use an existing Chrome installation instead of Playwright's bundled Chromium, set `CHROME_PATH` to that installation's executable path. No machine-specific path is embedded in the scripts. Pillow is needed by the animation encoder.

## Rebuild lossless animation exports

After generating the vector previews and installing Playwright:

```sh
python3 -m pip install -r requirements.txt
node export_lossless.cjs
```

The exporter captures the vector scene directly at 3840×2160 and encodes a lossless animated WebP at 12 frames per second. It does not transcode an MP4. Loops last 7, 8, 9 and 7 seconds. Temporary PNG frames are removed after successful encoding. This preserves rasterized text and line colors; post-width display can still make small labels hard to read. Export commands write new files at the repository root; copy reviewed replacements into `media/` to update the combined preview.

## Model and data availability

[SOURCES.md](SOURCES.md) distinguishes the frozen small-grid checkpoint from the published Texas predictions and records the verified checkpoint revision and toolkit version.

The upstream GENCO challenge and OpenGridFM resources are linked from the [official challenge page](https://huggingface.co/spaces/gridfm/genco-challenge). The Texas evaluation uses the authors' published predictions on their training grid. The unseen small-grid scenarios were generated for this study and are not included in this package. The released aggregate values support redrawing these selected figures, not independent reproduction of every statistical estimate.

This repository contains figure reproduction code, not a standalone scientific evaluation pipeline. No new model was trained for these visualizations. GENCO upstream resources and the public Texas files retain their upstream terms; the generated study data remain private.

## License and contact

Public source repository: https://github.com/meiyilutaustin/genco-pf-to-safety. Original code and accompanying original figure assets are provided under the MIT License (see LICENSE). This does not relicense upstream GENCO models, third-party software or upstream datasets; their original terms apply. Contact: Dr. Meiyi Li, LSU, mli30@lsu.edu.
