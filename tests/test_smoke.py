def test_package_imports():
    import counsel

    assert callable(counsel.main)
