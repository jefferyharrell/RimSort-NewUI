from PySide6.QtCore import QObject, QStringListModel


class MainWindowModel(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.inactive_mods_list_model = QStringListModel()
        self.active_mods_list_model = QStringListModel()
