import argparse
import sys
import time
import psutil
from focusgate.classifier import classify_all
from focusgate.state import get_current_mode
from focusgate.constants import MODE_WORK

CHECK_INTERVAL_SECONDS = 2
TERMINATE_TIMEOUT_SECONDS = 3.0


def terminate_processes(targets: list[dict]):

    alive_targets = []
    for p in targets:
        pid = p["pid"]
        name = p["name"]
        proc: psutil.Process = p["process"]
        try:
            proc.terminate()
            alive_targets.append((proc, name))
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            print(f"  [X] AccessDenied {pid} ({name}). ")

    if not alive_targets:
        return

    procs_only = [p for p, _ in alive_targets]
    _, still_alive = psutil.wait_procs(procs_only, timeout=TERMINATE_TIMEOUT_SECONDS)

    for proc in still_alive:
        try:
            proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def run_blocker():
    print("FocusGate Blocker started.")
    
    if get_current_mode() != MODE_WORK:
        print("Mode 'free' detected. The blocker will shut down.")
        sys.exit(0)

    try:
        while 1:
            if get_current_mode() != MODE_WORK:
                print("Change to 'free' mode detected. The blocker will shut down.")
                break

            groups = classify_all()
            to_block = groups.get("BLOCK", [])
            if to_block:
                print("Blocking processes:")
                terminate_processes(to_block)
        
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(0)