from typing import cast

from PySide6.QtCore import (
    QObject,
    Slot,
    Qt,
    QModelIndex,
    QSortFilterProxyModel,
    QThreadPool,
    QItemSelection,
    QItemSelectionModel,
)
from PySide6.QtGui import QPixmap, QStandardItemModel
from PySide6.QtWidgets import QListView

from controllers.settings_dialog_controller import SettingsDialogController
from models.main_window_model import MainWindowModel
from objects.mod import Mod
from views.about_dialog import AboutDialog
from views.main_window import MainWindow
from runners.load_mods_from_folders_runner import LoadModsFromFoldersRunner


class MainWindowController(QObject):
    def __init__(
        self,
        model: MainWindowModel,
        view: MainWindow,
        settings_dialog_controller: SettingsDialogController,
    ) -> None:
        super().__init__()

        self.main_window_model = model
        self.main_window = view
        self.settings_dialog_controller = settings_dialog_controller

        self.about_dialog = AboutDialog()

        # Connect the main window's signals
        self.main_window.inactive_mods_list_view.clicked.connect(
            self._on_mod_list_view_clicked
        )
        self.main_window.active_mods_list_view.clicked.connect(
            self._on_mod_list_view_clicked
        )

        self.main_window.inactive_mods_list_view.doubleClicked.connect(
            self._on_mod_list_view_double_clicked
        )
        self.main_window.active_mods_list_view.doubleClicked.connect(
            self._on_mod_list_view_double_clicked
        )

        # Set up the proxy models
        self.main_window_model.inactive_mods_proxy_model.setSourceModel(
            self.main_window_model.inactive_mods_list_model
        )
        self.main_window_model.inactive_mods_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.main_window.inactive_mods_filter_field.textChanged.connect(
            self._update_inactive_mods_filter
        )

        self.main_window_model.active_mods_proxy_model.setSourceModel(
            self.main_window_model.active_mods_list_model
        )
        self.main_window_model.active_mods_proxy_model.setFilterCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )
        self.main_window.active_mods_filter_field.textChanged.connect(
            self._update_active_mods_filter
        )

        # Connect the models to their views
        self.main_window.inactive_mods_list_view.setModel(
            self.main_window_model.inactive_mods_proxy_model
        )
        self.main_window.active_mods_list_view.setModel(
            self.main_window_model.active_mods_proxy_model
        )

        self.main_window.inactive_mods_list_view.selectionModel().selectionChanged.connect(
            self._on_mods_list_view_selection_changed
        )
        self.main_window.active_mods_list_view.selectionModel().selectionChanged.connect(
            self._on_mods_list_view_selection_changed
        )

        # Populate the models
        self._refresh_inactive_mods_list()

    def _refresh_inactive_mods_list(self) -> None:
        self.runner = LoadModsFromFoldersRunner(
            [
                self.settings_dialog_controller.settings_model.steam_mods_folder_location_path,
                self.settings_dialog_controller.settings_model.local_mods_folder_location_path,
            ]
        )
        self.runner.signals.data_ready.connect(self._on_runner_data_ready)
        pool = QThreadPool.globalInstance()
        pool.start(self.runner)

    @Slot(object)
    def _on_runner_data_ready(self, data: object) -> None:
        if not isinstance(data, list) or not all(
            isinstance(item, Mod) for item in data
        ):
            raise TypeError("Expected a list of Mod objects")

        self.main_window_model.mods_dictionary = {}
        self.main_window_model.inactive_mods_list_model.clear()

        for mod in data:
            self.main_window_model.mods_dictionary[mod.id] = mod
            self.main_window_model.inactive_mods_list_model.appendRow(mod)
            self.main_window_model.inactive_mods_proxy_model.sort(0)

    @Slot(str)
    def _update_inactive_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.inactive_mods_proxy_model.setFilterFixedString(text)

    @Slot(str)
    def _update_active_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.active_mods_proxy_model.setFilterFixedString(text)

    @Slot(QModelIndex)
    def _on_mod_list_view_clicked(self, index: QModelIndex) -> None:
        sender_object = self.sender()
        if not isinstance(sender_object, QListView):
            raise TypeError(
                f"Expected sender of type QListView, but got {type(sender_object)}"
            )

        if not sender_object.selectionModel().isSelected(index):
            return
        self._show_selected_mod_info_by_index(index)

    @Slot(QModelIndex)
    def _on_mod_list_view_double_clicked(self, index: QModelIndex) -> None:
        sender_obj = self.sender()
        if not isinstance(sender_obj, QListView):
            raise TypeError(
                f"Expected sender of type QListView, but got {type(sender_obj)}"
            )

        source_list_view = sender_obj
        target_list_view = (
            self.main_window.active_mods_list_view
            if source_list_view == self.main_window.inactive_mods_list_view
            else self.main_window.inactive_mods_list_view
        )

        self._move_mod_to_list_view(index, source_list_view, target_list_view)

    @Slot(QItemSelection, QItemSelection)
    def _on_mods_list_view_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        sender_object = self.sender()
        if not isinstance(sender_object, QItemSelectionModel):
            raise TypeError(
                f"Expected sender of type QListView, but got {type(sender_object)}"
            )

        if deselected.count() != 0:
            selected_indexes = sender_object.selectedIndexes()
            if selected_indexes:
                self._show_selected_mod_info_by_index(selected_indexes[-1])
            else:
                self._clear_selected_mod_info()

    def _show_selected_mod_info_by_index(self, index: QModelIndex) -> None:
        mod_uuid = index.data(Qt.ItemDataRole.UserRole)
        mod = self.main_window_model.mods_dictionary[mod_uuid]
        if mod.preview_image_path.exists():
            desired_width = self.main_window.selected_mod_preview_image.width()
            pixmap = QPixmap(str(mod.preview_image_path)).scaledToWidth(
                desired_width, Qt.TransformationMode.SmoothTransformation
            )
            self.main_window.selected_mod_preview_image.setPixmap(pixmap)
        self.main_window.selected_mod_name_label.setText(mod.name)
        self.main_window.selected_mod_package_id_label.setText(str(mod.package_id))
        self.main_window.selected_mod_supported_versions_label.setText(
            ", ".join(mod.supported_versions)
        )
        if mod.description != "":
            self.main_window.selected_mod_description.show()
        else:
            self.main_window.selected_mod_description.hide()
        self.main_window.selected_mod_description.setText(mod.description)
        height = self.main_window.selected_mod_description.document().size().height()
        self.main_window.selected_mod_description.setFixedHeight(int(height))

    def _clear_selected_mod_info(self) -> None:
        self.main_window.selected_mod_preview_image.setPixmap(QPixmap())
        self.main_window.selected_mod_name_label.setText("")
        self.main_window.selected_mod_package_id_label.setText("")
        self.main_window.selected_mod_supported_versions_label.setText("")
        self.main_window.selected_mod_description.setText("")
        self.main_window.selected_mod_description.hide()

    @staticmethod
    def _move_mod_to_list_view(
        index: QModelIndex,
        source_list_view: QListView,
        target_list_view: QListView,
    ) -> None:
        # Ensure the source_list_view and target_list_view are of type QListView
        if not isinstance(source_list_view, QListView):
            raise TypeError(
                f"Expected source_list_view of type QListView, but got {type(source_list_view)}"
            )
        if not isinstance(target_list_view, QListView):
            raise TypeError(
                f"Expected target_list_view of type QListView, but got {type(target_list_view)}"
            )

        # Retrieve the item from the source model
        source_model = cast(QStandardItemModel, source_list_view.model())

        # If the model is a QSortFilterProxyModel, get its source model
        if isinstance(source_model, QSortFilterProxyModel):
            index = source_model.mapToSource(index)
            source_model = cast(QStandardItemModel, source_model.sourceModel())

        # Ensure the source model is a QStandardItemModel
        if not isinstance(source_model, QStandardItemModel):
            raise TypeError(
                f"Expected source_model of type QStandardItemModel, but got {type(source_model)}"
            )

        # Retrieve the item from the source model
        item = source_model.itemFromIndex(index)

        # Clone the item
        item_clone = item.clone()

        # Remove the item from the source model
        source_model.removeRow(index.row())

        # Add the item to the bottom of the target model
        target_model = cast(QStandardItemModel, target_list_view.model())
        if isinstance(target_model, QSortFilterProxyModel):
            target_model = cast(QStandardItemModel, target_model.sourceModel())
        target_model.appendRow(item_clone)
