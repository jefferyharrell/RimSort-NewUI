import uuid
from pathlib import Path
from typing import Iterable

from PySide6.QtGui import QStandardItem, Qt


class Mod(QStandardItem):
    def __init__(
        self,
        name: str,
        package_id: str,
        supported_versions: Iterable[str],
        description: str,
        preview_image_path: Path,
    ) -> None:
        super().__init__(name)

        self._id = uuid.uuid4()

        self._name = name
        self._package_id = package_id
        self._supported_versions = supported_versions
        self._description = description
        self._preview_image_path = preview_image_path

        self.setData(self.id, Qt.ItemDataRole.UserRole)

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def package_id(self) -> str:
        return self._package_id

    @property
    def supported_versions(self) -> Iterable[str]:
        return self._supported_versions

    @property
    def description(self) -> str:
        return self._description

    @property
    def preview_image_path(self) -> Path:
        return self._preview_image_path

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Mod({self.name}, {self.package_id}, {self.supported_versions}, {self.preview_image_path})"
