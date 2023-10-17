import platform
from enum import Enum, unique, auto
from typing import Optional


class SystemInfo:
    """
    A class that provides information about the system, such as the operating system and architecture.
    """

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

    def __init__(self) -> None:
        """Prevents instantiation of the static SystemInfo class"""
        raise TypeError("SystemInfo class cannot be instantiated")

    @classmethod
    def operating_system(cls) -> Optional["SystemInfo.OperatingSystem"]:
        """
        Returns the current operating system.

        :raises UnsupportedOperatingSystemError: If the detected OS is not supported.
        """
        if cls._operating_system is None:
            if platform.system() in ["Windows"]:
                cls._operating_system = SystemInfo.OperatingSystem.WINDOWS
            elif platform.system() in ["Linux"]:
                cls._operating_system = SystemInfo.OperatingSystem.LINUX
            elif platform.system() in ["Darwin"]:
                cls._operating_system = SystemInfo.OperatingSystem.MACOS
            else:
                raise UnsupportedOperatingSystemError(
                    f"Unsupported operating system detected: {platform.system()}."
                )
        return cls._operating_system

    @classmethod
    def architecture(cls) -> Optional["SystemInfo.Architecture"]:
        """
        Returns the architecture of the system.

        :raises UnsupportedArchitectureError: If the detected architecture is not supported.
        """
        if cls._architecture is None:
            if platform.machine() in ["x86_64", "AMD64"]:
                cls._architecture = SystemInfo.Architecture.X64
            elif platform.machine() in ["arm64", "aarch64"]:
                cls._architecture = SystemInfo.Architecture.ARM64
            else:
                raise UnsupportedArchitectureError(
                    f"Unsupported architecture detected: {platform.machine()}."
                )
        return cls._architecture


class UnsupportedOperatingSystemError(Exception):
    """Raised when an unsupported operating system is detected."""

    pass


class UnsupportedArchitectureError(Exception):
    """Raised when an unsupported architecture is detected."""

    pass
