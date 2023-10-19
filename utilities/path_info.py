from pathlib import Path
from typing import Optional

from platformdirs import user_log_dir


class PathInfo:
    """
    A singleton class that provides information about the paths of files and folders.

    This class should be initialized once with the __file__ attribute to set the application's root directory.
    Subsequent accesses to the class will use the already initialized instance.
    """

    _instance: Optional["PathInfo"] = None

    def __new__(cls, file_path: Optional[str] = None) -> "PathInfo":
        """
        Create a new instance or return the existing one.

        :param file_path: The path to the current file, typically __file__.
        :return: An instance of PathInfo.
        """
        if not cls._instance:
            cls._instance = super(PathInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initialize the PathInfo instance.

        :param file_path: The path to the current file, typically __file__.
        :raises ValueError: If file_path is not provided.
        """
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        if file_path is None:
            raise ValueError("PathInfo must be initialized with __file__.")

        self._application_folder = Path(file_path).resolve().parent
        self._user_log_folder = Path(user_log_dir())

        self._is_initialized: bool = True

    @property
    def application_folder(self) -> Path:
        return self._application_folder

    @property
    def user_log_folder(self) -> Path:
        return self._user_log_folder
