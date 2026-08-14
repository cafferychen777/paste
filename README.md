# PASTE Modern

`paste-modern` is a focused maintained distribution of
[PASTE](https://github.com/raphael-group/paste) for spatial transcriptomics
registration. The Python import remains `paste`.

```bash
pip install paste-modern
```

The package retains the four runtime APIs used by ChatSpatial:

- `pairwise_align`
- `center_align`
- `stack_slices_pairwise`
- `stack_slices_center`

It delegates fused Gromov-Wasserstein optimization to POT's current public
`ot.gromov.fused_gromov_wasserstein` API. This removes the private solver copy
whose callback signature became incompatible with modern POT releases. Plotting,
IPython, Scanpy, and notebook-only assets are intentionally not part of this
runtime distribution.

## Compatibility

- Python 3.11–3.14
- POT 0.9.6+
- NumPy and PyTorch POT backends

## Attribution

PASTE was developed by Max Land and the Raphael Lab and published in
*Nature Methods*. See the [original repository](https://github.com/raphael-group/paste)
for the paper, tutorials, datasets, and complete historical project. This
maintained distribution remains under the original BSD 3-Clause license.
