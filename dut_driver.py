"""
DUT Driver
----------
Thin wrapper around pyserial that speaks the DUT command protocol.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import serial

log = logging.getLogger(__name__)


@dataclass
class Response:
    ok: bool
    payload: str = ""
    raw: str = ""


class Dut:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 2.0):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser: serial.Serial | None = None

    def open(self) -> None:
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        time.sleep(1.5)      # let ESP32 boot
        self._ser.reset_input_buffer()
        log.info("DUT opened on %s", self.port)

    def close(self) -> None:
        if self._ser:
            self._ser.close()
            self._ser = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *_exc):
        self.close()

    def cmd(self, line: str) -> Response:
        assert self._ser, "DUT not open"
        self._ser.write((line + "\n").encode())
        raw = self._ser.readline().decode(errors="replace").strip()
        log.debug(">>> %s  <<< %s", line, raw)

        if raw == "PONG":
            return Response(True, "PONG", raw)
        if raw.startswith("OK"):
            return Response(True, raw[2:].strip(), raw)
        if raw.startswith("ERR"):
            return Response(False, raw[3:].strip(), raw)
        return Response(False, "", raw)
