from PySide6.QtCore import QObject, QStringListModel


class MainWindowModel(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.inactive_mods_list_model = QStringListModel(
            [f"Item {i}" for i in range(1, 101)]
        )
        self.active_mods_list_model = QStringListModel(
            [f"Item {i}" for i in range(1, 101)]
        )
