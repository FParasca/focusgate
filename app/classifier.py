import json
import os
from pathlib import Path
import psutil

PATH = Path(__file__).resolve().parent.parent
CONFIG_PATH = PATH / "config" / "allowlist.json"

SISTEM_FILES = (
    "c:\\windows\\",
    "c:\\programdata\\microsoft\\windows defender\\",
)


def in_sistem(exe: str | None):
    if not exe or not os.path.isabs(exe):
        return True
    return exe.lower().startswith(SISTEM_FILES)


def load_config(path: Path = CONFIG_PATH):
    if not path.exists():
        raise FileNotFoundError(f"Not in {path}")
    with open(path, encoding="utf-8") as f:
        dados = json.load(f)
    allowed = {n.lower() for n in dados.get("allowed", [])}
    return allowed


def get_protected_pids():
    protected = set()
    try:
        protected.add(psutil.Process().pid)
        for p in psutil.Process().parents():
            protected.add(p.pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return protected


def descend_from_allowed(process: psutil.Process, allowed: set[str]):
    try:
        for p in process.parents():
            if p.name() and p.name().lower() in allowed:
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return False


def process_classify(p: psutil.Process, allowed: set[str], protected_pids: set[int]):
    try:
        pid = p.pid
        nome = (p.info.get("name") or "").lower()
        exe = p.info.get("exe")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "SISTEMA"

    if pid in protected_pids:
        return "SYSTEM"
    if in_sistem(exe):
        return "SYSTEM"
    if nome in allowed:
        return "ALLOWED"
    if descend_from_allowed(p, allowed):
        return "ALLOWED"
    return "BLOCK"


def classify_all():
    allowed = load_config()
    protected_pids = get_protected_pids()

    categorias = ("SYSTEM", "SYSTEM", "ALLOWED", "BLOCK")
    grupos = {c: [] for c in categorias}

    for p in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if not p.info.get("name"):
                continue
            cat = process_classify(p, allowed, protected_pids)
            grupos[cat].append({
                "pid": p.info["pid"],
                "name": p.info["name"],
                "exe": p.info["exe"],
                "process": p
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return grupos