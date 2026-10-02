# Pedal Calibration

Simple desktop app to view and save brake (load cell) and throttle (Hall sensor) calibration min/max values to `config.txt`.

## Project structure

```
main.py                        # entry point
app/
  models/pedal_config.py       # PedalConfig dataclass + validation
  services/config_repository.py# load/save config.txt
  ui/main_window.py             # Tkinter form (Brake + Throttle sections, Save button)
```

## Requirements

- Python 3.12+ (uses only the standard library: `tkinter`)

## Run from source

```powershell
python main.py
```

The app loads `config.txt` from the same folder on startup (if present) and writes to it when you click **Save**.

## Build a standalone executable

Install dependencies (one-time):

```powershell
python -m pip install -r requirements.txt
```

Build a single-file, windowed `.exe`:

```powershell
python -m PyInstaller --noconfirm --onefile --windowed --name PedalCalibration main.py
```

The executable is produced at `dist/PedalCalibration.exe`. It reads/writes `config.txt` next to the `.exe` itself. Rerun the same command after code changes to rebuild.

`build/` and `PedalCalibration.spec` are PyInstaller's intermediate artifacts — safe to delete; only `dist/PedalCalibration.exe` is needed to run the app.
