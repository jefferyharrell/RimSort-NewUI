from pathlib import Path
from typing import List

from PySide6.QtCore import QRunnable
from logger_tt import logger
from lxml import etree

from models.mod import Mod
from runners.runner_signals import RunnerSignals


class ModListFromFolderPathRunner(QRunnable):
    def __init__(self, folder_path: Path) -> None:
        super().__init__()
        self.signals = RunnerSignals()
        self.folder_path = folder_path

    def run(self) -> None:
        data: List[Mod] = []

        for sub_folder in self.folder_path.iterdir():
            if not sub_folder.is_dir():
                continue

            about_xml_path = sub_folder / "About" / "About.xml"
            if not about_xml_path.exists():
                continue

            name: str = ""
            package_id: str = ""
            supported_versions: List[str] = []
            description: str = ""
            preview_image_path: Path = Path("")

            try:
                tree = etree.parse(str(about_xml_path))
                root = tree.getroot()

                node = root.find("./name")
                if node is not None:
                    name = str(node.text)

                node = root.find("./packageId")
                if node is not None:
                    package_id = str(node.text)

                xpath = root.xpath("./supportedVersions/li/text()")
                if isinstance(xpath, list):
                    supported_versions = [
                        item for item in xpath if isinstance(item, str)
                    ]

                node = root.find("./description")
                if node is not None:
                    description = str(node.text)

            except etree.XMLSyntaxError:
                logger.warning(f"Could not parse About.xml at {about_xml_path}")

            preview_image_path = sub_folder / "About" / "Preview.png"
            if not preview_image_path.exists():
                preview_image_path = Path("")

            if name is not None:
                mod = Mod(
                    name=name,
                    package_id=package_id,
                    supported_versions=supported_versions,
                    description=description,
                    preview_image_path=preview_image_path,
                )
                data.append(mod)

        self.signals.data_ready.emit(data)
        self.signals.finished.emit()
