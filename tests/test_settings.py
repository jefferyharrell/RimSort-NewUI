import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import mock_open, patch

from models.settings import Settings
from utilities.app_info import AppInfo


class TestSettings(TestCase):
    def setUp(self) -> None:
        AppInfo(__file__)
        self.prefs = Settings()

    def test_apply_default_settings(self) -> None:
        self.prefs.game_location = Path("non-default value")
        self.prefs.config_folder_location = Path("non-default value")
        self.prefs.steam_mods_folder_location = Path("non-default value")
        self.prefs.local_mods_folder_location = Path("non-default value")
        self.prefs.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
        self.prefs.debug_logging = True
        self.prefs.apply_default_settings()
        self.assertEqual(self.prefs.game_location, None)
        self.assertEqual(self.prefs.config_folder_location, None)
        self.assertEqual(self.prefs.steam_mods_folder_location, None)
        self.assertEqual(self.prefs.local_mods_folder_location, None)
        self.assertEqual(
            self.prefs.sorting_algorithm, Settings.SortingAlgorithm.ALPHABETICAL
        )
        self.assertEqual(self.prefs.debug_logging, False)

    def test_game_folder(self) -> None:
        self.prefs.game_location = Path("test path")
        self.assertEqual(self.prefs.game_location, Path("test path"))

    def test_config_folder(self) -> None:
        self.prefs.config_folder_location = Path("test path")
        self.assertEqual(self.prefs.config_folder_location, Path("test path"))

    def test_steam_mods_folder(self) -> None:
        self.prefs.steam_mods_folder_location = Path("test path")
        self.assertEqual(self.prefs.steam_mods_folder_location, Path("test path"))

    def test_local_mods_folder(self) -> None:
        self.prefs.local_mods_folder_location = Path("test path")
        self.assertEqual(self.prefs.local_mods_folder_location, Path("test path"))

    def test_sorting_algorithm(self) -> None:
        self.prefs.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
        self.assertEqual(
            self.prefs.sorting_algorithm, Settings.SortingAlgorithm.TOPOLOGICAL
        )

    def test_debug_logging(self) -> None:
        self.prefs.debug_logging = True
        self.assertEqual(self.prefs.debug_logging, True)

    def test_save(self) -> None:
        m = mock_open()
        with patch("builtins.open", m):
            self.prefs.save()
        m.assert_called_once_with(str(self.prefs.settings_file), "w")

    def test_load(self) -> None:
        mock_data = {
            "game_location": "mock_game_location",
            "config_folder_location": "mock_config_folder_location",
            "steam_mods_folder_location": "mock_steam_mods_folder_location",
            "local_mods_folder_location": "mock_local_mods_folder_location",
            "sorting_algorithm": "ALPHABETICAL",
            "debug_logging": False,
        }
        m = mock_open(read_data=json.dumps(mock_data))
        with patch("builtins.open", m):
            self.prefs.load()
        m.assert_called_once_with(str(self.prefs.settings_file), "r")
        self.assertEqual(self.prefs.game_location, Path("mock_game_location").resolve())
        self.assertEqual(
            self.prefs.config_folder_location,
            Path("mock_config_folder_location").resolve(),
        )
        self.assertEqual(
            self.prefs.steam_mods_folder_location,
            Path("mock_steam_mods_folder_location").resolve(),
        )
        self.assertEqual(
            self.prefs.local_mods_folder_location,
            Path("mock_local_mods_folder_location").resolve(),
        )
        self.assertEqual(
            self.prefs.sorting_algorithm, Settings.SortingAlgorithm.ALPHABETICAL
        )
        self.assertEqual(self.prefs.debug_logging, False)
