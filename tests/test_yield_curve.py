# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 18:30:10 2025

@author: willp
"""

from data.treasury import get_latest_curve

def test_latest_curve_object():
    curve = get_latest_curve()
    assert curve.get_rate("10Y") is not None
    assert "10Y" in curve.data.index