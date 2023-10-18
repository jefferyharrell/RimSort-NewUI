import json
from enum import Enum, unique, auto
from pathlib import Path
from typing import Dict, Any

from PySide6.QtCore import QObject, Signal
from platformdirs import user_data_dir


class Settings(QObject):
    @unique
    class SortingAlgorithm(Enum):
        ALPHABETICAL = auto()
        TOPOLOGICAL = auto()
        RADIOLOGICAL = auto()

    settings_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        user_data_folder_location: Path = Path(user_data_dir("NewUI"))
        user_data_folder_location.mkdir(parents=True, exist_ok=True)
        self.settings_file_path: Path = Path(user_data_folder_location, "settings.json")

        self._apply_default_settings()

    def _apply_default_settings(self) -> None:
        self._game_location: str = ""
        self._config_folder_location: str = ""
        self._steam_mods_folder_location: str = ""
        self._local_mods_folder_location: str = ""

        self._sorting_algorithm: "Settings.SortingAlgorithm" = (
            Settings.SortingAlgorithm.ALPHABETICAL
        )

        self._debug_logging: bool = False

    def apply_default_settings(self) -> None:
        self._apply_default_settings()

    @property
    def game_location(self) -> str:
        return self._game_location

    @game_location.setter
    def game_location(self, value: str) -> None:
        if self._game_location != value:
            self._game_location = value
            self.settings_changed.emit()

    @property
    def config_folder_location(self) -> str:
        return self._config_folder_location

    @config_folder_location.setter
    def config_folder_location(self, value: str) -> None:
        if self._config_folder_location != value:
            self._config_folder_location = value
            self.settings_changed.emit()

    @property
    def steam_mods_folder_location(self) -> str:
        return self._steam_mods_folder_location

    @steam_mods_folder_location.setter
    def steam_mods_folder_location(self, value: str) -> None:
        if self._steam_mods_folder_location != value:
            self._steam_mods_folder_location = value
            self.settings_changed.emit()

    @property
    def local_mods_folder_location(self) -> str:
        return self._local_mods_folder_location

    @local_mods_folder_location.setter
    def local_mods_folder_location(self, value: str) -> None:
        if self._local_mods_folder_location != value:
            self._local_mods_folder_location = value
            self.settings_changed.emit()

    @property
    def sorting_algorithm(self) -> "Settings.SortingAlgorithm":
        return self._sorting_algorithm

    @sorting_algorithm.setter
    def sorting_algorithm(self, value: "Settings.SortingAlgorithm") -> None:
        if self._sorting_algorithm != value:
            self._sorting_algorithm = value
            self.settings_changed.emit()

    @property
    def debug_logging(self) -> bool:
        return self._debug_logging

    @debug_logging.setter
    def debug_logging(self, value: bool) -> None:
        if self._debug_logging != value:
            self._debug_logging = value
            self.settings_changed.emit()

    def save(self) -> None:
        with open(str(self.settings_file_path), "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load(self) -> None:
        try:
            with open(str(self.settings_file_path), "r") as file:
                data = json.load(file)
                self.from_dict(data)
        except FileNotFoundError:
            self.save()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "game_location": self._game_location,
            "config_folder_location": self._config_folder_location,
            "steam_mods_folder_location": self._steam_mods_folder_location,
            "local_mods_folder_location": self._local_mods_folder_location,
            "sorting_algorithm": self._sorting_algorithm.name,
            "debug_logging": self._debug_logging,
        }

    def from_dict(self, data: Dict[str, str]) -> None:
        self.game_location = data.get("game_location", "")
        self.config_folder_location = data.get("config_folder_location", "")
        self.steam_mods_folder_location = data.get("steam_mods_folder_location", "")
        self.local_mods_folder_location = data.get("local_mods_folder_location", "")

        sorting_algorithm_str = data.get("sorting_algorithm", "ALPHABETICAL")
        self.sorting_algorithm = Settings.SortingAlgorithm[sorting_algorithm_str]

        self.debug_logging = bool(data.get("debug_logging", False))
