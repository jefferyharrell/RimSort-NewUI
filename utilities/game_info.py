from typing import Optional

from controllers.settings_controller import SettingsController
from utilities.system_info import SystemInfo


class GameInfo:
    _instance: Optional["GameInfo"] = None

    def __new__(
        cls, settings_controller: Optional[SettingsController] = None
    ) -> "GameInfo":
        if cls._instance is None:
            cls._instance = super(GameInfo, cls).__new__(cls)
            cls._instance._is_initialized = False
        return cls._instance

    def __init__(
        self, settings_controller: Optional[SettingsController] = None
    ) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        if settings_controller is None:
            raise ValueError(
                "GameInfo must be initialized once with a SettingsController."
            )

        self._version: str = ""

        if settings_controller.settings.game_location is not None:
            if SystemInfo().operating_system == SystemInfo.OperatingSystem.MACOS:
                version_path = (
                    settings_controller.settings.game_location / "version.txt"
                )
            else:
                version_path = (
                    settings_controller.settings.game_location.parent / "version.txt"
                )
            if version_path.exists() and version_path.is_file():
                version_text = version_path.read_text()
                self._version = version_text.strip()

        super().__init__()

        self._is_initialized: bool = True

    @property
    def version(self) -> str:
        return self._version
