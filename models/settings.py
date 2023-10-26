import json
from enum import Enum, unique, auto
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, Any, Optional

from PySide6.QtCore import QObject, Signal

from utilities.app_info import AppInfo
from utilities.system_info import SystemInfo


class Settings(QObject):
    @unique
    class SortingAlgorithm(Enum):
        NONE = auto()
        ALPHABETICAL = auto()
        TOPOLOGICAL = auto()
        RADIOLOGICAL = auto()

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        AppInfo().user_data_folder.mkdir(parents=True, exist_ok=True)
        self.settings_file_path: Path = Path(
            AppInfo().user_data_folder, "settings.json"
        )

        self._game_location: Optional[Path] = None
        self._config_folder_location: Optional[Path] = None
        self._steam_mods_folder_location: Optional[Path] = None
        self._local_mods_folder_location: Optional[Path] = None

        self._sorting_algorithm: "Settings.SortingAlgorithm" = (
            Settings.SortingAlgorithm.NONE
        )

        self._debug_logging: bool = False

        self._game_data_location: str = ""

        self._apply_default_settings()

    def _apply_default_settings(self) -> None:
        self._game_location = None
        self._config_folder_location = None
        self._steam_mods_folder_location = None
        self._local_mods_folder_location = None

        self._sorting_algorithm = Settings.SortingAlgorithm.ALPHABETICAL

        self._debug_logging = False

    def apply_default_settings(self) -> None:
        self._apply_default_settings()
        self.changed.emit()

    @property
    def game_location(self) -> Optional[Path]:
        return self._game_location

    @game_location.setter
    def game_location(self, value: Optional[Path]) -> None:
        if self._game_location != value:
            self._game_location = value
            self.changed.emit()

    @property
    def config_folder_location(self) -> Optional[Path]:
        return self._config_folder_location

    @config_folder_location.setter
    def config_folder_location(self, value: Optional[Path]) -> None:
        if self._config_folder_location != value:
            self._config_folder_location = value
            self.changed.emit()

    @property
    def steam_mods_folder_location(self) -> Optional[Path]:
        return self._steam_mods_folder_location

    @steam_mods_folder_location.setter
    def steam_mods_folder_location(self, value: Optional[Path]) -> None:
        if self._steam_mods_folder_location != value:
            self._steam_mods_folder_location = value
            self.changed.emit()

    @property
    def local_mods_folder_location(self) -> Optional[Path]:
        return self._local_mods_folder_location

    @local_mods_folder_location.setter
    def local_mods_folder_location(self, value: Optional[Path]) -> None:
        if self._local_mods_folder_location != value:
            self._local_mods_folder_location = value
            self.changed.emit()

    @property
    def sorting_algorithm(self) -> "Settings.SortingAlgorithm":
        return self._sorting_algorithm

    @sorting_algorithm.setter
    def sorting_algorithm(self, value: "Settings.SortingAlgorithm") -> None:
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

    @property
    def game_data_location(self) -> Optional[Path]:
        if self.game_location is None:
            return None
        if SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            return self.game_location / "Data"
        else:
            return self.game_location.parent / "Data"

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
            "game_location": str(self._game_location) if self._game_location else "",
            "config_folder_location": str(self._config_folder_location)
            if self._config_folder_location
            else "",
            "steam_mods_folder_location": str(self._steam_mods_folder_location)
            if self._steam_mods_folder_location
            else "",
            "local_mods_folder_location": str(self._local_mods_folder_location)
            if self._local_mods_folder_location
            else "",
            "sorting_algorithm": self._sorting_algorithm.name,
            "debug_logging": self._debug_logging,
        }

    def from_dict(self, data: Dict[str, str]) -> None:
        if data.get("game_location") != "":
            self._game_location = Path(data["game_location"]).resolve()
        else:
            self._game_location = None

        if data.get("config_folder_location") != "":
            self._config_folder_location = Path(
                data["config_folder_location"]
            ).resolve()
        else:
            self._config_folder_location = None

        if data.get("steam_mods_folder_location") != "":
            self._steam_mods_folder_location = Path(
                data["steam_mods_folder_location"]
            ).resolve()
        else:
            self._steam_mods_folder_location = None

        if data.get("local_mods_folder_location") != "":
            self._local_mods_folder_location = Path(
                data["local_mods_folder_location"]
            ).resolve()
        else:
            self._local_mods_folder_location = None

        sorting_algorithm_str = data.get("sorting_algorithm", "ALPHABETICAL")
        self._sorting_algorithm = Settings.SortingAlgorithm[sorting_algorithm_str]

        self._debug_logging = bool(data.get("debug_logging", False))
