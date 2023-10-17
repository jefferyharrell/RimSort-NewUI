import json
from enum import Enum, unique, auto
from typing import Dict


class Preferences:
    @unique
    class SortingAlgorithm(Enum):
        ALPHABETICAL = auto()
        TOPOLOGICAL = auto()

    def __init__(self) -> None:
        super().__init__()

        self._game_folder: str = ""
        self._config_folder: str = ""
        self._steam_mods_folder: str = ""
        self._local_mods_folder: str = ""

        self._sorting_algorithm: "Preferences.SortingAlgorithm" = (
            Preferences.SortingAlgorithm.ALPHABETICAL
        )

    @property
    def game_folder(self) -> str:
        return self._game_folder

    @game_folder.setter
    def game_folder(self, value: str) -> None:
        self._game_folder = value

    @property
    def config_folder(self) -> str:
        return self._config_folder

    @config_folder.setter
    def config_folder(self, value: str) -> None:
        self._config_folder = value

    @property
    def steam_mods_folder(self) -> str:
        return self._steam_mods_folder

    @steam_mods_folder.setter
    def steam_mods_folder(self, value: str) -> None:
        self._steam_mods_folder = value

    @property
    def local_mods_folder(self) -> str:
        return self._local_mods_folder

    @local_mods_folder.setter
    def local_mods_folder(self, value: str) -> None:
        self._local_mods_folder = value

    @property
    def sorting_algorithm(self) -> "Preferences.SortingAlgorithm":
        return self._sorting_algorithm

    @sorting_algorithm.setter
    def sorting_algorithm(self, value: "Preferences.SortingAlgorithm") -> None:
        self._sorting_algorithm = value

    def save(self) -> None:
        with open("preferences.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def load(self) -> None:
        with open("preferences.json", "r") as file:
            data = json.load(file)
            self.from_dict(data)

    def to_dict(self) -> Dict[str, str]:
        return {
            "game_folder": self._game_folder,
            "config_folder": self._config_folder,
            "steam_mods_folder": self._steam_mods_folder,
            "local_mods_folder": self._local_mods_folder,
            "sorting_algorithm": self._sorting_algorithm.name,
        }

    def from_dict(self, data: Dict[str, str]) -> None:
        self._game_folder = data["game_folder"]
        self._config_folder = data["config_folder"]
        self._steam_mods_folder = data["steam_mods_folder"]
        self._local_mods_folder = data["local_mods_folder"]
        self._sorting_algorithm = Preferences.SortingAlgorithm[
            data["sorting_algorithm"]
        ]
