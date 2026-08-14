from __future__ import annotations

import anndata as ad
import numpy as np

import paste


def _slice(offset: float = 0.0) -> ad.AnnData:
    counts = np.array(
        [
            [5, 1, 0, 2],
            [4, 2, 0, 1],
            [0, 1, 5, 2],
            [1, 0, 4, 3],
            [3, 2, 1, 0],
            [2, 3, 0, 1],
        ],
        dtype=float,
    )
    result = ad.AnnData(counts)
    result.var_names = [f"gene_{index}" for index in range(result.n_vars)]
    result.obsm["spatial"] = (
        np.array([[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], [2, 1]], dtype=float) + offset
    )
    return result


def test_pairwise_alignment_and_stacking() -> None:
    first = _slice()
    second = _slice(0.25)
    plan = paste.pairwise_align(first, second, gpu_verbose=False, numItermax=20)

    assert plan.shape == (first.n_obs, second.n_obs)
    assert np.isfinite(plan).all()
    assert np.isclose(plan.sum(), 1.0)

    stacked = paste.stack_slices_pairwise([first, second], [plan])
    assert len(stacked) == 2
    assert all(item.obsm["spatial"].shape == (6, 2) for item in stacked)


def test_center_alignment_uses_public_pot_solver() -> None:
    first = _slice()
    second = _slice(0.25)
    initial = paste.pairwise_align(first, second, gpu_verbose=False, numItermax=20)
    center, plans = paste.center_align(
        first,
        [first, second],
        n_components=2,
        max_iter=1,
        pis_init=[np.eye(first.n_obs) / first.n_obs, initial],
        gpu_verbose=False,
    )

    assert center.shape == first.shape
    assert len(plans) == 2
    assert all(np.isfinite(plan).all() for plan in plans)
