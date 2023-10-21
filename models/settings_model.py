import json
from enum import Enum, unique, auto
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, Any

from PySide6.QtCore import QObject, Signal
from platformdirs import user_data_dir


class SettingsModel(QObject):
    @unique
    class SortingAlgorithm(Enum):
        NONE = auto()
        ALPHABETICAL = auto()
        TOPOLOGICAL = auto()
        RADIOLOGICAL = auto()

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        user_data_folder_location: Path = Path(user_data_dir("NewUI"))
        user_data_folder_location.mkdir(parents=True, exist_ok=True)
        self.settings_file_path: Path = Path(user_data_folder_location, "settings.json")

        self._game_location: str = str()
        self._config_folder_location: str = str()
        self._steam_mods_folder_location: str = str()
        self._local_mods_folder_location: str = str()

        self._sorting_algorithm: "SettingsModel.SortingAlgorithm" = (
            SettingsModel.SortingAlgorithm.NONE
        )

        self._debug_logging: bool = False

        self._apply_default_settings()

    def _apply_default_settings(self) -> None:
        self._game_location = ""
        self._config_folder_location = ""
        self._steam_mods_folder_location = ""
        self._local_mods_folder_location = ""

        self._sorting_algorithm = SettingsModel.SortingAlgorithm.ALPHABETICAL

        self._debug_logging = False

    def apply_default_settings(self) -> None:
        self._apply_default_settings()
        self.changed.emit()

    @property
    def game_location(self) -> str:
        return self._game_location

    @game_location.setter
    def game_location(self, value: str) -> None:
        if self._game_location != value:
            self._game_location = value
            self.changed.emit()

    @property
    def game_location_path(self) -> Path:
        return Path(self._game_location)

    @property
    def config_folder_location(self) -> str:
        return self._config_folder_location

    @config_folder_location.setter
    def config_folder_location(self, value: str) -> None:
        if self._config_folder_location != value:
            self._config_folder_location = value
            self.changed.emit()

    @property
    def config_folder_location_path(self) -> Path:
        return Path(self._config_folder_location)

    @property
    def steam_mods_folder_location(self) -> str:
        return self._steam_mods_folder_location

    @steam_mods_folder_location.setter
    def steam_mods_folder_location(self, value: str) -> None:
        if self._steam_mods_folder_location != value:
            self._steam_mods_folder_location = value
            self.changed.emit()

    @property
    def steam_mods_folder_location_path(self) -> Path:
        return Path(self._steam_mods_folder_location)

    @property
    def local_mods_folder_location(self) -> str:
        return self._local_mods_folder_location

    @local_mods_folder_location.setter
    def local_mods_folder_location(self, value: str) -> None:
        if self._local_mods_folder_location != value:
            self._local_mods_folder_location = value
            self.changed.emit()

    @property
    def local_mods_folder_location_path(self) -> Path:
        return Path(self._local_mods_folder_location)

    @property
    def sorting_algorithm(self) -> "SettingsModel.SortingAlgorithm":
        return self._sorting_algorithm

    @sorting_algorithm.setter
    def sorting_algorithm(self, value: "SettingsModel.SortingAlgorithm") -> None:
        if self._sorting_algorithm != value:
            self._sorting_algorithm = value
            self.changed.emit()

    @property
    def debug_logging(self) -> bool:
        return self._debug_logging

    @debug_logging.setter
    def debug_logging(self, value: bool) -> None:
        if self._debug_logging != value:
            self._debug_logging = value
            self.changed.emit()

    def save(self) -> None:
        with open(str(self.settings_file_path), "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load(self) -> None:
        try:
            with open(str(self.settings_file_path), "r") as file:
                data = json.load(file)
                self.from_dict(data)
        except (FileNotFoundError, JSONDecodeError):
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
        self._game_location = data.get("game_location", "")
        self._config_folder_location = data.get("config_folder_location", "")
        self._steam_mods_folder_location = data.get("steam_mods_folder_location", "")
        self._local_mods_folder_location = data.get("local_mods_folder_location", "")

        sorting_algorithm_str = data.get("sorting_algorithm", "ALPHABETICAL")
        self._sorting_algorithm = SettingsModel.SortingAlgorithm[sorting_algorithm_str]

        self._debug_logging = bool(data.get("debug_logging", False))
