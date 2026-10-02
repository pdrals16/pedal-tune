"""Domain model for pedal calibration values."""

from dataclasses import dataclass


class InvalidPedalConfigError(ValueError):
    """Raised when a PedalConfig fails validation."""


@dataclass
class PedalConfig:
    min_load_cell: int
    max_load_cell: int
    min_hall: int
    max_hall: int

    def validate(self) -> None:
        if self.min_load_cell >= self.max_load_cell:
            raise InvalidPedalConfigError(
                "MinLoadCell must be less than MaxLoadCell."
            )
        if self.min_hall >= self.max_hall:
            raise InvalidPedalConfigError("MinHall must be less than MaxHall.")
