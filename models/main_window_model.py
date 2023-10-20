from PySide6.QtCore import QObject, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel


class MainWindowModel(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.inactive_mods_list_model = QStandardItemModel()
        self.inactive_mods_proxy_model = QSortFilterProxyModel(self)

        self.active_mods_list_model = QStandardItemModel()
        self.active_mods_proxy_model = QSortFilterProxyModel(self)
