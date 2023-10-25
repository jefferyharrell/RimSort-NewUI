from pathlib import Path
from typing import Optional, Dict, List

import uuid
from PySide6.QtCore import QObject, Slot, QThreadPool

from models.mod import Mod
from runners.mods_from_folders_runner import ModsFromFoldersRunner
from utilities.event_bus import EventBus


class ModDatabase(QObject):
    """
    A database for managing and storing Mod objects.
    """

    _instance = None

    def __new__(cls, from_folders: Optional[List[Path]] = None) -> "ModDatabase":
        """
        Ensure a single instance of ModDatabase is created (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(ModDatabase, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(self, from_folders: Optional[List[Path]] = None) -> None:
        """
        Initialize the ModDatabase.
        """
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        if from_folders is None:
            raise ValueError(
                "from_folders argument cannot be None during the first instantiation of ModDatabase."
            )

        super().__init__()

        self._mods_by_id: Dict[uuid.UUID, Mod] = {}
        self._mods_by_package_id: Dict[str, Mod] = {}

        self._load_mods(from_folders)

        self._is_initialized: bool = True

        EventBus().database_ready.emit()

    def add_mod(self, mod: Mod) -> None:
        """
        Add a Mod object to the database.

        :param mod: The Mod object to add.
        :type mod: Mod
        """
        self._mods_by_id[mod.id] = mod
        self._mods_by_package_id[mod.package_id.lower()] = mod

    def get_mod_by_package_id(self, mod_package_id: str) -> Optional[Mod]:
        """
        Retrieve a Mod object by its package ID.

        :param mod_package_id: The package ID of the Mod.
        :type mod_package_id: str
        :return: The Mod object if found, otherwise None.
        :rtype: Optional[Mod]
        """
        return self._mods_by_package_id.get(mod_package_id.lower())

    def get_mod_by_id(self, mod_id: uuid.UUID) -> Optional[Mod]:
        """
        Retrieve a Mod object by its UUID.

        :param mod_id: The UUID of the Mod.
        :type mod_id: uuid.UUID
        :return: The Mod object if found, otherwise None.
        :rtype: Optional[Mod]
        """
        return self._mods_by_id.get(mod_id)

    def remove_mod(self, mod: Mod) -> None:
        """
        Remove a Mod object from the database.

        :param mod: The Mod object to remove.
        :type mod: Mod
        """
        if mod.package_id in self._mods_by_package_id:
            del self._mods_by_package_id[mod.package_id]
        if mod.id in self._mods_by_id:
            del self._mods_by_id[mod.id]

    def clear(self) -> None:
        """
        Clear all Mod objects from the database.
        """
        self._mods_by_id.clear()
        self._mods_by_package_id.clear()

    def _load_mods(self, from_folders: List[Path]) -> None:
        """
        Load Mod items into the database from a list of folders.

        :param from_folders: The list of folders from which to load mods.
        :type from_folders: List[Path]
        """
        runner = ModsFromFoldersRunner(from_folders)
        runner.signals.data_ready.connect(self._on_data_ready)
        QThreadPool.globalInstance().start(runner)

    @Slot(object)
    def _on_data_ready(self, data: object) -> None:
        """
        Load found Mod items into the database.

        :param data: The ModDatabase instance.
        :type data: object
        """
        if not isinstance(data, list) or not all(
            isinstance(item, Mod) for item in data
        ):
            raise TypeError("Expected a list of Mod objects")
        for mod in data:
            self.add_mod(mod)
        EventBus().database_ready.emit()

    def __iter__(self) -> "ModDatabase":
        """
        Initialize the iterator for the ModDatabase.

        :return: The ModDatabase instance.
        :rtype: ModDatabase
        """
        self._current_iter_index = 0
        self._mods_list = list(self._mods_by_id.values())
        return self

    def __next__(self) -> Mod:
        """
        Get the next Mod object in the iteration.

        :return: The next Mod object.
        :rtype: Mod
        :raises StopIteration: If there are no more Mod objects to iterate over.
        """
        if self._current_iter_index < len(self._mods_list):
            mod = self._mods_list[self._current_iter_index]
            self._current_iter_index += 1
            return mod
        else:
            raise StopIteration
