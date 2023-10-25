from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from loguru import logger
from platformdirs import PlatformDirs


class AppInfo:
    _instance: Optional["AppInfo"] = None

    def __new__(cls, file_path: Optional[str] = None) -> "AppInfo":
        if not cls._instance:
            cls._instance = super(AppInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_path: Optional[str] = None) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        if file_path is None:
            raise ValueError("AppInfo must be initialized once with __file__.")

        self._application_folder = Path(file_path).resolve().parent

        self._app_name = "NewUI"
        self._app_version = "Version 0.0.0"
        self._app_copyright = "Copyright blah blah blah\nAll rights reserved."
        self._app_icon_path = Path(
            self._application_folder, "./resources/AppIcon_a.png"
        )
        self._app_icon_64x64_pixmap: Optional[QPixmap] = None

        platform_dirs = PlatformDirs(appname=self._app_name)
        self._user_data_folder = Path(platform_dirs.user_data_dir)
        logger.info(f"User data folder: {self._user_data_folder}")
        self._user_log_folder = Path(platform_dirs.user_log_dir)
        logger.info(f"User log folder: {self._user_log_folder}")

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
        if self._app_icon_64x64_pixmap is None:
            self._app_icon_64x64_pixmap = QPixmap(str(self._app_icon_path)).scaled(
                QSize(64, 64),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        return self._app_icon_64x64_pixmap

    @property
    def application_folder(self) -> Path:
        return self._application_folder

    @property
    def user_data_folder(self) -> Path:
        return self._user_data_folder

    @property
    def user_log_folder(self) -> Path:
        return self._user_log_folder
