from typing import Optional

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from utilities.gui_info import GUIInfo
from utilities.system_info import SystemInfo


class AboutDialog(QWidget):
    close_window_hotkey = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(AboutDialog, self).__init__(parent)

        if SystemInfo().operating_system != SystemInfo.OperatingSystem.MACOS:
            self.setWindowTitle("About NewUI")

        self.app_icon_label = QLabel()
        pixmap = QPixmap("resources/AppIcon_a.png").scaled(
            QSize(64, 64),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.app_icon_label.setPixmap(pixmap)
        self.app_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_name_label = QLabel("NewUI")

        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_name_label.setFont(GUIInfo().emphasis_font)

        self.more_info_label = QLabel(
            "Version so-n-so whatever.0.0.0\n"
            "© 2023 blah blah blah\n"
            "All rights reserved."
        )
        self.more_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the font to a smaller size
        small_font = self.more_info_label.font()
        small_font.setPointSize(small_font.pointSize() - 1)
        self.more_info_label.setFont(small_font)

        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.app_icon_label)
        layout.addWidget(self.app_name_label)
        layout.addStretch(1)
        layout.addWidget(self.more_info_label)

        self.setFixedSize(300, 200)

        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.key() == Qt.Key.Key_W
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.close_window_hotkey.emit()
        super().keyPressEvent(event)
