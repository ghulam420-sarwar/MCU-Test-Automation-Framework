"""Smoke + functional tests for the DUT."""
import time
import pytest


# ---------- smoke ----------
def test_ping_responds(dut):
    r = dut.cmd("PING")
    assert r.ok and r.payload == "PONG"


def test_version_string(dut):
    r = dut.cmd("VER?")
    assert r.ok
    parts = r.payload.split(".")
    assert len(parts) == 3 and all(p.isdigit() for p in parts), \
        f"bad version format: {r.payload!r}"


def test_chip_id_stable(dut):
    ids = {dut.cmd("ID?").payload for _ in range(5)}
    assert len(ids) == 1, f"chip id changed across reads: {ids}"


# ---------- functional ----------
@pytest.mark.parametrize("a,b,expect", [
    (0, 0, 0),
    (1, 2, 3),
    (-5, 10, 5),
    (99999, 1, 100000),
])
def test_add_command(dut, a, b, expect):
    r = dut.cmd(f"ADD {a} {b}")
    assert r.ok
    assert int(r.payload) == expect


def test_echo_preserves_text(dut):
    msg = "hello embedded world"
    r = dut.cmd(f"ECHO {msg}")
    assert r.ok
    assert r.payload == msg


def test_unknown_command_errors(dut):
    r = dut.cmd("FOOBAR")
    assert not r.ok


# ---------- timing ----------
def test_response_latency_under_20ms(dut):
    latencies = []
    for _ in range(30):
        t0 = time.perf_counter()
        r = dut.cmd("PING")
        latencies.append((time.perf_counter() - t0) * 1000)
        assert r.ok
    avg = sum(latencies) / len(latencies)
    assert avg < 20.0, f"avg latency {avg:.2f} ms exceeds budget"


# ---------- hardware ----------
def test_led_toggle(dut):
    assert dut.cmd("LED 1").ok
    time.sleep(0.2)
    assert dut.cmd("LED 0").ok


def test_adc_in_valid_range(dut):
    r = dut.cmd("ADC?")
    assert r.ok
    v = int(r.payload)
    assert 0 <= v <= 4095, f"ADC reading {v} out of 12-bit range"
