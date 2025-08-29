def test_imports():
    from curves.zero_curve import ZeroCurve
    from pricing.bond import Bond, price_bond, dv01_bond
    assert True