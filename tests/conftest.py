import pytest


def pytest_addoption(parser):
    print('ran')
    parser.addoption("--chromedriver", action="store", default=None, help="Path to chromedriver")


@pytest.fixture
def chromedriver(pytestconfig, monkeypatch):
    chromedriver = pytestconfig.getoption("--chromedriver")
    if chromedriver:
        monkeypatch.setenv("CHROMEDRIVER_PATH", chromedriver)
    yield
    monkeypatch.delenv("CHROMDRIVER_PATH", raising=False)
