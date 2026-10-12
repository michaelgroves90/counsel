import counsel


def test_package_imports(capsys):
    counsel.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from counsel!\n"
