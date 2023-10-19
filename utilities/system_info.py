import platform
from enum import Enum, unique, auto
from typing import Optional


class SystemInfo:
    """
    A singleton class that provides information about the system.
    """

    _instance: Optional["SystemInfo"] = None
    _operating_system: Optional["SystemInfo.OperatingSystem"] = None
    _architecture: Optional["SystemInfo.Architecture"] = None

    @unique
    class OperatingSystem(Enum):
        """Represents the operating system of the system."""

        WINDOWS = auto()
        LINUX = auto()
        MACOS = auto()

    @unique
    class Architecture(Enum):
        """Represents the architecture of the system."""

        X86 = auto()
        X64 = auto()
        ARM64 = auto()

    def __new__(cls) -> "SystemInfo":
        if not cls._instance:
            cls._instance = super(SystemInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # Initialize _operating_system
        if platform.system() in ["Windows"]:
            self._operating_system = SystemInfo.OperatingSystem.WINDOWS
        elif platform.system() in ["Linux"]:
            self._operating_system = SystemInfo.OperatingSystem.LINUX
        elif platform.system() in ["Darwin"]:
            self._operating_system = SystemInfo.OperatingSystem.MACOS
        else:
            raise UnsupportedOperatingSystemError(
                f"Unsupported operating system detected: {platform.system()}."
            )

        # Initialize _architecture
        if platform.machine() in ["x86_64", "AMD64"]:
            self._architecture = SystemInfo.Architecture.X64
        elif platform.machine() in ["arm64", "aarch64"]:
            self._architecture = SystemInfo.Architecture.ARM64
        else:
            raise UnsupportedArchitectureError(
                f"Unsupported architecture detected: {platform.machine()}."
            )

    @property
    def operating_system(self) -> Optional["SystemInfo.OperatingSystem"]:
        return self._operating_system

    @property
    def architecture(self) -> Optional["SystemInfo.Architecture"]:
        return self._architecture


class UnsupportedOperatingSystemError(Exception):
    """Raised when an unsupported operating system is detected."""

    pass


class UnsupportedArchitectureError(Exception):
    """Raised when an unsupported architecture is detected."""

    pass
