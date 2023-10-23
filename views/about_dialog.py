from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from utilities.app_info import AppInfo
from utilities.gui_info import GUIInfo
from utilities.system_info import SystemInfo


class AboutDialog(QWidget):
    close_window_hotkey = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(AboutDialog, self).__init__(parent)

        if SystemInfo().operating_system != SystemInfo.OperatingSystem.MACOS:
            self.setWindowTitle(f"About {AppInfo().app_name}")

        self.app_icon_label = QLabel()
        self.app_icon_label.setPixmap(AppInfo().app_icon_64x64_pixmap)
        self.app_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_name_label = QLabel(AppInfo().app_name)
        self.app_name_label.setFont(GUIInfo().emphasis_font)
        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_version_label = QLabel(AppInfo().app_version)
        self.app_version_label.setFont(GUIInfo().smaller_font)
        self.app_version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.app_copyright_label = QLabel(AppInfo().app_copyright)
        self.app_copyright_label.setFont(GUIInfo().smaller_font)
        self.app_copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.app_icon_label)
        layout.addWidget(self.app_name_label)
        layout.addStretch(1)
        layout.addWidget(self.app_version_label)
        layout.addWidget(self.app_copyright_label)

        self.setFixedSize(300, 200)

        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.key() == Qt.Key.Key_W
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.close_window_hotkey.emit()
        super().keyPressEvent(event)
