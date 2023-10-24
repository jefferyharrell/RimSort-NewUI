from pathlib import Path
from typing import List

from PySide6.QtCore import QRunnable
from loguru import logger
from lxml import etree

from models.mod import Mod
from runners.runner_signals import RunnerSignals


class ModsFromFoldersRunner(QRunnable):
    def __init__(self, from_folders: List[Path]) -> None:
        super().__init__()
        self.signals = RunnerSignals()
        self.from_folders = from_folders

    def run(self) -> None:
        logger.info(f"Searching for mods in {len(self.from_folders)} folders")

        data: List[Mod] = []

        for folder in self.from_folders:
            for sub_folder in folder.iterdir():
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

        logger.info(f"Found {len(data)} mods")

        self.signals.data_ready.emit(data)
        self.signals.finished.emit()
