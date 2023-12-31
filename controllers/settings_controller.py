from pathlib import Path

from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication

from models.settings import Settings
from utilities.event_bus import EventBus
from utilities.system_info import SystemInfo
from views.settings_dialog import SettingsDialog


class SettingsController(QObject):
    def __init__(self, model: Settings, view: SettingsDialog) -> None:
        super().__init__()

        self.settings = model
        self.settings_dialog = view

        self.user_home_path: Path = Path.home()

        self._connect_signals()

        self.settings.load()
        self._update_view_from_model()

    def show_settings_dialog(self) -> None:
        self.settings_dialog.exec()

    @Slot()
    def _on_settings_changed(self) -> None:
        self._update_view_from_model()

    @Slot()
    def _on_global_reset_to_defaults_button_clicked(self) -> None:
        message_box = QMessageBox(self.settings_dialog)
        message_box.setWindowTitle("Reset to defaults")
        message_box.setText(
            "Are you sure you want to reset all settings to their default values?"
        )
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        message_box.setDefaultButton(QMessageBox.StandardButton.No)
        message_box.setWindowModality(Qt.WindowModality.WindowModal)

        pressed_button = message_box.exec()
        if pressed_button == QMessageBox.StandardButton.No:
            return

        self.settings.apply_default_settings()

    @Slot()
    def _on_global_cancel_button_clicked(self) -> None:
        self.settings_dialog.close()

    @Slot()
    def _on_global_ok_button_clicked(self) -> None:
        self.settings.save()
        self.settings_dialog.close()

    @Slot()
    def _on_choose_game_location(self) -> None:
        game_location, _ = QFileDialog.getOpenFileName(
            parent=self.settings_dialog,
            dir=str(self.user_home_path),
        )
        if game_location != "":
            self.settings.game_location = Path(game_location).resolve()

    @Slot()
    def _on_choose_config_folder_location(self) -> None:
        config_folder_location = QFileDialog.getExistingDirectory(
            parent=self.settings_dialog,
            dir=str(self.user_home_path),
        )
        if config_folder_location != "":
            self.settings.config_folder_location = Path(
                config_folder_location
            ).resolve()

    @Slot()
    def _on_choose_steam_mods_folder_location(self) -> None:
        steam_mods_folder_location = QFileDialog.getExistingDirectory(
            parent=self.settings_dialog,
            dir=str(self.user_home_path),
        )
        if steam_mods_folder_location != "":
            self.settings.steam_mods_folder_location = Path(
                steam_mods_folder_location
            ).resolve()

    @Slot()
    def _on_choose_local_mods_folder_location(self) -> None:
        local_mods_folder_location = QFileDialog.getExistingDirectory(
            parent=self.settings_dialog,
            dir=str(self.user_home_path),
        )
        if local_mods_folder_location != "":
            self.settings.local_mods_folder_location = Path(
                local_mods_folder_location
            ).resolve()

    @Slot()
    def _on_locations_autodetect_button_clicked(self) -> None:
        if (
            self.settings_dialog.game_location.text() != ""
            or self.settings_dialog.config_folder_location.text() != ""
            or self.settings_dialog.steam_mods_folder_location.text() != ""
            or self.settings_dialog.local_mods_folder_location.text() != ""
        ):
            message_box = QMessageBox(self.settings_dialog)
            message_box.setWindowTitle("Autodetect locations")
            message_box.setText("Are you sure you want to autodetect all locations?")
            message_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            message_box.setDefaultButton(QMessageBox.StandardButton.No)
            message_box.setWindowModality(Qt.WindowModality.WindowModal)

            pressed_button = message_box.exec()
            if pressed_button == QMessageBox.StandardButton.No:
                return

        if SystemInfo().operating_system == SystemInfo.OperatingSystem.WINDOWS:
            self._autodetect_locations_windows()
        elif SystemInfo().operating_system == SystemInfo.OperatingSystem.LINUX:
            self._autodetect_locations_linux()
        elif SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            self._autodetect_locations_macos()

    @Slot()
    def _on_locations_clear_button_clicked(self) -> None:
        message_box = QMessageBox(self.settings_dialog)
        message_box.setWindowTitle("Clear all locations")
        message_box.setText("Are you sure you want to clear all locations?")
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        message_box.setDefaultButton(QMessageBox.StandardButton.No)
        message_box.setWindowModality(Qt.WindowModality.WindowModal)

        pressed_button = message_box.exec()
        if pressed_button == QMessageBox.StandardButton.No:
            return

        self.settings.game_location = None
        self.settings.config_folder_location = None
        self.settings.steam_mods_folder_location = None
        self.settings.local_mods_folder_location = None

    @Slot()
    def _on_community_rules_db_radio_clicked(self, checked: bool) -> None:
        if (
            self.sender() == self.settings_dialog.community_rules_db_none_radio
            and checked
        ):
            self.settings_dialog.community_rules_db_github_url.setEnabled(False)
            self.settings_dialog.community_rules_db_local_file.setEnabled(False)
            self.settings_dialog.community_rules_db_local_file_choose_button.setEnabled(
                False
            )
            app_instance = QApplication.instance()
            if isinstance(app_instance, QApplication):
                focused_widget = app_instance.focusWidget()
                if focused_widget:
                    focused_widget.clearFocus()
            return

        if (
            self.sender() == self.settings_dialog.community_rules_db_github_radio
            and checked
        ):
            self.settings_dialog.community_rules_db_github_url.setEnabled(True)
            self.settings_dialog.community_rules_db_local_file.setEnabled(False)
            self.settings_dialog.community_rules_db_local_file_choose_button.setEnabled(
                False
            )
            self.settings_dialog.community_rules_db_github_url.setFocus()
            return

        if (
            self.sender() == self.settings_dialog.community_rules_db_local_file_radio
            and checked
        ):
            self.settings_dialog.community_rules_db_github_url.setEnabled(False)
            self.settings_dialog.community_rules_db_local_file.setEnabled(True)
            self.settings_dialog.community_rules_db_local_file_choose_button.setEnabled(
                True
            )
            self.settings_dialog.community_rules_db_local_file.setFocus()
            return

    @Slot()
    def _on_community_rules_db_local_file_choose_button_clicked(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            parent=self.settings_dialog,
            dir=str(self.user_home_path),
        )
        if file_name != "":
            self.settings_dialog.community_rules_db_local_file.setText(file_name)

    @Slot()
    def _on_steam_workshop_db_radio_clicked(self, checked: bool) -> None:
        if (
            self.sender() == self.settings_dialog.steam_workshop_db_none_radio
            and checked
        ):
            self.settings_dialog.steam_workshop_db_github_url.setEnabled(False)
            self.settings_dialog.steam_workshop_db_local_file.setEnabled(False)
            self.settings_dialog.steam_workshop_db_local_file_choose_button.setEnabled(
                False
            )
            app_instance = QApplication.instance()
            if isinstance(app_instance, QApplication):
                focused_widget = app_instance.focusWidget()
                if focused_widget:
                    focused_widget.clearFocus()
            return

        if (
            self.sender() == self.settings_dialog.steam_workshop_db_github_radio
            and checked
        ):
            self.settings_dialog.steam_workshop_db_github_url.setEnabled(True)
            self.settings_dialog.steam_workshop_db_local_file.setEnabled(False)
            self.settings_dialog.steam_mods_folder_location_choose_button.setEnabled(
                False
            )
            self.settings_dialog.steam_workshop_db_github_url.setFocus()
            return

        if (
            self.sender() == self.settings_dialog.steam_workshop_db_local_file_radio
            and checked
        ):
            self.settings_dialog.steam_workshop_db_github_url.setEnabled(False)
            self.settings_dialog.steam_workshop_db_local_file.setEnabled(True)
            self.settings_dialog.steam_workshop_db_local_file_choose_button.setEnabled(
                True
            )
            self.settings_dialog.steam_workshop_db_local_file.setFocus()
            return

    @Slot()
    def _on_sorting_algorithm_button_toggled(self, checked: bool) -> None:
        if checked:
            if self.sender() == self.settings_dialog.alphabetical_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.ALPHABETICAL
            elif self.sender() == self.settings_dialog.topological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
            elif self.sender() == self.settings_dialog.radiological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.RADIOLOGICAL

    @Slot()
    def _on_debug_logging_button_toggled(self, checked: bool) -> None:
        if checked:
            self.settings.debug_logging = True
        else:
            self.settings.debug_logging = False

    def _connect_signals(self) -> None:
        EventBus().menu_bar_settings_triggered.connect(self.settings_dialog.exec)

        # Global buttons
        self.settings_dialog.global_reset_to_defaults_button.clicked.connect(
            self._on_global_reset_to_defaults_button_clicked
        )
        self.settings_dialog.global_cancel_button.clicked.connect(
            self._on_global_cancel_button_clicked
        )
        self.settings_dialog.global_ok_button.clicked.connect(
            self._on_global_ok_button_clicked
        )

        # Locations tab
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
        self.settings_dialog.locations_clear_button.clicked.connect(
            self._on_locations_clear_button_clicked
        )
        self.settings_dialog.locations_autodetect_button.clicked.connect(
            self._on_locations_autodetect_button_clicked
        )

        # Databases tab
        self.settings_dialog.community_rules_db_none_radio.clicked.connect(
            self._on_community_rules_db_radio_clicked
        )
        self.settings_dialog.community_rules_db_github_radio.clicked.connect(
            self._on_community_rules_db_radio_clicked
        )
        self.settings_dialog.community_rules_db_local_file_radio.clicked.connect(
            self._on_community_rules_db_radio_clicked
        )
        self.settings_dialog.community_rules_db_local_file_choose_button.clicked.connect(
            self._on_community_rules_db_local_file_choose_button_clicked
        )
        self.settings_dialog.steam_workshop_db_none_radio.clicked.connect(
            self._on_steam_workshop_db_radio_clicked
        )
        self.settings_dialog.steam_workshop_db_github_radio.clicked.connect(
            self._on_steam_workshop_db_radio_clicked
        )
        self.settings_dialog.steam_workshop_db_local_file_radio.clicked.connect(
            self._on_steam_workshop_db_radio_clicked
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

        self.settings.changed.connect(self._on_settings_changed)

    def _update_view_from_model(self) -> None:
        # Locations tab
        self.settings_dialog.game_location.setText(
            str(self.settings.game_location)
            if self.settings.game_location is not None
            else ""
        )
        self.settings_dialog.config_folder_location.setText(
            str(self.settings.config_folder_location)
            if self.settings.config_folder_location is not None
            else ""
        )
        self.settings_dialog.steam_mods_folder_location.setText(
            str(self.settings.steam_mods_folder_location)
            if self.settings.steam_mods_folder_location is not None
            else ""
        )
        self.settings_dialog.local_mods_folder_location.setText(
            str(self.settings.local_mods_folder_location)
            if self.settings.local_mods_folder_location is not None
            else ""
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
        else:
            self.settings_dialog.debug_logging_checkbox.setChecked(False)

    def _autodetect_locations_windows(self) -> None:
        self.settings.game_location = None
        self.settings.config_folder_location = None
        self.settings.steam_mods_folder_location = None
        self.settings.local_mods_folder_location = None

    def _autodetect_locations_linux(self) -> None:
        self.settings.game_location = None
        self.settings.config_folder_location = None
        self.settings.steam_mods_folder_location = None
        self.settings.local_mods_folder_location = None

    def _autodetect_locations_macos(self) -> None:
        self.settings.game_location = None
        self.settings.config_folder_location = None
        self.settings.steam_mods_folder_location = None
        self.settings.local_mods_folder_location = None

        home_folder_path: Path = Path.home()
        steam_folder_candidate_path: Path = (
            home_folder_path / "Library/Application Support/Steam"
        )
        app_support_candidate_path: Path = Path.home() / "Library/Application Support"

        game_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/common/RimWorld/RimWorldMac.app"
        )
        if game_location_candidate.exists():
            self.settings.game_location = game_location_candidate

        config_folder_location_candidate: Path = (
            app_support_candidate_path / "RimWorld/Config"
        )
        if config_folder_location_candidate.exists():
            self.settings.config_folder_location = config_folder_location_candidate

        steam_mods_folder_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/workshop/content/294100"
        )
        if steam_mods_folder_location_candidate.exists():
            self.settings.steam_mods_folder_location = (
                steam_mods_folder_location_candidate
            )

        local_mods_folder_location_candidate: Path = game_location_candidate / "Mods"
        if local_mods_folder_location_candidate.exists():
            self.settings.local_mods_folder_location = (
                local_mods_folder_location_candidate
            )
