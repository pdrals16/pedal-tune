"""Entry point for the Pedal Calibration app."""

import sys
from pathlib import Path

from app.services.config_repository import ConfigRepository
from app.ui.main_window import MainWindow


def _app_dir() -> Path:
    # When frozen by PyInstaller, __file__ points inside a temp extraction folder.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def main() -> None:
    config_path = _app_dir() / "config.txt"
    window = MainWindow(config_path=config_path, repository=ConfigRepository())
    window.mainloop()


if __name__ == "__main__":
    main()
