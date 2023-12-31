from PySide6.QtCore import QObject, Slot, Qt
from PySide6.QtWidgets import QApplication, QLineEdit

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
            EventBus().menu_bar_about_triggered.emit
        )

        self.menu_bar.check_for_updates_action.triggered.connect(
            EventBus().menu_bar_check_for_update_triggered.emit
        )

        self.menu_bar.settings_action.triggered.connect(
            EventBus().menu_bar_settings_triggered.emit
        )

        self.menu_bar.quit_action.triggered.connect(
            EventBus().menu_bar_quit_action_triggered.emit
        )

        self.menu_bar.cut_action.triggered.connect(self._on_menu_bar_cut_triggered)

        self.menu_bar.copy_action.triggered.connect(self._on_menu_bar_copy_triggered)

        self.menu_bar.paste_action.triggered.connect(self._on_menu_bar_paste_triggered)

        self.menu_bar.minimize_action.triggered.connect(
            EventBus().menu_bar_minimize_triggered.emit
        )

        self.menu_bar.zoom_action.triggered.connect(
            EventBus().menu_bar_zoom_triggered.emit
        )

        EventBus().main_window_state_changed.connect(self._on_main_window_state_changed)

    @Slot()
    def _on_menu_bar_cut_triggered(self) -> None:
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            focused_widget = app_instance.focusWidget()
            if focused_widget and isinstance(focused_widget, QLineEdit):
                focused_widget.cut()

    @Slot()
    def _on_menu_bar_copy_triggered(self) -> None:
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            focused_widget = app_instance.focusWidget()
            if focused_widget and isinstance(focused_widget, QLineEdit):
                focused_widget.copy()

    @Slot()
    def _on_menu_bar_paste_triggered(self) -> None:
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            focused_widget = app_instance.focusWidget()
            if focused_widget and isinstance(focused_widget, QLineEdit):
                focused_widget.paste()

    @Slot(Qt.WindowState)
    def _on_main_window_state_changed(self, state: Qt.WindowState) -> None:
        if state == Qt.WindowState.WindowMinimized:
            for action in self.menu_bar.window_menu.actions():
                action.setEnabled(False)

        if state == Qt.WindowState.WindowMaximized:
            for action in self.menu_bar.window_menu.actions():
                action.setEnabled(True)

        if state == Qt.WindowState.WindowNoState:
            for action in self.menu_bar.window_menu.actions():
                action.setEnabled(True)

        if state == Qt.WindowState.WindowFullScreen:
            for action in self.menu_bar.window_menu.actions():
                action.setEnabled(True)
