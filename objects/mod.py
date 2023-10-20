from pathlib import Path
from typing import List, Optional

from PySide6.QtGui import QStandardItem, Qt


class Mod(QStandardItem):
    def __init__(
        self,
        name: str,
        package_id: Optional[str],
        supported_versions: Optional[List[str]],
        preview_image_path: Path,
    ) -> None:
        super().__init__(name)
        self._name = name
        self._package_id = package_id
        self._supported_versions = supported_versions
        self._preview_image_path = preview_image_path

        self.setData(self, Qt.ItemDataRole.UserRole)

    @property
    def name(self) -> str:
        return self._name

    @property
    def package_id(self) -> Optional[str]:
        return self._package_id

    @property
    def supported_versions(self) -> Optional[List[str]]:
        return self._supported_versions

    @property
    def preview_image_path(self) -> Path:
        return self._preview_image_path

    def __str__(self) -> str:
        return self.name
