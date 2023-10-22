from PySide6.QtCore import QObject

from utilities.event_bus import EventBus
from views.about_dialog import AboutDialog


class AboutDialogController(QObject):
    def __init__(self, view: AboutDialog) -> None:
        super().__init__()

        self.about_dialog = view

        EventBus.instance().menu_bar_about_action_triggered.connect(
            self.about_dialog.show
        )

        self.about_dialog.close_window_hotkey.connect(self.about_dialog.close)
