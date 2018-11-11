import chutil as module


def test_versions():
    expected = "0.0"
    assert module.__version__ == expected
