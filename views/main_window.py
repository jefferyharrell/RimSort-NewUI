from PySide6.QtGui import QAction, QKeySequence, Qt
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
)

from utilities.gui_info import GUIInfo
from utilities.system_info import SystemInfo
from widgets.drag_drop_list_view import DragDropListView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NewUI")
        self.setMinimumSize(1000, 600)

        if SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            self._do_main_menu_macos()
        else:
            self._do_main_menu_non_macos()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_layout = QVBoxLayout(central_widget)

        frames_layout = QHBoxLayout()

        selected_mod_info_frame = QGroupBox()
        frames_layout.addWidget(selected_mod_info_frame, stretch=2)

        selected_mod_layout = QVBoxLayout(selected_mod_info_frame)

        selected_mod_label = QLabel("Selected Mod")
        selected_mod_label.setFont(GUIInfo().emphasis_font)
        selected_mod_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        selected_mod_layout.addWidget(selected_mod_label)

        self.selected_mod_preview_image = QLabel()
        selected_mod_layout.addWidget(self.selected_mod_preview_image)

        selected_mod_layout.addStretch()

        self.selected_mod_table = QTableWidget(3, 2)
        self.selected_mod_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.selected_mod_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.selected_mod_table.horizontalHeader().setVisible(False)
        self.selected_mod_table.verticalHeader().setVisible(False)
        self.selected_mod_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.selected_mod_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.selected_mod_table.setShowGrid(False)
        self.selected_mod_table.setStyleSheet("background: transparent;")

        row = 0
        self.selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Name")
        row_header_label.setFont(GUIInfo().emphasis_font)
        self.selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_name_label = QTableWidgetItem()
        self.selected_mod_table.setItem(row, 1, self.selected_mod_name_label)

        row = 1
        self.selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Package ID")
        row_header_label.setFont(GUIInfo().emphasis_font)
        self.selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_package_id_label = QTableWidgetItem()
        self.selected_mod_table.setItem(row, 1, self.selected_mod_package_id_label)

        row = 2
        self.selected_mod_table.setRowHeight(row, GUIInfo().default_font_line_height)
        row_header_label = QTableWidgetItem("Supported Versions")
        row_header_label.setFont(GUIInfo().emphasis_font)
        self.selected_mod_table.setItem(row, 0, row_header_label)
        self.selected_mod_supported_versions_label = QTableWidgetItem()
        self.selected_mod_table.setItem(
            row, 1, self.selected_mod_supported_versions_label
        )

        selected_mod_layout.addWidget(self.selected_mod_table)

        inactive_mods_frame = QGroupBox()
        frames_layout.addWidget(inactive_mods_frame, stretch=1)

        inactive_mods_layout = QVBoxLayout(inactive_mods_frame)

        inactive_mods_label = QLabel("Inactive Mods")
        inactive_mods_label.setFont(GUIInfo().emphasis_font)
        inactive_mods_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inactive_mods_layout.addWidget(inactive_mods_label)

        self.inactive_mods_filter_field = QLineEdit()
        self.inactive_mods_filter_field.setPlaceholderText("Search...")
        inactive_mods_layout.addWidget(self.inactive_mods_filter_field)

        self.inactive_mods_list_view = DragDropListView()
        self.inactive_mods_list_view.setFont(GUIInfo().default_font)
        self.inactive_mods_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        inactive_mods_layout.addWidget(self.inactive_mods_list_view)

        active_mods_frame = QGroupBox()
        frames_layout.addWidget(active_mods_frame, stretch=1)

        active_mods_layout = QVBoxLayout(active_mods_frame)

        active_mods_label = QLabel("Active Mods")
        active_mods_label.setFont(GUIInfo().emphasis_font)
        active_mods_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        active_mods_layout.addWidget(active_mods_label)

        self.active_mods_filter_field = QLineEdit()
        self.active_mods_filter_field.setPlaceholderText("Search...")
        active_mods_layout.addWidget(self.active_mods_filter_field)

        self.active_mods_list_view = DragDropListView()
        self.active_mods_list_view.setFont(GUIInfo().default_font)
        self.active_mods_list_view.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        active_mods_layout.addWidget(self.active_mods_list_view)

        central_layout.addLayout(frames_layout)

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setMinimumWidth(100)
        button_layout.addWidget(self.refresh_button)

        self.sort_button = QPushButton("Sort")
        self.sort_button.setMinimumWidth(100)
        self.sort_button.setDefault(True)
        button_layout.addWidget(self.sort_button)

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumWidth(100)
        button_layout.addWidget(self.save_button)

        central_layout.addLayout(button_layout)

    def _do_main_menu_macos(self) -> None:
        app_menu = self.menuBar().addMenu("AppName")  # This title is ignored on macOS

        self.about_action = QAction("About", self)
        app_menu.addAction(self.about_action)
        app_menu.addSeparator()

        self.settings_action = QAction("Settings", self)
        app_menu.addAction(self.settings_action)
        app_menu.addSeparator()

        self.exit_action = QAction("Quit", self)
        app_menu.addAction(self.exit_action)

    def _do_main_menu_non_macos(self) -> None:
        file_menu = self.menuBar().addMenu("File")

        self.settings_action = QAction("Settings", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        file_menu.addAction(self.settings_action)
        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        file_menu.addAction(self.exit_action)

        help_menu = self.menuBar().addMenu("Help")

        self.about_action = QAction("About NewUI", self)
        help_menu.addAction(self.about_action)
