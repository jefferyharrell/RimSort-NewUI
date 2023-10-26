from PySide6.QtCore import (
    QObject,
    Slot,
    Qt,
    QModelIndex,
    QSortFilterProxyModel,
    QItemSelection,
    QItemSelectionModel,
)
from PySide6.QtGui import QPixmap, QStandardItemModel
from PySide6.QtWidgets import QListView

from controllers.settings_controller import SettingsController
from models.main_window_model import MainWindowModel
from models.mod import Mod
from models.mod_database import ModDatabase
from utilities.event_bus import EventBus
from views.main_window import MainWindow


class MainWindowController(QObject):
    def __init__(
        self,
        model: MainWindowModel,
        view: MainWindow,
        settings_controller: SettingsController,
    ) -> None:
        super().__init__()

        self.main_window_model = model
        self.main_window = view
        self.settings_controller = settings_controller

        EventBus().menu_bar_minimize_triggered.connect(
            self._on_minimize_action_triggered
        )
        EventBus().menu_bar_zoom_triggered.connect(self._on_zoom_action_triggered)

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

        # Connect the models to their views
        self.main_window.inactive_mods_list_view.setModel(
            self.main_window_model.inactive_mod_list.proxy_model
        )
        self.main_window.active_mods_list_view.setModel(
            self.main_window_model.active_mod_list.proxy_model
        )

        self.main_window.inactive_mods_filter_field.textChanged.connect(
            self._update_inactive_mods_filter
        )
        self.main_window.active_mods_filter_field.textChanged.connect(
            self._update_active_mods_filter
        )

        self.main_window.inactive_mods_list_view.selectionModel().selectionChanged.connect(
            self._on_mods_list_view_selection_changed
        )
        self.main_window.active_mods_list_view.selectionModel().selectionChanged.connect(
            self._on_mods_list_view_selection_changed
        )

        EventBus().database_ready.connect(self._on_database_ready)

    @Slot()
    def _on_database_ready(self) -> None:
        if self.settings_controller.settings.config_folder_location is not None:
            self.main_window_model.active_mod_list.from_xml(
                self.settings_controller.settings.config_folder_location
                / "ModsConfig.xml"
            )

        for mod in ModDatabase():
            if mod not in self.main_window_model.active_mod_list:
                self.main_window_model.inactive_mod_list.append(mod)

        self.main_window_model.inactive_mod_list.sort()

    @Slot(str)
    def _update_inactive_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.inactive_mod_list.filter(text)

    @Slot(str)
    def _update_active_mods_filter(self, text: str) -> None:
        """Update the filter based on the text in the QLineEdit."""
        self.main_window_model.active_mod_list.filter(text)

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

        source_model = source_list_view.model()
        if isinstance(source_model, QSortFilterProxyModel):
            index = source_model.mapToSource(index)

        MainWindowController.move_mod_between_list_views(
            source_list_view, index, target_list_view
        )

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
        mod_id = index.data(Qt.ItemDataRole.UserRole)
        mod = ModDatabase().get_mod_by_id(mod_id)
        if not isinstance(mod, Mod):
            return

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
    def get_standard_item_model(view: QListView) -> QStandardItemModel:
        """Retrieve the underlying QStandardItemModel from a QListView."""
        model = view.model()

        if isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()

        if not isinstance(model, QStandardItemModel):
            raise TypeError(
                f"Expected model of type QStandardItemModel, but got {type(model)}"
            )

        return model

    @staticmethod
    def move_mod_between_list_views(
        source_list_view: QListView,
        index: QModelIndex,
        target_list_view: QListView,
    ) -> None:
        # Ensure the views are of type QListView
        if not isinstance(source_list_view, QListView) or not isinstance(
            target_list_view, QListView
        ):
            raise TypeError(
                "Both source_list_view and target_list_view must be of type QListView"
            )

        # Retrieve the item from the source model
        source_model = MainWindowController.get_standard_item_model(source_list_view)

        # Retrieve and clone the item
        item = source_model.itemFromIndex(index)
        item_clone = item.clone()

        # Remove the item from the source model
        source_model.removeRow(index.row())

        # Add the item to the target model
        target_model = MainWindowController.get_standard_item_model(
            target_list_view
        )  # Use the class name to call the static method
        target_model.appendRow(item_clone)

    @Slot()
    def _on_zoom_action_triggered(self) -> None:
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            self.main_window.showMaximized()

    @Slot()
    def _on_minimize_action_triggered(self) -> None:
        if not self.main_window.isMinimized():
            self.main_window.showMinimized()
