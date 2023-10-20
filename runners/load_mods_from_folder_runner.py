from pathlib import Path
from typing import List

from PySide6.QtCore import QRunnable
from logger_tt import logger
from lxml import etree

from objects.mod import Mod
from runners.runner_signals import RunnerSignals


class LoadModsFromFolderRunner(QRunnable):
    def __init__(self, folder_location_path: Path) -> None:
        super().__init__()
        self.folder_location_path = folder_location_path
        self.signals = RunnerSignals()

    def run(self) -> None:
        data: List[Mod] = []
        for subfolder in self.folder_location_path.iterdir():
            if subfolder.is_dir():
                about_xml_path = subfolder / "About" / "About.xml"

                name = ""
                package_id = ""
                supported_versions = []

                if about_xml_path.exists():
                    try:
                        tree = etree.parse(str(about_xml_path))
                        root = tree.getroot()

                        node = root.find("./name")
                        name = node.text if node is not None else ""
                        node = root.find("./packageId")
                        package_id = node.text if node is not None else ""
                        supported_versions = root.xpath("./supportedVersions/li/text()")
                    except etree.XMLSyntaxError:
                        logger.warning(f"Could not parse About.xml at {about_xml_path}")

                    preview_image_path = subfolder / "About" / "Preview.png"

                    if name is not None:
                        data.append(
                            Mod(
                                name, package_id, supported_versions, preview_image_path
                            )
                        )

        self.signals.data_ready.emit(data)
        self.signals.finished.emit()
