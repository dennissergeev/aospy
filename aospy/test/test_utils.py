#!/usr/bin/env python
"""Test suite for aospy.utils module."""
import sys
import unittest

import numpy as np
import xarray as xr

import aospy.utils as au


class AospyUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.p_in_hpa = np.array([1000, 925, 850, 775, 700, 600, 500, 400, 300,
                                  200, 150, 100, 70, 50, 30, 20, 10],
                                 dtype=np.float64)
        self.p_in_pa = self.p_in_hpa*1e2
        self.p_top = 0
        self.p_bot = 1.1e5
        self.p_edges = 0.5*(self.p_in_pa[1:] + 0.5*self.p_in_pa[:-1])
        self.phalf = np.concatenate(([self.p_bot], self.p_edges, [self.p_top]))

    def tearDown(self):
        pass


class TestUtils(AospyUtilsTestCase):
    def test_to_pascal_scalar_positive(self):
        self.assertEqual(au.to_pascal(1e2), 1e4)
        self.assertEqual(au.to_pascal(1e5), 1e5)

    def test_to_pascal_scalar_negative(self):
        self.assertEqual(au.to_pascal(-1e2), -1e4)
        self.assertEqual(au.to_pascal(-1e5), -1e5)

    def test_to_pascal_array(self):
        np.testing.assert_array_equal(au.to_pascal(self.p_in_hpa),
                                      self.p_in_pa)
        np.testing.assert_array_equal(au.to_pascal(self.p_in_pa), self.p_in_pa)

    # def test_to_phalf_from_pfull(self):
    #     # S. Hill 2015-11-10: This needs to be rewritten.
    #     np.testing.assert_array_equal(
    #         au.to_phalf_from_pfull(self.p_in_pa, self.p_top, self.p_bot),
    #         self.phalf
    #     )


def test_dp_from_p():
    path = (
        '/archive/Spencer.Hill/am2/am2clim_reyoi/gfdl.ncrc2-default-prod/pp/'
        'atmos/ts/monthly/30yr/atmos.198301-201212.ucomp.nc'
    )
    ds = xr.open_dataset(path)
    p = ds.level
    path = (
        '/archive/Spencer.Hill/am2/am2clim_reyoi/gfdl.ncrc2-default-prod/pp/'
        'atmos/ts/monthly/30yr/atmos.198301-201212.ps.nc'
    )
    ps = xr.open_dataset(path).ps
    dp = au.dp_from_p(p, ps)
    np.testing.assert_array_equal(p.level, dp.level)
    # TODO: More tests


if __name__ == '__main__':
    sys.exit(unittest.main())
