from PySide6.QtCore import QObject

from models.main_window_model import MainWindowModel
from views.about_dialog import AboutDialog
from views.main_window import MainWindow
from views.settings_dialog import SettingsDialog


class MainWindowController(QObject):
    def __init__(
        self, model: MainWindowModel, view: MainWindow, settings_dialog: SettingsDialog
    ) -> None:
        super().__init__()

        self.main_window_model = model
        self.main_window = view
        self.settings_dialog = settings_dialog

        self.about_dialog = AboutDialog()

        self.main_window.about_action.triggered.connect(self.about_dialog.show)

        self.main_window.settings_action.triggered.connect(self.settings_dialog.exec)

        self.main_window.exit_action.triggered.connect(self.main_window.close)
