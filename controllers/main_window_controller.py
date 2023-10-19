from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication

from models.main_window_model import MainWindowModel
from models.settings_model import SettingsModel
from views.about_dialog import AboutDialog
from views.main_window import MainWindow
from views.settings_dialog import SettingsDialog


class MainWindowController(QObject):
    def __init__(
        self,
        model: MainWindowModel,
        view: MainWindow,
        settings_model: SettingsModel,
        settings_dialog: SettingsDialog,
    ) -> None:
        super().__init__()

        self.main_window_model = model
        self.main_window = view
        self.settings_model = settings_model
        self.settings_dialog = settings_dialog

        self.about_dialog = AboutDialog()

        # Connect the signals
        self.main_window.about_action.triggered.connect(self._on_about_action_triggered)
        self.main_window.settings_action.triggered.connect(
            self._on_settings_action_triggered
        )
        self.main_window.exit_action.triggered.connect(self._on_exit_action_triggered)

        # Connect the models to their views
        self.main_window.inactive_mods_list_view.setModel(
            self.main_window_model.inactive_mods_list_model
        )

    # region SLots

    @Slot()
    def _on_about_action_triggered(self) -> None:
        self.about_dialog.show()

    @Slot()
    def _on_settings_action_triggered(self) -> None:
        self.settings_dialog.exec()

    @Slot()
    def _on_exit_action_triggered(self) -> None:
        QApplication.quit()

    # endregion
