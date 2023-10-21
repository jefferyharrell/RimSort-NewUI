from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication

from controllers.settings_dialog_controller import SettingsDialogController
from views.about_dialog import AboutDialog
from views.main_menu import MainMenu


class MainMenuController(QObject):
    def __init__(
        self,
        view: MainMenu,
        settings_dialog_controller: SettingsDialogController,
        about_dialog: AboutDialog,
    ) -> None:
        super().__init__()

        self.main_menu = view
        self.settings_dialog_controller = settings_dialog_controller
        self.about_dialog = about_dialog

        self.main_menu.about_action.triggered.connect(self._on_about_action_triggered)
        self.main_menu.settings_action.triggered.connect(
            self._on_settings_action_triggered
        )
        self.main_menu.exit_action.triggered.connect(self._on_exit_action_triggered)

    @Slot()
    def _on_about_action_triggered(self) -> None:
        self.about_dialog.show()

    @Slot()
    def _on_settings_action_triggered(self) -> None:
        self.settings_dialog_controller.show_settings_dialog()

    @Slot()
    def _on_exit_action_triggered(self) -> None:
        QApplication.quit()
