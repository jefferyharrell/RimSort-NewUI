import json
from unittest import TestCase
from unittest.mock import mock_open, patch

from models.preferences import Preferences


class TestPreferences(TestCase):
    def setUp(self) -> None:
        self.prefs = Preferences()

    def test_game_folder(self) -> None:
        self.prefs.game_folder = "test_path"
        self.assertEqual(self.prefs.game_folder, "test_path")

    def test_config_folder(self) -> None:
        self.prefs.config_folder = "test_path"
        self.assertEqual(self.prefs.config_folder, "test_path")

    def test_steam_mods_folder(self) -> None:
        self.prefs.steam_mods_folder = "test_path"
        self.assertEqual(self.prefs.steam_mods_folder, "test_path")

    def test_local_mods_folder(self) -> None:
        self.prefs.local_mods_folder = "test_path"
        self.assertEqual(self.prefs.local_mods_folder, "test_path")

    def test_sorting_algorithm(self) -> None:
        self.prefs.sorting_algorithm = Preferences.SortingAlgorithm.TOPOLOGICAL
        self.assertEqual(
            self.prefs.sorting_algorithm, Preferences.SortingAlgorithm.TOPOLOGICAL
        )

    def test_save(self) -> None:
        m = mock_open()
        with patch("builtins.open", m):
            self.prefs.save()
        m.assert_called_once_with("preferences.json", "w")

    def test_load(self) -> None:
        mock_data = {
            "game_folder": "mock_game_folder",
            "config_folder": "mock_config_folder",
            "steam_mods_folder": "mock_steam_mods_folder",
            "local_mods_folder": "mock_local_mods_folder",
            "sorting_algorithm": "ALPHABETICAL",
        }
        m = mock_open(read_data=json.dumps(mock_data))
        with patch("builtins.open", m):
            self.prefs.load()
        m.assert_called_once_with("preferences.json", "r")
        self.assertEqual(self.prefs.game_folder, "mock_game_folder")
