from pathlib import Path
from typing import List

from PySide6.QtCore import QRunnable
from logger_tt import logger
from lxml import etree

from objects.mod import Mod
from runners.runner_signals import RunnerSignals


class LoadModsFromFoldersRunner(QRunnable):
    def __init__(self, folder_paths: List[Path]) -> None:
        super().__init__()
        self.signals = RunnerSignals()
        self.folder_paths = folder_paths

    def run(self) -> None:
        data: List[Mod] = []

        for folder_path in self.folder_paths:
            for sub_folder in folder_path.iterdir():
                if sub_folder.is_dir():
                    about_xml_path = sub_folder / "About" / "About.xml"

                    name = ""
                    package_id = ""
                    supported_versions = []
                    description = ""

                    if about_xml_path.exists():
                        try:
                            tree = etree.parse(str(about_xml_path))
                            root = tree.getroot()

                            node = root.find("./name")
                            name = node.text if node is not None else ""
                            node = root.find("./packageId")
                            package_id = node.text if node is not None else ""
                            supported_versions = root.xpath(
                                "./supportedVersions/li/text()"
                            )
                            node = root.find("./description")
                            description = node.text if node is not None else ""
                        except etree.XMLSyntaxError:
                            logger.warning(
                                f"Could not parse About.xml at {about_xml_path}"
                            )

                        preview_image_path = sub_folder / "About" / "Preview.png"

                        if name is not None:
                            data.append(
                                Mod(
                                    name,
                                    package_id,
                                    supported_versions,
                                    description,
                                    preview_image_path,
                                )
                            )

        self.signals.data_ready.emit(data)
        self.signals.finished.emit()
