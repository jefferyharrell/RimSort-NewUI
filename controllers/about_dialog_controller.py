from PySide6.QtCore import QObject

from views.about_dialog import AboutDialog


class AboutDialogController(QObject):
    def __init__(self, view: AboutDialog) -> None:
        super().__init__()

        self.about_dialog = view

        self.about_dialog.close_window_hotkey.connect(self._on_close_window_hotkey)

    def show_about_dialog(self) -> None:
        self.about_dialog.show()

    def _on_close_window_hotkey(self) -> None:
        self.about_dialog.close()
