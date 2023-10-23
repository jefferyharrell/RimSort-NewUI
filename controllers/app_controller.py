import sys

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from logger_tt import logger

from controllers.about_dialog_controller import AboutDialogController
from controllers.menu_bar_controller import MenuBarController
from controllers.main_window_controller import MainWindowController
from controllers.settings_dialog_controller import SettingsDialogController
from models.main_window_model import MainWindowModel
from models.settings_model import SettingsModel
from utilities.event_bus import EventBus
from utilities.path_info import PathInfo
from utilities.system_info import SystemInfo
from views.about_dialog import AboutDialog
from views.menu_bar import MenuBar
from views.main_window import MainWindow
from views.settings_dialog import SettingsDialog


class AppController(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.app = QApplication(sys.argv)

        if SystemInfo().operating_system == SystemInfo.OperatingSystem.WINDOWS:
            self.app.setStyle("Fusion")
        elif SystemInfo().operating_system == SystemInfo.OperatingSystem.LINUX:
            self.app.setStyle("Fusion")
        elif SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            self.app.setStyle("macOS")

        stylesheet_path = PathInfo().application_folder / "resources" / "style.qss"
        stylesheet = stylesheet_path.read_text()
        logger.info(f"Using stylesheet: {stylesheet_path}")
        self.app.setStyleSheet(stylesheet)

        # Uncomment to debug the UI
        # self.app.setStyleSheet("QWidget { border: 1px solid red; }")
        # self.app.setStyleSheet(
        #     stylesheet + "QWidget { background-color: rgba(255, 255, 255, 25); }"
        # )

        self.settings_model = SettingsModel()
        self.settings_dialog = SettingsDialog()
        self.settings_dialog_controller = SettingsDialogController(
            model=self.settings_model, view=self.settings_dialog
        )

        self.main_window_model = MainWindowModel()
        self.main_window = MainWindow()
        self.main_window_controller = MainWindowController(
            model=self.main_window_model,
            view=self.main_window,
            settings_dialog_controller=self.settings_dialog_controller,
        )

        self.about_dialog = AboutDialog()
        self.about_dialog_controller = AboutDialogController(view=self.about_dialog)

        self.menu_bar = MenuBar(menu_bar=self.main_window.menuBar())
        self.menu_bar_controller = MenuBarController(view=self.menu_bar)

        EventBus.instance().menu_bar_quit_action_triggered.connect(self.quit)

    def run(self) -> int:
        self.main_window.show()
        return self.app.exec()

    def quit(self) -> None:
        self.app.quit()
