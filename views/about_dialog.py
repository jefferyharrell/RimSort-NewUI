from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication


class AboutDialog(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super(AboutDialog, self).__init__(parent)

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
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(more_info_label)

        self.setFixedSize(300, 200)

        self.setLayout(layout)

    def showEvent(self, event):
        screen_geometry = self.screen().geometry()
        screen_center_x = screen_geometry.width() / 2
        screen_center_y = screen_geometry.height() / 2

        move_x = screen_center_x - self.width() / 2
        move_y = (screen_center_y - self.height()) / 1.6
        self.move(int(move_x), int(move_y))

        super().showEvent(event)
