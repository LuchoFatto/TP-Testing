import json
from pathlib import Path
from typing import Any, Dict, List

from app.core.logger import logger


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


class FileRepository:
    def __init__(self, filename: str):
        self.filepath = DATA_DIR / filename

    def read_all(self) -> List[Dict[str, Any]]:
        logger.info("Reading file: %s", self.filepath.name)
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_all(self, data: List[Dict[str, Any]]) -> None:
        logger.info("Writing file: %s (%s records)", self.filepath.name, len(data))
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
