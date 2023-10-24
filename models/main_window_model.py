from PySide6.QtCore import QObject

from models.mod_list import ModList


class MainWindowModel(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.inactive_mod_list = ModList()
        self.active_mod_list = ModList()
