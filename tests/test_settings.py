import json
from pathlib import Path
from unittest import TestCase
from unittest.mock import mock_open, patch

from models.settings import Settings
from utilities.app_info import AppInfo


class TestSettings(TestCase):
    def setUp(self) -> None:
        AppInfo(__file__)
        self.settings = Settings()

    def test_apply_default_settings(self) -> None:
        self.settings.game_location = Path("non-default value")
        self.settings.config_folder_location = Path("non-default value")
        self.settings.steam_mods_folder_location = Path("non-default value")
        self.settings.local_mods_folder_location = Path("non-default value")
        self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
        self.settings.debug_logging = True
        self.settings.apply_default_settings()
        self.assertEqual(self.settings.game_location, None)
        self.assertEqual(self.settings.config_folder_location, None)
        self.assertEqual(self.settings.steam_mods_folder_location, None)
        self.assertEqual(self.settings.local_mods_folder_location, None)
        self.assertEqual(
            self.settings.sorting_algorithm, Settings.SortingAlgorithm.ALPHABETICAL
        )
        self.assertEqual(self.settings.debug_logging, False)

    def test_game_folder(self) -> None:
        self.settings.game_location = Path("test path")
        self.assertEqual(self.settings.game_location, Path("test path"))

    def test_config_folder(self) -> None:
        self.settings.config_folder_location = Path("test path")
        self.assertEqual(self.settings.config_folder_location, Path("test path"))

    def test_steam_mods_folder(self) -> None:
        self.settings.steam_mods_folder_location = Path("test path")
        self.assertEqual(self.settings.steam_mods_folder_location, Path("test path"))

    def test_local_mods_folder(self) -> None:
        self.settings.local_mods_folder_location = Path("test path")
        self.assertEqual(self.settings.local_mods_folder_location, Path("test path"))

    def test_sorting_algorithm(self) -> None:
        self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
        self.assertEqual(
            self.settings.sorting_algorithm, Settings.SortingAlgorithm.TOPOLOGICAL
        )

    def test_debug_logging(self) -> None:
        self.settings.debug_logging = True
        self.assertEqual(self.settings.debug_logging, True)

    def test_save(self) -> None:
        m = mock_open()
        with patch("builtins.open", m):
            self.settings.save()
        m.assert_called_once_with(str(self.settings.settings_file), "w")

    def test_load(self) -> None:
        mock_data = {
            "game_location": "/mock_game_location",
            "config_folder_location": "/mock_config_folder_location",
            "steam_mods_folder_location": "/mock_steam_mods_folder_location",
            "local_mods_folder_location": "/mock_local_mods_folder_location",
            "sorting_algorithm": "ALPHABETICAL",
            "debug_logging": False,
        }
        m = mock_open(read_data=json.dumps(mock_data))
        with patch("builtins.open", m):
            self.settings.load()
        m.assert_called_once_with(str(self.settings.settings_file), "r")
        self.assertEqual(self.settings.game_location, Path("/mock_game_location"))
        self.assertEqual(
            self.settings.config_folder_location,
            Path("/mock_config_folder_location"),
        )
        self.assertEqual(
            self.settings.steam_mods_folder_location,
            Path("/mock_steam_mods_folder_location"),
        )
        self.assertEqual(
            self.settings.local_mods_folder_location,
            Path("/mock_local_mods_folder_location"),
        )
        self.assertEqual(
            self.settings.sorting_algorithm, Settings.SortingAlgorithm.ALPHABETICAL
        )
        self.assertEqual(self.settings.debug_logging, False)
