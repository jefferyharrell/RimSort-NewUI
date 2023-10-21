from typing import Optional

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from utilities.system_info import SystemInfo


class AboutDialog(QWidget):
    close_window_hotkey = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(AboutDialog, self).__init__(parent)

        if SystemInfo().operating_system != SystemInfo.OperatingSystem.MACOS:
            self.setWindowTitle("About NewUI")

        image_label = QLabel()
        pixmap = QPixmap("resources/AppIcon_a.png").scaled(
            QSize(64, 64),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("NewUI")

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = label.font()
        font.setBold(True)
        label.setFont(font)

        # Create a QLabel for the copyright notice
        more_info_label = QLabel(
            "Version so-n-so whatever.0.0.0\n"
            "© 2023 blah blah blah\n"
            "All rights reserved."
        )
        more_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the font to a smaller size
        small_font = more_info_label.font()
        small_font.setPointSize(small_font.pointSize() - 1)
        more_info_label.setFont(small_font)

        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(image_label)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(more_info_label)

        self.setFixedSize(300, 200)

        self.setLayout(layout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.key() == Qt.Key.Key_W
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.close_window_hotkey.emit()
        super().keyPressEvent(event)
