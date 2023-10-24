from PySide6.QtCore import QObject

from utilities.event_bus import EventBus
from views.menu_bar import MenuBar


class MenuBarController(QObject):
    def __init__(
        self,
        view: MenuBar,
    ) -> None:
        super().__init__()

        self.menu_bar = view

        self.menu_bar.about_action.triggered.connect(
            EventBus().menu_bar_about_action_triggered.emit
        )

        self.menu_bar.settings_action.triggered.connect(
            EventBus().menu_bar_settings_action_triggered.emit
        )

        self.menu_bar.quit_action.triggered.connect(
            EventBus().menu_bar_quit_action_triggered.emit
        )

        self.menu_bar.zoom_action.triggered.connect(
            EventBus().menu_bar_zoom_action_triggered.emit
        )
