from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMenuBar, QMenu

from utilities.app_info import AppInfo
from utilities.system_info import SystemInfo


class MenuBar(QObject):
    def __init__(self, menu_bar: QMenuBar) -> None:
        super().__init__()

        self.menu_bar = menu_bar

        if SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
            self._do_menu_bar_macos()
        else:
            self._do_menu_bar_non_macos()

    def _do_menu_bar_macos(self) -> None:
        app_menu = self.menu_bar.addMenu("AppName")  # This title is ignored on macOS

        self.about_action = QAction("About", self)
        app_menu.addAction(self.about_action)

        self.check_for_updates_action = QAction("Check for Updates…", self)
        self.check_for_updates_action.setMenuRole(
            QAction.MenuRole.ApplicationSpecificRole
        )
        app_menu.addAction(self.check_for_updates_action)

        app_menu.addSeparator()

        self.settings_action = QAction("Settings…", self)
        self.settings_action.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        app_menu.addAction(self.settings_action)

        app_menu.addSeparator()

        self.quit_action = QAction("Quit", self)
        app_menu.addAction(self.quit_action)

        self.file_menu = self.menu_bar.addMenu("File")

        self.open_mod_list_action = QAction("Open Mod List", self)
        self.open_mod_list_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_mod_list_action.setEnabled(False)
        self.file_menu.addAction(self.open_mod_list_action)

        self.file_menu.addSeparator()

        self.save_mod_list_action = QAction("Save Mod List", self)
        self.save_mod_list_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_mod_list_action.setEnabled(False)
        self.file_menu.addAction(self.save_mod_list_action)

        self.file_menu.addSeparator()

        self.export_submenu = QMenu("Export")
        self.file_menu.addMenu(self.export_submenu)

        self.export_to_clipboard_action = QAction("To Clipboard…", self)
        self.export_to_clipboard_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_clipboard_action)

        self.export_to_file_action = QAction("To Text File…", self)
        self.export_to_file_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_file_action)

        self.export_to_rentry_action = QAction("To Rentry.co…", self)
        self.export_to_rentry_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_rentry_action)

        self.edit_menu = self.menu_bar.addMenu("Edit")

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut(QKeySequence("Ctrl+X"))
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+C"))
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(QKeySequence("Ctrl+V"))
        self.edit_menu.addAction(self.paste_action)

        self.window_menu = self.menu_bar.addMenu("Window")

        self.minimize_action = QAction("Minimize", self)
        self.window_menu.addAction(self.minimize_action)

        self.zoom_action = QAction("Zoom", self)
        self.window_menu.addAction(self.zoom_action)

        self.help_menu = self.menu_bar.addMenu("Help")

        self.wiki_action = QAction(f"{AppInfo().app_name} Wiki…", self)
        self.help_menu.addAction(self.wiki_action)

    def _do_menu_bar_non_macos(self) -> None:
        self.file_menu = self.menu_bar.addMenu("File")

        self.open_mod_list_action = QAction("Open Mod List", self)
        self.open_mod_list_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_mod_list_action.setEnabled(False)
        self.file_menu.addAction(self.open_mod_list_action)

        self.file_menu.addSeparator()

        self.save_mod_list_action = QAction("Save Mod List", self)
        self.save_mod_list_action.setShortcut(QKeySequence("Ctrl+S"))
        self.save_mod_list_action.setEnabled(False)
        self.file_menu.addAction(self.save_mod_list_action)

        self.file_menu.addSeparator()

        self.export_submenu = QMenu("Export")
        self.file_menu.addMenu(self.export_submenu)

        self.export_to_clipboard_action = QAction("To Clipboard…", self)
        self.export_to_clipboard_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_clipboard_action)

        self.export_to_file_action = QAction("To Text File…", self)
        self.export_to_file_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_file_action)

        self.export_to_rentry_action = QAction("To Rentry.co…", self)
        self.export_to_rentry_action.setEnabled(False)
        self.export_submenu.addAction(self.export_to_rentry_action)

        self.file_menu.addSeparator()

        self.settings_action = QAction("Settings…", self)
        self.file_menu.addAction(self.settings_action)

        self.file_menu.addSeparator()

        self.quit_action = QAction("Exit", self)
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.file_menu.addAction(self.quit_action)

        self.edit_menu = self.menu_bar.addMenu("Edit")

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut(QKeySequence("Ctrl+X"))
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+C"))
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(QKeySequence("Ctrl+V"))
        self.edit_menu.addAction(self.paste_action)

        self.window_menu = self.menu_bar.addMenu("Window")

        self.minimize_action = QAction("Minimize", self)
        self.window_menu.addAction(self.minimize_action)

        self.zoom_action = QAction("Zoom", self)
        self.window_menu.addAction(self.zoom_action)

        self.help_menu = self.menu_bar.addMenu("Help")

        self.wiki_action = QAction(f"{AppInfo().app_name} Wiki…", self)
        self.help_menu.addAction(self.wiki_action)

        self.help_menu.addSeparator()

        self.check_for_updates_action = QAction("Check for Updates…", self)
        self.help_menu.addAction(self.check_for_updates_action)

        self.help_menu.addSeparator()

        self.about_action = QAction(f"About {AppInfo().app_name}", self)
        self.help_menu.addAction(self.about_action)
