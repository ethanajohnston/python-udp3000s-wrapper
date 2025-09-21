# udp3000s.py
# Minimal per-channel control for UNI-T UDP3000S series via VISA/SCPI.
# pip install pyvisa  (and optionally: pip install pyvisa-py)

import pyvisa

import warnings
from pyvisa.errors import VisaIOWarning
warnings.simplefilter("ignore", VisaIOWarning)

class UDP3000S:
    def __init__(self, resource: str, timeout_ms: int = 2000):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource)
        self.inst.timeout = timeout_ms
        self.inst.read_termination = "\n"
        self.inst.write_termination = "\n"

    def close(self):
        try:
            self.inst.close()
        finally:
            try:
                self.rm.close()
            except Exception:
                pass

    def idn(self) -> str:
        return self.inst.query("*IDN?").strip()

    # ----- internal -----
    @staticmethod
    def _chs(ch: int | str) -> str:
        if isinstance(ch, int):
            if ch not in (1, 2, 3):
                raise ValueError("Channel must be 1, 2, or 3.")
            return f"CH{ch}"
        s = str(ch).upper()
        if s in ("CH1", "CH2", "CH3"):
            return s
        raise ValueError("Channel must be CH1, CH2, or CH3 (or 1/2/3).")

    @staticmethod
    def _chnum(chs: str) -> int:
        return {"CH1": 1, "CH2": 2, "CH3": 3}[chs]

    # ----- output on/off (single command) -----
    def set_output(self, ch: int | str, on: bool) -> None:
        chs = self._chs(ch)
        self.inst.write(f":OUTPut:STATe {chs}, {'ON' if on else 'OFF'}")

    # ----- setpoints (single command each) -----
    def set_voltage(self, ch: int | str, volts: float) -> None:
        n = self._chnum(self._chs(ch))
        self.inst.write(f":SOURce{n}:VOLTage {volts:.3f}")

    def set_current(self, ch: int | str, amps: float) -> None:
        n = self._chnum(self._chs(ch))
        self.inst.write(f":SOURce{n}:CURRent {amps:.3f}")

    # ----- readback (separate queries; returns floats) -----
    def get_voltage(self, ch: int | str) -> float:
        chs = self._chs(ch)
        return float(self.inst.query(f":MEASure:VOLTage? {chs}"))

    def get_current(self, ch: int | str) -> float:
        chs = self._chs(ch)
        return float(self.inst.query(f":MEASure:CURRent? {chs}"))

    def get_v_i(self, ch: int | str) -> tuple[float, float]:
        return self.get_voltage(ch), self.get_current(ch)

    # ----- OVP (level + enable) -----
    def set_ovp_level(self, ch: int | str, volts: float) -> None:
        chs = self._chs(ch)
        self.inst.write(f":OUTPut:OVP:VALue {chs}, {volts:.3f}")

    def get_ovp_level(self, ch: int | str) -> float:
        chs = self._chs(ch)
        return float(self.inst.query(f":OUTPut:OVP:VALue? {chs}"))

    def set_ovp_state(self, ch: int | str, on: bool) -> None:
        chs = self._chs(ch)
        self.inst.write(f":OUTPut:OVP:STATe {chs}, {'ON' if on else 'OFF'}")

    def get_ovp_state(self, ch: int | str) -> bool:
        chs = self._chs(ch)
        return self.inst.query(f":OUTPut:OVP:STATe? {chs}").strip().upper() == "ON"

    # ----- OCP (level + enable) -----
    def set_ocp_level(self, ch: int | str, amps: float) -> None:
        chs = self._chs(ch)
        self.inst.write(f":OUTPut:OCP:VALue {chs}, {amps:.3f}")

    def get_ocp_level(self, ch: int | str) -> float:
        chs = self._chs(ch)
        return float(self.inst.query(f":OUTPut:OCP:VALue? {chs}"))

    def set_ocp_state(self, ch: int | str, on: bool) -> None:
        chs = self._chs(ch)
        self.inst.write(f":OUTPut:OCP:STATe {chs}, {'ON' if on else 'OFF'}")

    def get_ocp_state(self, ch: int | str) -> bool:
        chs = self._chs(ch)
        return self.inst.query(f":OUTPut:OCP:STATe? {chs}").strip().upper() == "ON"
