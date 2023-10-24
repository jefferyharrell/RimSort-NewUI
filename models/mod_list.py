import uuid
from pathlib import Path
from typing import Any, Optional, Dict

from PySide6.QtCore import (
    QObject,
    QSortFilterProxyModel,
    Qt,
    QModelIndex,
    QThreadPool,
    Slot,
)
from PySide6.QtGui import QStandardItemModel

from models.mod import Mod
from runners.mod_list_from_folder_path_runner import ModListFromFolderPathRunner


class ModList(QObject):
    """
    Represents a list of RimWorld mods.
    """

    def __init__(self) -> None:
        super().__init__()

        self._inner_model: QStandardItemModel = QStandardItemModel()

        self._proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self._proxy_model.setSourceModel(self._inner_model)
        self._proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self._id_to_mod_map: Dict[uuid.UUID, Mod] = {}

    @property
    def proxy_model(self) -> QSortFilterProxyModel:
        """
        :return: The proxy model used for sorting and filtering.
        :rtype: QSortFilterProxyModel
        """
        return self._proxy_model

    # CRUD Operations
    def append(self, item: Mod) -> None:
        """
        Append a Mod item to the end of the list.

        :param item: The Mod item to append.
        :type item: Mod
        """
        self._inner_model.appendRow(item)
        self._id_to_mod_map[item.id] = item

    def insert(self, item: Mod, index: int) -> None:
        """
        Insert a Mod item at a specific index.

        :param item: The Mod item to insert.
        :type item: Mod
        :param index: The index at which to insert the item.
        :type index: int
        """
        self._inner_model.insertRow(index, item)
        self._id_to_mod_map[item.id] = item

    def update(self, index: int, new_item: Mod) -> None:
        """
        Update the Mod item at a specific index.

        :param index: The index of the item to update.
        :type index: int
        :param new_item: The new Mod item to replace the existing one.
        :type new_item: Mod
        """
        self._inner_model.setItem(index, new_item)

    def remove(self, index: int) -> None:
        """
        Remove the Mod item at a specific index.

        :param index: The index of the item to remove.
        :type index: int
        """
        item = self.get_item(index)
        if item:
            del self._id_to_mod_map[item.id]
        self._inner_model.removeRow(index)

    def clear(self) -> None:
        """
        Remove all Mod items from the list.
        """
        self._inner_model.clear()
        self._id_to_mod_map.clear()

    # I/O Methods
    def from_folder_path(self, folder_path: Path) -> None:
        """
        Load Mod items into the list from a folder path.

        :param folder_path: The path to the folder from which to load mods.
        :type folder_path: Path
        """
        runner = ModListFromFolderPathRunner(folder_path)
        runner.signals.data_ready.connect(self._on_from_folder_path_data_ready)
        pool = QThreadPool.globalInstance()
        pool.start(runner)

    @Slot(object)
    def _on_from_folder_path_data_ready(self, data: object) -> None:
        if not isinstance(data, list) or not all(
            isinstance(item, Mod) for item in data
        ):
            raise TypeError("Expected a list of Mod objects")
        for mod in data:
            self.append(mod)
        self.sort(Qt.SortOrder.AscendingOrder)

    def to_xml(self) -> str:
        return ""

    # Other Public Methods
    def count(self) -> int:
        """
        Get the total number of Mod items in the list.

        :return: The number of Mod items.
        :rtype: int
        """
        return self._inner_model.rowCount()

    def get_by_uuid(self, mod_id: uuid.UUID) -> Optional[Mod]:
        """
        Find a Mod item by its unique identifier.

        :param mod_id: The unique identifier of the Mod item.
        :type mod_id: uuid.UUID
        :return: The Mod item if found, otherwise None.
        :rtype: Optional[Mod]
        """
        return self._id_to_mod_map.get(mod_id)

    def sort(self, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        """
        Do a one-time sort of the mod list..

        :param order: The order in which to sort (ascending or descending).
        :type order: Qt.SortOrder
        """
        self._inner_model.sort(0, order)

    def filter(self, text: str) -> None:
        """
        Filter the Mod items based on a specific text.

        :param text: The text to filter the Mod items.
        :type text: str
        """
        self._proxy_model.setFilterFixedString(text)

    # Utility Methods
    def index(self, row: int) -> QModelIndex:
        """
        Get the QModelIndex for a specific row.

        :param row: The row index.
        :type row: int
        :return: The QModelIndex for the specified row.
        :rtype: QModelIndex
        """
        return self._proxy_model.index(row, 0)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Get the data for a specific QModelIndex and role.

        :param index: The QModelIndex for which to get the data.
        :type index: QModelIndex
        :param role: The role for which to get the data.
        :type role: int
        :return: The data for the specified index and role.
        """
        return self._proxy_model.data(index, role)

    def get_item(self, index: int) -> Optional[Mod]:
        """
        Get the Mod item at a specific index.

        :param index: The index of the Mod item.
        :type index: int
        :return: The Mod item if found, otherwise None.
        :rtype: Optional[Mod]
        """
        item = self._inner_model.item(index)
        if isinstance(item, Mod):
            return item
        return None

    # Representation and Special Methods
    def __repr__(self) -> str:
        """
        Return an unambiguous representation of the ModList.

        :return: The string representation of the ModList.
        :rtype: str
        """
        return f"<ModList with {self.count()} Mods>"

    def __str__(self) -> str:
        """
        Return a human-readable representation of the ModList.

        :return: The formatted list of Mod names.
        :rtype: str
        """
        mod_names = [mod.name for mod in self._id_to_mod_map.values()]
        return "\n".join(mod_names)

    def __len__(self) -> int:
        """
        Return the number of Mod items in the list.

        :return: The number of Mod items.
        :rtype: int
        """
        return self._inner_model.rowCount()

    def __iter__(self) -> "ModList":
        """
        Return an iterator over the Mod items.

        :return: The iterator for the ModList.
        :rtype: ModList
        """
        self._current_index = 0
        return self

    def __next__(self) -> Optional[Mod]:
        """
        Return the next Mod item in the iteration.

        :return: The next Mod item.
        :rtype: Optional[Mod]
        :raises StopIteration: If there are no more items to iterate over.
        """
        if self._current_index < self.count():
            mod = self.get_item(self._current_index)
            self._current_index += 1
            return mod
        else:
            raise StopIteration
