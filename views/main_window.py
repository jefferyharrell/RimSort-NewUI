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

        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(
            self.app_controller.show_preferences_dialog
        )
        app_menu.addAction(preferences_action)
        app_menu.addSeparator()

    def _do_main_menu_non_macos(self) -> None:
        file_menu = self.menuBar().addMenu("File")

        preferences_action = QAction("Preferences", self)
        preferences_action.setShortcut(QKeySequence.StandardKey.Preferences)
        preferences_action.triggered.connect(
            self.app_controller.show_preferences_dialog
        )
        file_menu.addAction(preferences_action)
        file_menu.addSeparator()
