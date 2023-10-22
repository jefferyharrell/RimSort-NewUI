from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar, QMenu

from utilities.system_info import SystemInfo


class MainMenu(QObject):
    def __init__(self, menu_bar: QMenuBar) -> None:
        super().__init__()

        self.menu_bar = menu_bar

        if SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            self._do_main_menu_macos()
        else:
            self._do_main_menu_non_macos()

    def _do_main_menu_macos(self) -> None:
        app_menu = self.menu_bar.addMenu("AppName")  # This title is ignored on macOS

        self.about_action = QAction("About", self)
        app_menu.addAction(self.about_action)

        app_menu.addSeparator()

        self.settings_action = QAction("Settings…", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        self.settings_action.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        app_menu.addAction(self.settings_action)

        app_menu.addSeparator()

        self.quit_action = QAction("Quit", self)
        app_menu.addAction(self.quit_action)

        self._do_file_menu()
        self._do_window_menu()

    def _do_main_menu_non_macos(self) -> None:
        self._do_file_menu()

        help_menu = self.menu_bar.addMenu("Help")

        self.about_action = QAction("About NewUI", self)
        help_menu.addAction(self.about_action)

    def _do_file_menu(self) -> None:
        file_menu = self.menu_bar.addMenu("File")

        self.open_mod_list_action = QAction("Open Mod List", self)
        self.open_mod_list_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_mod_list_action.setEnabled(False)
        file_menu.addAction(self.open_mod_list_action)

        file_menu.addSeparator()

        self.save_mod_list_action = QAction("Save Mod List", self)
        self.save_mod_list_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_mod_list_action.setEnabled(False)
        file_menu.addAction(self.save_mod_list_action)

        file_menu.addSeparator()

        export_submenu = QMenu("Export")
        file_menu.addMenu(export_submenu)

        self.export_to_clipboard_action = QAction("To Clipboard…", self)
        self.export_to_clipboard_action.setEnabled(False)
        export_submenu.addAction(self.export_to_clipboard_action)

        self.export_to_file_action = QAction("To Text File…", self)
        self.export_to_file_action.setEnabled(False)
        export_submenu.addAction(self.export_to_file_action)

        self.export_to_rentry_action = QAction("To Rentry.co…", self)
        self.export_to_rentry_action.setEnabled(False)
        export_submenu.addAction(self.export_to_rentry_action)

    def _do_window_menu(self) -> None:
        window_menu = self.menu_bar.addMenu("Window")

        self.zoom_action = QAction("Zoom", self)
        window_menu.addAction(self.zoom_action)
