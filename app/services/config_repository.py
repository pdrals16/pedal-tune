"""Reads and writes PedalConfig as a simple `Key = Value` text file."""

from pathlib import Path

from app.models.pedal_config import PedalConfig

_MIN_LOAD_CELL_KEY = "MinLoadCell"
_MAX_LOAD_CELL_KEY = "MaxLoadCell"
_MIN_HALL_KEY = "MinHall"
_MAX_HALL_KEY = "MaxHall"


class ConfigRepository:
    def load(self, path: Path) -> PedalConfig | None:
        """Returns None when no config file exists yet."""
        if not path.exists():
            return None

        values: dict[str, int] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = int(value.strip())

        return PedalConfig(
            min_load_cell=values[_MIN_LOAD_CELL_KEY],
            max_load_cell=values[_MAX_LOAD_CELL_KEY],
            min_hall=values[_MIN_HALL_KEY],
            max_hall=values[_MAX_HALL_KEY],
        )

    def save(self, path: Path, config: PedalConfig) -> None:
        lines = [
            f"{_MIN_LOAD_CELL_KEY} = {config.min_load_cell}",
            f"{_MAX_LOAD_CELL_KEY} = {config.max_load_cell}",
            f"{_MIN_HALL_KEY} = {config.min_hall}",
            f"{_MAX_HALL_KEY} = {config.max_hall}",
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
