# MCU Test Automation Framework

A Python-based automated test framework for validating MCU firmware over serial. Inspired by real test work at Rouelite Techno — reduces manual test effort by running a repeatable regression suite against any ESP32 or AVR device with a compatible command-response firmware.

![Architecture](https://github.com/ghulam420-sarwar/MCU-Test-Automation-Framework/blob/main/architecture.png)

## Highlights

- **Pytest-based** — clean test reports, easy CI integration
- **Parametrised tests** — one test covers many input/output cases
- **Timing tests** — validates response latency budget (< 20 ms)
- **Hardware tests** — LED, ADC range validation
- **Session-scoped DUT fixture** — single serial open for the whole test run
- **JUnit XML output** — plug straight into GitHub Actions / Jenkins

## Project Structure

```
04-MCU-Test-Automation/
├── firmware_dut/       # Flash this to your ESP32 first
│   └── main.cpp
├── framework/
│   └── dut_driver.py   # Serial wrapper (Dut class)
├── tests/
│   ├── conftest.py     # Pytest fixtures
│   └── test_dut.py     # All test cases
└── requirements.txt
```

## Quick Start

### 1. Flash the DUT firmware
```bash
cd firmware_dut
pio run -t upload --upload-port /dev/ttyUSB0
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run tests
```bash
pytest tests/ --port /dev/ttyUSB0 -v
```

### 4. Generate HTML report
```bash
pytest tests/ --port /dev/ttyUSB0 --html=reports/report.html
```

## Sample Output

```
tests/test_dut.py::test_ping_responds              PASSED
tests/test_dut.py::test_version_string             PASSED
tests/test_dut.py::test_chip_id_stable             PASSED
tests/test_dut.py::test_add_command[0-0-0]         PASSED
tests/test_dut.py::test_add_command[1-2-3]         PASSED
tests/test_dut.py::test_add_command[-5-10-5]       PASSED
tests/test_dut.py::test_add_command[99999-1-100000]PASSED
tests/test_dut.py::test_echo_preserves_text        PASSED
tests/test_dut.py::test_unknown_command_errors     PASSED
tests/test_dut.py::test_response_latency_under_20ms PASSED  (avg 4.2 ms)
tests/test_dut.py::test_led_toggle                 PASSED
tests/test_dut.py::test_adc_in_valid_range         PASSED

12 passed in 8.34s
```

## Extending

Add a new test file in `tests/` — the `dut` fixture is automatically available:

```python
def test_my_feature(dut):
    r = dut.cmd("MYCOMMAND 42")
    assert r.ok
    assert r.payload == "expected"
```

## What I Learned

- Designing a clean command-response protocol that is easy to test
- Using pytest fixtures and parametrize to write DRY test suites
- Measuring and asserting on timing (latency budgets)
- Structuring a test project for reuse across multiple firmware variants

## License

MIT © Ghulam Sarwar
