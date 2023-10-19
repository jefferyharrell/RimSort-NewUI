from typing import Optional

from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import QApplication


class GUIInfo:
    _instance: Optional["GUIInfo"] = None

    def __new__(cls) -> "GUIInfo":
        if not cls._instance:
            cls._instance = super(GUIInfo, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return

        self._default_font = QApplication.font()

        self._emphasis_font = QFont(self._default_font)
        self._emphasis_font.setWeight(QFont.Weight.Bold)

        self._default_font_line_height = QFontMetrics(self._default_font).lineSpacing()

        self._is_initialized: bool = True

    @property
    def default_font(self) -> QFont:
        return self._default_font

    @property
    def emphasis_font(self) -> QFont:
        return self._emphasis_font

    @property
    def default_font_line_height(self) -> int:
        return self._default_font_line_height
