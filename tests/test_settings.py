import json
from unittest import TestCase
from unittest.mock import mock_open, patch

from models.settings import Settings


class TestSettings(TestCase):
    def setUp(self) -> None:
        self.prefs = Settings()

    def test_game_folder(self) -> None:
        self.prefs.game_location = "test_path"
        self.assertEqual(self.prefs.game_location, "test_path")

    def test_config_folder(self) -> None:
        self.prefs.config_folder_location = "test_path"
        self.assertEqual(self.prefs.config_folder_location, "test_path")

    def test_steam_mods_folder(self) -> None:
        self.prefs.steam_mods_folder_location = "test_path"
        self.assertEqual(self.prefs.steam_mods_folder_location, "test_path")

    def test_local_mods_folder(self) -> None:
        self.prefs.local_mods_folder_location = "test_path"
        self.assertEqual(self.prefs.local_mods_folder_location, "test_path")

    def test_sorting_algorithm(self) -> None:
        self.prefs.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
        self.assertEqual(
            self.prefs.sorting_algorithm, Settings.SortingAlgorithm.TOPOLOGICAL
        )

    def test_save(self) -> None:
        m = mock_open()
        with patch("builtins.open", m):
            self.prefs.save()
        m.assert_called_once_with(str(self.prefs.settings_file_path), "w")

    def test_load(self) -> None:
        mock_data = {
            "game_location": "mock_game_location",
            "config_folder_location": "mock_config_folder_location",
            "steam_mods_folder_location": "mock_steam_mods_folder_location",
            "local_mods_folder_location": "mock_local_mods_folder_location",
            "sorting_algorithm": "ALPHABETICAL",
        }
        m = mock_open(read_data=json.dumps(mock_data))
        with patch("builtins.open", m):
            self.prefs.load()
        m.assert_called_once_with(str(self.prefs.settings_file_path), "r")
        self.assertEqual(self.prefs.game_location, "mock_game_location")
