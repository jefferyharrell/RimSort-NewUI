from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar

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

        self.exit_action = QAction("Quit", self)
        app_menu.addAction(self.exit_action)

        file_menu = self.menu_bar.addMenu("File")

        self.open_mod_list_action = QAction("Open Mod List", self)
        self.open_mod_list_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_mod_list_action.setEnabled(False)
        file_menu.addAction(self.open_mod_list_action)

        self.save_mod_list_action = QAction("Save Mod List", self)
        self.save_mod_list_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_mod_list_action.setEnabled(False)
        file_menu.addAction(self.save_mod_list_action)

        file_menu.addSeparator()

        self.close_window_action = QAction("Close Window", self)
        self.close_window_action.setShortcut(QKeySequence("Ctrl+W"))
        file_menu.addAction(self.close_window_action)
        file_menu.addSeparator()

    def _do_main_menu_non_macos(self) -> None:
        file_menu = self.menu_bar.addMenu("File")

        self.open_mod_list_action = QAction("Open Mod List", self)
        self.open_mod_list_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_mod_list_action.setEnabled(False)
        file_menu.addAction(self.open_mod_list_action)

        self.save_mod_list_action = QAction("Save Mod List", self)
        self.save_mod_list_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_mod_list_action.setEnabled(False)
        file_menu.addAction(self.save_mod_list_action)

        file_menu.addSeparator()

        self.close_window_action = QAction("Close Window", self)
        self.close_window_action.setShortcut(QKeySequence("Ctrl+W"))
        file_menu.addAction(self.close_window_action)

        file_menu.addSeparator()

        self.settings_action = QAction("Settings", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        file_menu.addAction(self.settings_action)

        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        file_menu.addAction(self.exit_action)

        help_menu = self.menu_bar.addMenu("Help")

        self.about_action = QAction("About NewUI", self)
        help_menu.addAction(self.about_action)
