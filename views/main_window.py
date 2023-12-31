from PySide6.QtCore import QEvent
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QAbstractItemView,
    QGroupBox,
    QTableWidgetItem,
    QTableWidget,
    QHeaderView,
    QScrollArea,
    QTextEdit,
)

from utilities.app_info import AppInfo
from utilities.event_bus import EventBus
from utilities.game_info import GameInfo
from utilities.gui_info import GUIInfo
from widgets.drag_drop_list_view import DragDropListView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(AppInfo().app_name)
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout(central_widget)

        self.horizontal_layout = QHBoxLayout()

        self._do_selected_mod_widget()
        self._do_inactive_mods_widget()
        self._do_active_mods_widget()

        central_layout.addLayout(self.horizontal_layout)

        button_layout = QHBoxLayout()

        version_string = QLabel("RimWorld version " + GameInfo().version)
        version_string.setFont(GUIInfo().smaller_font)
        version_string.setEnabled(False)
        button_layout.addWidget(version_string)

        button_layout.addStretch()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMinimumWidth(100)
        button_layout.addWidget(self.refresh_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumWidth(100)
        button_layout.addWidget(self.clear_button)

        self.sort_button = QPushButton("Sort")
        self.sort_button.setMinimumWidth(100)
        self.sort_button.setDefault(True)
        button_layout.addWidget(self.sort_button)

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumWidth(100)
        button_layout.addWidget(self.save_button)

        central_layout.addLayout(button_layout)

    def _do_selected_mod_widget(self) -> None:
        selected_mod_info_frame = QGroupBox()
        self.horizontal_layout.addWidget(selected_mod_info_frame, stretch=2)

        selected_mod_layout = QVBoxLayout(selected_mod_info_frame)

        selected_mod_label = QLabel("Selected Mod")
        selected_mod_label.setFont(GUIInfo().emphasis_font)
        selected_mod_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)

        self.selected_mod_preview_image = QLabel()

        selected_mod_table = QTableWidget(3, 2)
        selected_mod_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        selected_mod_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        selected_mod_table.horizontalHeader().setVisible(False)
        selected_mod_table.verticalHeader().setVisible(False)
        selected_mod_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        selected_mod_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        selected_mod_table.setShowGrid(False)
        selected_mod_table.setStyleSheet("background: transparent;")

        row = 0
        selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Name")
        row_header_label.setFont(GUIInfo().emphasis_font)
        selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_name_label = QTableWidgetItem()
        selected_mod_table.setItem(row, 1, self.selected_mod_name_label)

        row = 1
        selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Package ID")
        row_header_label.setFont(GUIInfo().emphasis_font)
        selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_package_id_label = QTableWidgetItem()
        selected_mod_table.setItem(row, 1, self.selected_mod_package_id_label)

        row = 2
        selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Supported Versions")
        row_header_label.setFont(GUIInfo().emphasis_font)
        selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_supported_versions_label = QTableWidgetItem()
        selected_mod_table.setItem(row, 1, self.selected_mod_supported_versions_label)

        total_height = sum(
            [
                selected_mod_table.rowHeight(i)
                for i in range(selected_mod_table.rowCount())
            ]
        )
        selected_mod_table.setFixedHeight(total_height + 2)

        self.selected_mod_description = QTextEdit()
        self.selected_mod_description.setReadOnly(True)
        self.selected_mod_description.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.selected_mod_description.setStyleSheet("background: transparent;")
        self.selected_mod_description.hide()

        scroll_layout.addWidget(self.selected_mod_preview_image)
        scroll_layout.addStretch()
        scroll_layout.addWidget(selected_mod_table)
        scroll_layout.addWidget(self.selected_mod_description)

        selected_mod_layout.addWidget(selected_mod_label)
        selected_mod_layout.addWidget(scroll_area)

    def _do_inactive_mods_widget(self) -> None:
        inactive_mods_frame = QGroupBox()
        self.horizontal_layout.addWidget(inactive_mods_frame, stretch=1)

        inactive_mods_layout = QVBoxLayout(inactive_mods_frame)
        inactive_mods_label = QLabel("Inactive Mods")
        inactive_mods_label.setFont(GUIInfo().emphasis_font)
        inactive_mods_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inactive_mods_layout.addWidget(inactive_mods_label)

        self.inactive_mods_filter_field = QLineEdit()
        self.inactive_mods_filter_field.setPlaceholderText("Filter…")
        self.inactive_mods_filter_field.setClearButtonEnabled(True)
        inactive_mods_layout.addWidget(self.inactive_mods_filter_field)

        self.inactive_mods_list_view = DragDropListView()
        self.inactive_mods_list_view.setFont(GUIInfo().default_font)
        self.inactive_mods_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.inactive_mods_list_view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        inactive_mods_layout.addWidget(self.inactive_mods_list_view)

    def _do_active_mods_widget(self) -> None:
        active_mods_frame = QGroupBox()
        self.horizontal_layout.addWidget(active_mods_frame, stretch=1)

        active_mods_layout = QVBoxLayout(active_mods_frame)

        active_mods_label = QLabel("Active Mods")
        active_mods_label.setFont(GUIInfo().emphasis_font)
        active_mods_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        active_mods_layout.addWidget(active_mods_label)

        self.active_mods_filter_field = QLineEdit()
        self.active_mods_filter_field.setPlaceholderText("Filter…")
        self.active_mods_filter_field.setClearButtonEnabled(True)
        active_mods_layout.addWidget(self.active_mods_filter_field)

        self.active_mods_list_view = DragDropListView()
        self.active_mods_list_view.setFont(GUIInfo().default_font)
        self.active_mods_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.active_mods_list_view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        active_mods_layout.addWidget(self.active_mods_list_view)

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.WindowStateChange:
            EventBus().main_window_state_changed.emit(self.windowState())
        super().changeEvent(event)
