from pathlib import Path
from typing import List

from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QApplication
from logger_tt import logger
from lxml import etree

from models.main_window_model import MainWindowModel
from models.settings_model import SettingsModel
from objects.mod import Mod
from views.about_dialog import AboutDialog
from views.main_window import MainWindow
from views.settings_dialog import SettingsDialog


class MainWindowController(QObject):
    def __init__(
        self,
        model: MainWindowModel,
        view: MainWindow,
        settings_model: SettingsModel,
        settings_dialog: SettingsDialog,
    ) -> None:
        super().__init__()

        self.main_window_model = model
        self.main_window = view
        self.settings_model = settings_model
        self.settings_dialog = settings_dialog

        self.about_dialog = AboutDialog()

        # Connect the signals
        self.main_window.about_action.triggered.connect(self._on_about_action_triggered)
        self.main_window.settings_action.triggered.connect(
            self._on_settings_action_triggered
        )
        self.main_window.exit_action.triggered.connect(self._on_exit_action_triggered)

        # Populate the models
        steam_mods_folder_location_path = Path(
            self.settings_model.steam_mods_folder_location
        )
        local_mods_folder_location_path = Path(
            self.settings_model.local_mods_folder_location
        )

        result_list = self._scan_folder_for_mods(steam_mods_folder_location_path)
        result_list += self._scan_folder_for_mods(local_mods_folder_location_path)
        result_list.sort(key=lambda x: x.name)

        for mod in result_list:
            self.main_window_model.inactive_mods_list_model.appendRow(mod)

        # Set up the proxy models
        self.main_window_model.inactive_mods_proxy_model.setSourceModel(
            self.main_window_model.inactive_mods_list_model
        )
        self.main_window_model.inactive_mods_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.main_window.inactive_mods_filter_field.textChanged.connect(
            self.update_inactive_mods_filter
        )

        self.main_window_model.active_mods_proxy_model.setSourceModel(
            self.main_window_model.active_mods_list_model
        )
        self.main_window_model.active_mods_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.main_window.active_mods_filter_field.textChanged.connect(
            self.update_active_mods_filter
        )

        # Connect the models to their views
        self.main_window.inactive_mods_list_view.setModel(
            self.main_window_model.inactive_mods_proxy_model
        )
        self.main_window.active_mods_list_view.setModel(
            self.main_window_model.active_mods_proxy_model
        )

    @Slot(str)
    def update_inactive_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.inactive_mods_proxy_model.setFilterFixedString(text)

    @Slot(str)
    def update_active_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.active_mods_proxy_model.setFilterFixedString(text)

    def _scan_folder_for_mods(self, folder_location_path: Path) -> List[Mod]:
        result_list = []
        for subfolder in folder_location_path.iterdir():
            if subfolder.is_dir():
                about_xml_path = subfolder / "About" / "About.xml"

                if about_xml_path.exists():
                    try:
                        # Parse the XML file using lxml
                        tree = etree.parse(str(about_xml_path))
                        root = tree.getroot()

                        node = root.find("./name")
                        name = node.text if node is not None else ""
                        node = root.find("./packageId")
                        package_id = node.text if node is not None else ""
                        supported_versions = root.xpath("./supportedVersions/li/text()")

                        if (
                            name is not None
                            and package_id is not None
                            and supported_versions is not None
                        ):
                            result_list.append(
                                Mod(name, package_id, supported_versions)
                            )
                    except (
                        etree.XMLSyntaxError
                    ):  # Catching XML parsing errors specific to lxml
                        logger.warning(f"Could not parse About.xml at {about_xml_path}")
        return result_list

    # region SLots

    @Slot()
    def _on_about_action_triggered(self) -> None:
        self.about_dialog.show()

    @Slot()
    def _on_settings_action_triggered(self) -> None:
        self.settings_dialog.exec()

    @Slot()
    def _on_exit_action_triggered(self) -> None:
        QApplication.quit()

    # endregion
