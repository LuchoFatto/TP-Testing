from pathlib import Path
import shutil
import sys

import pytest


ROOT_DIR = Path(__file__).resolve().parent.parent
ROOT_STR = str(ROOT_DIR)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)


DATA_DIR = ROOT_DIR / "data"
BASELINE_DIR = ROOT_DIR / "tests" / "_baseline_data"


@pytest.fixture(autouse=True)
def restore_data_files():
    BASELINE_DIR.mkdir(exist_ok=True)
    if not any(BASELINE_DIR.iterdir()):
        for source in DATA_DIR.glob("*.json"):
            shutil.copy2(source, BASELINE_DIR / source.name)

    for source in BASELINE_DIR.glob("*.json"):
        shutil.copy2(source, DATA_DIR / source.name)

    yield

    for source in BASELINE_DIR.glob("*.json"):
        shutil.copy2(source, DATA_DIR / source.name)
