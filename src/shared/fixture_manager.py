import json
from pathlib import Path


class FixtureManager:
    ROOT = Path("tests/fixtures")

    @classmethod
    def load(
        cls,
        stage: str,
        name: str,
    ):
        path = cls.ROOT / stage / f"{name}.json"

        if not path.exists():
            return None

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def save(
        cls,
        stage: str,
        name: str,
        data: dict,
    ):
        folder = cls.ROOT / stage
        folder.mkdir(parents=True, exist_ok=True)

        path = folder / f"{name}.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )
