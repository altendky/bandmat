"""Tests for addition, multiplication, etc using banded matrices."""

# Copyright 2013 Matt Shannon

# This file is part of bandmat.
# See `License` for details of license and warranty.

from bandmat.testhelp import assert_allclose
from bandmat.test_core import gen_BandMat

import bandmat as bm
import bandmat.full as fl

import unittest
import numpy as np
import random
from numpy.random import randn, randint

def randBool():
    return randint(0, 2) == 0

class TestTensor(unittest.TestCase):
    def test_dot_mv_plus_equals(self, its = 100):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b = randn(size)
            c = randn(size)
            a_full = a_bm.full()
            c_good = c.copy()

            bm.dot_mv_plus_equals(a_bm, b, c)
            c_good += np.dot(a_full, b)
            assert_allclose(c, c_good)

    def test_dot_mv(self, its = 100):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b = randn(size)
            a_full = a_bm.full()

            c = bm.dot_mv(a_bm, b)
            c_good = np.dot(a_full, b)
            assert_allclose(c, c_good)

    def test_dot_mm_plus_equals(self, its = 50):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b_bm = gen_BandMat(size)
            c_bm = gen_BandMat(size)
            diag = None if randBool() else randn(size)
            diag_value = np.ones((size,)) if diag is None else diag
            a_full = a_bm.full()
            b_full = b_bm.full()
            c_full = c_bm.full()
            l = c_bm.l
            u = c_bm.u

            bm.dot_mm_plus_equals(a_bm, b_bm, c_bm, diag = diag)
            c_full += fl.band_ec(
                l, u,
                np.dot(np.dot(a_full, np.diag(diag_value)), b_full)
            )
            assert_allclose(c_bm.full(), c_full)

    def test_dot_mm(self, its = 50):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b_bm = gen_BandMat(size)
            diag = None if randBool() else randn(size)
            diag_value = np.ones((size,)) if diag is None else diag
            a_full = a_bm.full()
            b_full = b_bm.full()

            c_bm = bm.dot_mm(a_bm, b_bm, diag = diag)
            c_full = np.dot(np.dot(a_full, np.diag(diag_value)), b_full)
            assert c_bm.l == a_bm.l + b_bm.l
            assert c_bm.u == a_bm.u + b_bm.u
            assert c_bm.size == size
            assert_allclose(c_bm.full(), c_full)

    def test_dot_mm_partial(self, its = 50):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b_bm = gen_BandMat(size)
            l = random.choice([0, 1, randint(0, 10)])
            u = random.choice([0, 1, randint(0, 10)])
            diag = None if randBool() else randn(size)
            diag_value = np.ones((size,)) if diag is None else diag
            a_full = a_bm.full()
            b_full = b_bm.full()

            c_bm = bm.dot_mm_partial(l, u, a_bm, b_bm, diag = diag)
            c_full = fl.band_ec(
                l, u,
                np.dot(np.dot(a_full, np.diag(diag_value)), b_full)
            )
            assert c_bm.l == l
            assert c_bm.u == u
            assert c_bm.size == size
            assert_allclose(c_bm.full(), c_full)

    def test_dot_mmm_partial(self, its = 50):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_bm = gen_BandMat(size)
            b_bm = gen_BandMat(size)
            c_bm = gen_BandMat(size)
            l = random.choice([0, 1, randint(0, 10)])
            u = random.choice([0, 1, randint(0, 10)])
            a_full = a_bm.full()
            b_full = b_bm.full()
            c_full = c_bm.full()

            d_bm = bm.dot_mmm_partial(l, u, a_bm, b_bm, c_bm)
            d_full = fl.band_ec(l, u, np.dot(a_full, np.dot(b_full, c_full)))
            assert d_bm.l == l
            assert d_bm.u == u
            assert d_bm.size == size
            assert_allclose(d_bm.full(), d_full)

    def test_band_of_outer_plus_equals(self, its = 50):
        for it in range(its):
            size = random.choice([0, 1, randint(0, 10), randint(0, 100)])
            a_vec = randn(size)
            b_vec = randn(size)
            mult = randn()
            mat_bm = gen_BandMat(size)
            mat_full = mat_bm.full()
            l = mat_bm.l
            u = mat_bm.u

            bm.band_of_outer_plus_equals(a_vec, b_vec, mat_bm, mult = mult)
            mat_full += fl.band_ec(l, u, np.outer(a_vec, b_vec) * mult)
            assert_allclose(mat_bm.full(), mat_full)

if __name__ == '__main__':
    unittest.main()
