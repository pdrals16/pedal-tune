"""Main window: form to view and save pedal calibration values."""

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from app.models.pedal_config import InvalidPedalConfigError, PedalConfig
from app.services.config_repository import ConfigRepository


class MainWindow(tk.Tk):
    def __init__(self, config_path: Path, repository: ConfigRepository):
        super().__init__()
        self._config_path = config_path
        self._repository = repository

        self.title("Pedal Calibration")
        self.resizable(False, False)

        self._min_load_cell_var = tk.StringVar()
        self._max_load_cell_var = tk.StringVar()
        self._min_hall_var = tk.StringVar()
        self._max_hall_var = tk.StringVar()
        self._status_var = tk.StringVar()

        self._build_layout()
        self._load_existing_config()

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=16)
        container.grid(row=0, column=0, sticky="nsew")

        self._build_section(
            container,
            row=0,
            title="Brake (Load Cell)",
            min_var=self._min_load_cell_var,
            max_var=self._max_load_cell_var,
        )
        self._build_section(
            container,
            row=1,
            title="Throttle (Hall Sensor)",
            min_var=self._min_hall_var,
            max_var=self._max_hall_var,
        )

        status_label = ttk.Label(
            container, textvariable=self._status_var, foreground="red"
        )
        status_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        save_button = ttk.Button(container, text="Save", command=self._on_save)
        save_button.grid(row=3, column=0, columnspan=2, sticky="e", pady=(12, 0))

    def _build_section(
        self,
        parent: ttk.Frame,
        row: int,
        title: str,
        min_var: tk.StringVar,
        max_var: tk.StringVar,
    ) -> None:
        section = ttk.LabelFrame(parent, text=title, padding=10)
        section.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Label(section, text="Min").grid(row=0, column=0, sticky="w")
        ttk.Entry(section, textvariable=min_var, width=12).grid(
            row=0, column=1, padx=(8, 0)
        )

        ttk.Label(section, text="Max").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(section, textvariable=max_var, width=12).grid(
            row=1, column=1, padx=(8, 0), pady=(6, 0)
        )

    def _load_existing_config(self) -> None:
        config = self._repository.load(self._config_path)
        if config is None:
            return

        self._min_load_cell_var.set(str(config.min_load_cell))
        self._max_load_cell_var.set(str(config.max_load_cell))
        self._min_hall_var.set(str(config.min_hall))
        self._max_hall_var.set(str(config.max_hall))

    def _on_save(self) -> None:
        self._status_var.set("")
        try:
            config = PedalConfig(
                min_load_cell=int(self._min_load_cell_var.get()),
                max_load_cell=int(self._max_load_cell_var.get()),
                min_hall=int(self._min_hall_var.get()),
                max_hall=int(self._max_hall_var.get()),
            )
            config.validate()
        except ValueError as error:
            message = (
                str(error)
                if isinstance(error, InvalidPedalConfigError)
                else "All fields must be whole numbers."
            )
            self._status_var.set(message)
            return

        self._repository.save(self._config_path, config)
        self._status_var.set("Saved.")
