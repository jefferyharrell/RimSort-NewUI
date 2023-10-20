from pathlib import Path
from typing import List

from PySide6.QtCore import QObject, Slot, Qt, QModelIndex
from PySide6.QtGui import QPixmap
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

        self.main_window.inactive_mods_list_view.clicked.connect(
            self._on_mod_list_view_clicked
        )
        self.main_window.active_mods_list_view.clicked.connect(
            self._on_mod_list_view_clicked
        )

        # Populate the models
        steam_mods_folder_location_path = Path(
            self.settings_model.steam_mods_folder_location
        )
        local_mods_folder_location_path = Path(
            self.settings_model.local_mods_folder_location
        )

        result_list = self._scan_folder_for_mods(steam_mods_folder_location_path)
        result_list += self._scan_folder_for_mods(local_mods_folder_location_path)
        for mod in result_list:
            self.main_window_model.mods_dictionary[mod.id] = mod

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

    @Slot(QModelIndex)
    def _on_mod_list_view_clicked(self, index: QModelIndex) -> None:
        mod_uuid = index.data(Qt.ItemDataRole.UserRole)
        mod = self.main_window_model.mods_dictionary[mod_uuid]

        self.main_window.selected_mod_name_label.setText(mod.name)
        self.main_window.selected_mod_package_id_label.setText(str(mod.package_id))
        self.main_window.selected_mod_supported_versions_label.setText(
            ", ".join(mod.supported_versions)
        )
        if mod.preview_image_path.exists():
            desired_width = self.main_window.selected_mod_preview_image.width()
            pixmap = QPixmap(str(mod.preview_image_path)).scaledToWidth(
                desired_width, Qt.TransformationMode.SmoothTransformation
            )
            self.main_window.selected_mod_preview_image.setPixmap(pixmap)

    def _scan_folder_for_mods(self, folder_location_path: Path) -> List[Mod]:
        result_list: List[Mod] = []
        for subfolder in folder_location_path.iterdir():
            if subfolder.is_dir():
                about_xml_path = subfolder / "About" / "About.xml"

                name = ""
                package_id = ""
                supported_versions = []

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
                    except (
                        etree.XMLSyntaxError
                    ):  # Catching XML parsing errors specific to lxml
                        logger.warning(f"Could not parse About.xml at {about_xml_path}")

                    preview_image_path = subfolder / "About" / "Preview.png"

                    if name is not None:
                        result_list.append(
                            Mod(
                                name, package_id, supported_versions, preview_image_path
                            )
                        )

        return result_list

    # region Slots

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
