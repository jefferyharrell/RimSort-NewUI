from typing import TYPE_CHECKING

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QWidget

from utilities.system_info import SystemInfo

if TYPE_CHECKING:
    from controllers.app_controller import AppController


class MainWindow(QMainWindow):
    def __init__(self, app_controller: "AppController") -> None:
        super().__init__()

        self.app_controller: "AppController" = app_controller

        self.setWindowTitle("Main Window")
        self.setMinimumSize(1280, 720)

        if SystemInfo.operating_system() == SystemInfo.OperatingSystem.MACOS:
            self._do_main_menu_macos()
        else:
            self._do_main_menu_non_macos()

        central_widget = QWidget(self)

        self.setCentralWidget(central_widget)

    def _do_main_menu_macos(self) -> None:
        app_menu = self.menuBar().addMenu("AppName")  # This title is ignored on macOS

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(
            self.app_controller.show_settings_dialog
        )
        app_menu.addAction(settings_action)
        app_menu.addSeparator()

    def _do_main_menu_non_macos(self) -> None:
        file_menu = self.menuBar().addMenu("File")

        settings_action = QAction("Settings", self)
        settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        settings_action.triggered.connect(
            self.app_controller.show_settings_dialog
        )
        file_menu.addAction(settings_action)
        file_menu.addSeparator()
