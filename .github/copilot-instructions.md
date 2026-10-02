## Project context (for AI/LLM assistants)

- **Purpose**: a sim-racing pedal rig has a load cell (brake) and a Hall sensor (throttle). This app lets a user calibrate the raw sensor min/max ranges and persist them to `config.txt` so an Arduino Leonardo can later read them.
- **Current scope**: local-only — read/edit/save `config.txt`. Uploading the config to the Arduino itself is **not implemented yet** and is the likely next feature.
- **Architecture**: layered, clean-code style — `models` (domain data + validation), `services` (file I/O), `ui` (Tkinter presentation). No business logic lives in the UI layer; `MainWindow` only reads form values, delegates to `PedalConfig.validate()`, then calls `ConfigRepository.save()`.
- **Config file format** (`config.txt`, plain text, `Key = Value` per line):
  ```
  MinLoadCell = 5000
  MaxLoadCell = 400000
  MinHall = 500
  MaxHall = 600
  ```
- **Validation rule**: for each pair, Min must be strictly less than Max; all four values must be integers.
- **Packaging**: PyInstaller builds a onefile/windowed `.exe`. `main.py` resolves `config.txt` next to `sys.executable` when frozen, otherwise next to `main.py` — keep this distinction in mind when changing path logic.
