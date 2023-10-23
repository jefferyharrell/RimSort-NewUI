import uuid
from typing import Dict

from PySide6.QtCore import QObject, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel

from models.mod import Mod


class MainWindowModel(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.mods_dictionary: Dict[uuid.UUID, Mod] = {}

        self.inactive_mods_list_model = QStandardItemModel()
        self.inactive_mods_proxy_model = QSortFilterProxyModel()

        self.active_mods_list_model = QStandardItemModel()
        self.active_mods_proxy_model = QSortFilterProxyModel()
