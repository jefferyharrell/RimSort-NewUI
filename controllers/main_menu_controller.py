from PySide6.QtCore import QObject, Slot

from controllers.about_dialog_controller import AboutDialogController
from controllers.main_window_controller import MainWindowController
from controllers.settings_dialog_controller import SettingsDialogController
from utilities.event_bus import EventBus
from views.main_menu import MainMenu


class MainMenuController(QObject):
    def __init__(
        self,
        view: MainMenu,
    ) -> None:
        super().__init__()

        self.main_menu = view

        self.main_menu.about_action.triggered.connect(
            EventBus.instance().main_menu_about_action_triggered.emit
        )

        self.main_menu.settings_action.triggered.connect(
            EventBus.instance().main_menu_settings_action_triggered.emit
        )

        self.main_menu.quit_action.triggered.connect(
            EventBus.instance().main_menu_quit_action_triggered.emit
        )

        self.main_menu.zoom_action.triggered.connect(
            EventBus.instance().main_menu_zoom_action_triggered.emit
        )
