import json
import logging
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Dict, Any

from focusgate.constants import (
    FOCUSGATE_DIR,
    STATE_FILE,
    STATE_SCHEMA_VERSION,
    MODE_FREE,
    DEFAULT_MODE_ON_ERROR,
)

logger = logging.getLogger(__name__)


def _ensure_dir_exists():
    FOCUSGATE_DIR.mkdir(parents=True, exist_ok=True)


def read_state():

    if not STATE_FILE.exists():
        logger.info("State file does not exist. Assuming default mode.")
        return {"mode": DEFAULT_MODE_ON_ERROR, "since": None, "schema_version": STATE_SCHEMA_VERSION}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            if "mode" not in data:
                raise ValueError("Key 'mode' is missing in state.json")

            return data
            
    except (json.JSONDecodeError, ValueError, OSError) as e:
        logger.error(f"Error reading state.json: {e}. Fail-open activated. Assuming mode 'free'.")
        return {"mode": DEFAULT_MODE_ON_ERROR, "since": None, "schema_version": STATE_SCHEMA_VERSION}


def write_state(mode: str):

    _ensure_dir_exists()
    
    data = {
        "schema_version": STATE_SCHEMA_VERSION,
        "mode": mode,
        "since": datetime.now(timezone.utc).isoformat(),
        "set_by": "launcher" 
    }

    temp_file = STATE_FILE.with_suffix(".tmp")
    
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
            
        
        temp_file.replace(STATE_FILE)
        logger.info(f"State updated to '{mode}' successfully.")
        
    except OSError as e:
        logger.critical(f"CRITICAL FAILURE while writing state: {e}")
        if temp_file.exists():
            try:
                temp_file.unlink()
            except OSError:
                pass
        raise


def get_current_mode() -> str:
    """Helper to get only the current mode string."""
    return read_state().get("mode", DEFAULT_MODE_ON_ERROR)