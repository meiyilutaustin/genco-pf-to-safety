# Model, toolkit and data sources

This repository reproduces the selected figures and animations from checked-in aggregate values. It does not load model weights or regenerate study data.

## Frozen small-grid GENCO

The study used the pretraining checkpoint from [gridfm/genco-pf-transfer at revision 45bcde49af8e0767074790e48af8e7babf06f0c0](https://huggingface.co/gridfm/genco-pf-transfer/tree/45bcde49af8e0767074790e48af8e7babf06f0c0):

`mlflow/pretrain/1_h_100_32/artifacts/model/best_model_state_dict.pt`

Checkpoint SHA256: `b2c9cf9b1007e24b924c83f440e57d252d500df126c4a4f11fba10c1762f5d41`. Configuration and normalization artifacts use the same repository revision.

The model configuration and normalization artifacts were read from the same upstream repository's `finetune/case118_100/` directory. This directory name identifies the supplied configuration assets; the tested model weights are the pretraining checkpoint above. It does not mean our frozen small-grid probes fine-tuned GENCO.

## Texas published predictions

The Texas N−2 safety-screening analysis uses the test cases and published predictions from [gridfm/genco-pf-contingency](https://huggingface.co/gridfm/genco-pf-contingency). It does not run the small-grid checkpoint above on Texas. Texas is a training-grid evaluation; the four small grids are unseen grids in the separate frozen-model experiment.

## Toolkit and scope

The model interface uses [OpenGridFM gridfm-graphkit 0.9.0.3](https://pypi.org/project/gridfm-graphkit/0.9.0.3/). The environment freeze records this version; the checked environment metadata and relevant model-source hash match that freeze. This identifies the toolkit version, not a claim of bitwise-identical replay across all hardware. The figure build itself uses Python's standard library; the optional raster exports use Playwright/Chromium and Pillow. See `package.json` and `requirements.txt` for figure-build dependencies.

The upstream [GENCO paper](https://arxiv.org/abs/2608.09921) and [challenge page](https://huggingface.co/spaces/gridfm/genco-challenge) describe the model and toolkit. No upstream model, code or data is relicensed by this repository's MIT license.

The supplied aggregate tables reproduce the selected display values. The newly generated small-grid scenarios, labels and hidden activations are private. No original raw scenarios, activations, weights, fitted models or experiment caches are included.

Upstream repository names and artifact paths identify the study sources. A repository's current `main` revision is not asserted to be the study revision. Independent end-to-end reproduction of the private-data experiments is outside this release's scope.
