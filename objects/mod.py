from typing import List

from PySide6.QtGui import QStandardItem


class Mod(QStandardItem):
    def __init__(
        self, name: str, package_id: str, supported_versions: List[str]
    ) -> None:
        super().__init__(name)
        self._name = name
        self._package_id = package_id
        self._supported_versions = supported_versions

    @property
    def name(self) -> str:
        return self._name

    @property
    def package_id(self) -> str:
        return self._package_id

    @property
    def supported_versions(self) -> List[str]:
        return self._supported_versions

    def __str__(self) -> str:
        return self.name
