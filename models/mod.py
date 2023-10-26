import uuid
from pathlib import Path
from typing import Optional, List

from PySide6.QtGui import QStandardItem, Qt, QPixmap


class Mod(QStandardItem):
    """
    Represents a RimWorld mod.

    :param name: The display name of the mod.
    :type name: str, optional
    :param package_id: The unique identifier for the mod package.
    :type package_id: str, optional
    :param supported_versions: A list of versions the mod supports.
    :type supported_versions: List[str], optional
    :param description: A brief description of the mod.
    :type description: str, optional
    :param preview_image_path: The path to the mod's preview image.
    :type preview_image_path: Path, optional
    """

    def __init__(
        self,
        name: str = "",
        package_id: str = "",
        supported_versions: Optional[List[str]] = None,
        description: str = "",
        preview_image_path: Path = Path(""),
    ) -> None:
        super().__init__(name)

        self._id = uuid.uuid4()

        self._name = name
        self._package_id = package_id
        self._supported_versions = (
            list(supported_versions) if supported_versions else []
        )
        self._description = description
        self._preview_image_path = preview_image_path

        self._preview_pixmap: Optional[QPixmap] = None

        if self._name == "" and self._package_id.lower() == "ludeon.rimworld":
            self._name = "Core"

        if self._name == "" and self._package_id.lower() == "ludeon.rimworld.royalty":
            self._name = "Royalty"

        if self._name == "" and self._package_id.lower() == "ludeon.rimworld.ideology":
            self._name = "Ideology"

        if self._name == "" and self._package_id.lower() == "ludeon.rimworld.biotech":
            self._name = "Biotech"

        self.setData(self.name, Qt.ItemDataRole.DisplayRole)
        self.setData(self.id, Qt.ItemDataRole.UserRole)

    @property
    def id(self) -> uuid.UUID:
        """
        :return: The unique identifier of the mod.
        :rtype: uuid.UUID
        """
        return self._id

    @property
    def name(self) -> str:
        """
        :return: The display name of the mod.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.setData(self._name, Qt.ItemDataRole.DisplayRole)

    @property
    def package_id(self) -> str:
        """
        :return: The unique identifier for the mod package.
        :rtype: str
        """
        return self._package_id

    @package_id.setter
    def package_id(self, value: str) -> None:
        self._package_id = value

    @property
    def supported_versions(self) -> List[str]:
        """
        :return: A list of versions the mod supports.
        :rtype: List[str]
        """
        return self._supported_versions

    @supported_versions.setter
    def supported_versions(self, value: List[str]) -> None:
        self._supported_versions = list(value)

    @property
    def description(self) -> str:
        """
        :return: A brief description of the mod.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def preview_image_path(self) -> Path:
        """
        :return: The path to the mod's preview image.
        :rtype: Path
        """
        return self._preview_image_path

    @preview_image_path.setter
    def preview_image_path(self, value: Path) -> None:
        self._preview_image_path = value

    @property
    def preview_pixmap(self) -> Optional[QPixmap]:
        if self._preview_pixmap is None and self._preview_image_path.exists():
            self._preview_pixmap = QPixmap(str(self._preview_image_path))
        return self._preview_pixmap

    def __str__(self) -> str:
        """
        Return a human-readable representation of the mod.

        :return: The display name of the mod.
        :rtype: str
        """
        return self.name

    def __repr__(self) -> str:
        """
        Return an unambiguous representation of the mod.

        :return: A string representation of the mod's attributes.
        :rtype: str
        """
        return f"Mod({self.name}, {self.package_id}, {self.supported_versions}, {self.preview_image_path.__repr__()})"
