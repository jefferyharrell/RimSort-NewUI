import sys

from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QApplication

from controllers.preferences_controller import PreferencesController
from models.preferences import Preferences
from utilities.system_info import SystemInfo
from views.main_window import MainWindow
from views.preferences_dialog import PreferencesDialog


class AppController(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.app = QApplication(sys.argv)

        if SystemInfo.operating_system() == SystemInfo.OperatingSystem.WINDOWS:
            self.app.setStyle("Windows")
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.LINUX:
            self.app.setStyle("Fusion")
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.MACOS:
            self.app.setStyle("macOS")

        # Uncomment to debug the UI
        # self.app.setStyleSheet("QWidget { border: 1px solid red; }")

        self.main_window = MainWindow(app_controller=self)

        self.preferences = Preferences()
        self.preferences_dialog = PreferencesDialog(parent=self.main_window)

    def run(self) -> int:
        self.main_window.show()
        return self.app.exec()

    @Slot()
    def show_preferences_dialog(self) -> None:
        self.preferences_dialog.exec()
