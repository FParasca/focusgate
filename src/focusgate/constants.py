import os
from pathlib import Path


PROGRAMDATA = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
FOCUSGATE_DIR = PROGRAMDATA / "FocusGate"
STATE_FILE = FOCUSGATE_DIR / "state.json"
ALLOWLIST_FILE = FOCUSGATE_DIR / "allowlist.json"
LOG_FILE = FOCUSGATE_DIR / "focusgate.log"
STATE_SCHEMA_VERSION = 1
MODE_WORK = "work"
MODE_FREE = "free"
DEFAULT_MODE_ON_ERROR = MODE_FREE

CRITICAL_WINDOWS_PROCESSES = {
    "csrss.exe",
    "winlogon.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "explorer.exe",
    "dwm.exe",
    "smss.exe",
    "wininit.exe",
    "fontdrvhost.exe",
    "sihost.exe",
    "ctfmon.exe",
    "taskhostw.exe",
    "vgc.exe",
    "vgtray.exe",
}