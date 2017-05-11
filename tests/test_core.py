#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pytest

import numpy as np
import scipy.ndimage.fourier as sp_ndf

import dask.array as da
import dask.array.utils as dau
import dask_ndfourier as da_ndf


def test_import_core():
    try:
        from dask_ndfourier import core
    except ImportError:
        pytest.fail("Unable to import `core`.")


@pytest.mark.parametrize(
    "err_type, s, n",
    [
        (NotImplementedError, 0.0, 0),
        (TypeError, 0.0 + 0.0j, 0),
        (TypeError, {}, 0),
        (RuntimeError, [0.0], 0),
        (TypeError, [0.0, 0.0 + 0.0j], 0),
        (NotImplementedError, 0, 0),
    ]
)
@pytest.mark.parametrize(
    "funcname",
    [
        "fourier_shift",
        "fourier_gaussian",
    ]
)
def test_fourier_filter_err(funcname, err_type, s, n):
    da_func = getattr(da_ndf, funcname)

    a = np.arange(140.0).reshape(10, 14).astype(complex)
    d = da.from_array(a, chunks=(5, 7))

    with pytest.raises(err_type):
        da_func(d, s, n)


@pytest.mark.parametrize(
    "s",
    [
        0,
        (0, 0),
    ]
)
@pytest.mark.parametrize(
    "funcname",
    [
        "fourier_shift",
        "fourier_gaussian",
    ]
)
def test_fourier_filter_identity(funcname, s):
    da_func = getattr(da_ndf, funcname)
    sp_func = getattr(sp_ndf, funcname)

    a = np.arange(140.0).reshape(10, 14).astype(complex)
    d = da.from_array(a, chunks=(5, 7))

    dau.assert_eq(d, da_func(d, s))
    dau.assert_eq(sp_func(a, s), da_func(d, s))


@pytest.mark.parametrize(
    "dtype",
    [
        int,
        float,
        complex,
    ]
)
@pytest.mark.parametrize(
    "funcname",
    [
        "fourier_shift",
        "fourier_gaussian",
    ]
)
def test_fourier_filter_identity(funcname, dtype):
    s = 1

    da_func = getattr(da_ndf, funcname)
    sp_func = getattr(sp_ndf, funcname)

    a = np.arange(140.0).reshape(10, 14).astype(dtype)
    d = da.from_array(a, chunks=(5, 7))

    dau.assert_eq(sp_func(a, s), da_func(d, s))


@pytest.mark.parametrize(
    "s",
    [
        -1,
        (-1, -1),
        (-1, 2),
        (10, -9),
        (1, 0),
        (0, 2),
    ]
)
@pytest.mark.parametrize(
    "funcname",
    [
        "fourier_shift",
        "fourier_gaussian",
    ]
)
def test_fourier_filter_non_positive(funcname, s):
    da_func = getattr(da_ndf, funcname)
    sp_func = getattr(sp_ndf, funcname)

    a = np.arange(140.0).reshape(10, 14).astype(complex)
    d = da.from_array(a, chunks=(5, 7))

    dau.assert_eq(
        sp_func(a, s), da_func(d, s)
    )


@pytest.mark.parametrize(
    "s",
    [
        1,
        0.5,
        (1, 1),
        (0.8, 1.5),
    ]
)
@pytest.mark.parametrize(
    "funcname",
    [
        "fourier_shift",
        "fourier_gaussian",
    ]
)
def test_fourier_filter(funcname, s):
    da_func = getattr(da_ndf, funcname)
    sp_func = getattr(sp_ndf, funcname)

    a = np.arange(140.0).reshape(10, 14).astype(complex)
    d = da.from_array(a, chunks=(5, 7))

    dau.assert_eq(
        sp_func(a, s), da_func(d, s)
    )
