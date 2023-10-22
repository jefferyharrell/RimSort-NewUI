from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt

from utilities.path_info import PathInfo


class AppInfo:
    _instance: Optional["AppInfo"] = None

    def __new__(cls) -> "AppInfo":
        if not cls._instance:
            cls._instance = super(AppInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        self._app_name = "NewUI"
        self._app_version = "Version 0.0.0"
        self._app_copyright = "Copyright blah blah blah\nAll rights reserved."
        self._app_icon_path = Path(
            PathInfo().application_folder, "./resources/AppIcon_a.png"
        )
        self._app_icon_64x64_pixmap = QPixmap(str(self._app_icon_path)).scaled(
            QSize(64, 64),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self._is_initialized: bool = True

    @property
    def app_name(self) -> str:
        return self._app_name

    @property
    def app_version(self) -> str:
        return self._app_version

    @property
    def app_copyright(self) -> str:
        return self._app_copyright

    @property
    def app_icon_path(self) -> Path:
        return self._app_icon_path

    @property
    def app_icon_64x64_pixmap(self) -> QPixmap:
        return self._app_icon_64x64_pixmap
