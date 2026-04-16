"""Pytest fixtures shared by every test module."""
import os
import pytest

from framework.dut_driver import Dut


def pytest_addoption(parser):
    parser.addoption("--port", default=os.environ.get("DUT_PORT", "/dev/ttyUSB0"))
    parser.addoption("--baud", type=int, default=115200)


@pytest.fixture(scope="session")
def dut(pytestconfig):
    port = pytestconfig.getoption("--port")
    baud = pytestconfig.getoption("--baud")
    with Dut(port, baud) as d:
        yield d
