from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from models.settings import Settings
from utilities.system_info import SystemInfo
from views.settings_dialog import SettingsDialog


class SettingsDialogController(QObject):
    def __init__(self, model: Settings, view: SettingsDialog) -> None:
        super().__init__()

        self.settings = model
        self.settings_dialog = view
        self.settings_dialog.global_cancel_button.clicked.connect(
            self.settings_dialog.close
        )
        self.settings_dialog.global_apply_button.clicked.connect(
            self._on_global_apply_button_clicked
        )

        # General tab
        self.settings_dialog.game_location_choose_button.clicked.connect(
            self._on_choose_game_location
        )
        self.settings_dialog.config_folder_location_choose_button.clicked.connect(
            self._on_choose_config_folder_location
        )
        self.settings_dialog.steam_mods_folder_location_choose_button.clicked.connect(
            self._on_choose_steam_mods_folder_location
        )
        self.settings_dialog.local_mods_folder_location_choose_button.clicked.connect(
            self._on_choose_local_mods_folder_location
        )
        self.settings_dialog.general_clear_button.clicked.connect(
            self._on_general_clear_button_clicked
        )
        self.settings_dialog.general_autodetect_button.clicked.connect(
            self._on_general_autodetect_button_clicked
        )

        # Sorting tab
        self.settings_dialog.alphabetical_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        self.settings_dialog.topological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        self.settings_dialog.radiological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )

        # Advanced tab
        self.settings_dialog.debug_logging_checkbox.toggled.connect(
            self._on_debug_logging_button_toggled
        )

        self.settings.settings_changed.connect(self._on_settings_changed)
        self.settings.load()

    def _on_settings_changed(self) -> None:
        # General tab
        self.settings_dialog.game_location_value_label.setText(
            self.settings.game_location
        )
        self.settings_dialog.config_folder_location_value_label.setText(
            self.settings.config_folder_location
        )
        self.settings_dialog.steam_mods_folder_location_value_label.setText(
            self.settings.steam_mods_folder_location
        )
        self.settings_dialog.local_mods_folder_location_value_label.setText(
            self.settings.local_mods_folder_location
        )

        # Sorting tab
        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.settings_dialog.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.settings_dialog.topological_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.RADIOLOGICAL:
            self.settings_dialog.radiological_button.setChecked(True)

        # Advanced tab
        if self.settings.debug_logging:
            self.settings_dialog.debug_logging_checkbox.setChecked(True)

    def _on_global_apply_button_clicked(self) -> None:
        self.settings.save()
        self.settings_dialog.close()

    def _on_choose_game_location(self) -> None:
        game_location, _ = QFileDialog.getOpenFileName(self.settings_dialog)
        if game_location != "":
            self.settings.game_location = game_location

    def _on_choose_config_folder_location(self) -> None:
        config_folder_location = QFileDialog.getExistingDirectory(self.settings_dialog)
        if config_folder_location != "":
            self.settings.config_folder_location = config_folder_location

    def _on_choose_steam_mods_folder_location(self) -> None:
        steam_mods_folder_location = QFileDialog.getExistingDirectory(
            self.settings_dialog
        )
        if steam_mods_folder_location != "":
            self.settings.steam_mods_folder_location = steam_mods_folder_location

    def _on_choose_local_mods_folder_location(self) -> None:
        local_mods_folder_location = QFileDialog.getExistingDirectory(
            self.settings_dialog
        )
        if local_mods_folder_location != "":
            self.settings.local_mods_folder_location = local_mods_folder_location

    def _on_general_autodetect_button_clicked(self) -> None:
        if SystemInfo.operating_system() == SystemInfo.OperatingSystem.WINDOWS:
            self._autodetect_locations_windows()
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.LINUX:
            self._autodetect_locations_linux()
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.MACOS:
            self._autodetect_locations_macos()

    def _autodetect_locations_windows(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

    def _autodetect_locations_linux(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

    def _autodetect_locations_macos(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

        home_folder_path: Path = Path.home()
        steam_folder_candidate_path: Path = (
            home_folder_path / "Library/Application Support/Steam"
        )
        app_support_candidate_path: Path = Path.home() / "Library/Application Support"

        game_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/common/RimWorld/RimWorldMac.app"
        )
        if game_location_candidate.exists():
            self.settings.game_location = str(game_location_candidate)

        config_folder_location_candidate: Path = (
            app_support_candidate_path / "RimWorld/Config"
        )
        if config_folder_location_candidate.exists():
            self.settings.config_folder_location = str(config_folder_location_candidate)

        steam_mods_folder_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/workshop/content/294100"
        )
        if steam_mods_folder_location_candidate.exists():
            self.settings.steam_mods_folder_location = str(
                steam_mods_folder_location_candidate
            )

        local_mods_folder_location_candidate: Path = game_location_candidate / "Mods"
        if local_mods_folder_location_candidate.exists():
            self.settings.local_mods_folder_location = str(
                local_mods_folder_location_candidate
            )

    def _on_general_clear_button_clicked(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

    def _on_sorting_algorithm_button_toggled(self, checked: bool) -> None:
        if checked:
            if self.sender() == self.settings_dialog.alphabetical_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.ALPHABETICAL
            elif self.sender() == self.settings_dialog.topological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
            elif self.sender() == self.settings_dialog.radiological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.RADIOLOGICAL

    def _on_debug_logging_button_toggled(self, checked: bool) -> None:
        if checked:
            self.settings.debug_logging = True
        else:
            self.settings.debug_logging = False
