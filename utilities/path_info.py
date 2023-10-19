from pathlib import Path
from typing import Optional

from platformdirs import user_log_dir


class PathInfo:
    """
    A class that provides information about the paths of files and folders.
    """

    _instance: Optional["PathInfo"] = None

    def __new__(cls, file_path: Optional[str] = None) -> "PathInfo":
        if not cls._instance:
            cls._instance = super(PathInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_path: Optional[str] = None) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        if file_path is None:
            raise ValueError("PathInfo must be initialized with __file__.")

        self._application_folder = Path(file_path).resolve().parent
        self._log_folder = Path(user_log_dir())

        self._is_initialized: bool = True

    @property
    def application_folder(self) -> Path:
        return self._application_folder

    @property
    def log_folder(self) -> Path:
        return self._log_folder
