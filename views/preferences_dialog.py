from typing import Optional, TYPE_CHECKING

from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QLabel,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QRadioButton,
)


if TYPE_CHECKING:
    from controllers.app_controller import AppController


class PreferencesDialog(QDialog):
    def __init__(
        self, app_controller: "AppController", parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)

        self.app_controller = app_controller

        close_shortcut = QShortcut(QKeySequence.StandardKey.Close, self)
        close_shortcut.activated.connect(self.close)

        self.setWindowTitle("Preferences")

        self.resize(768, 480)

        layout = QHBoxLayout(self)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.stacked_widget = QStackedWidget(self)
        layout.addWidget(self.stacked_widget)

        layout.setStretchFactor(self.list_widget, 2)  # 20% of the space
        layout.setStretchFactor(self.stacked_widget, 8)  # 80% of the space

        self._do_sorting_page()

        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        self.list_widget.setCurrentRow(0)

    def _do_sorting_page(self) -> None:
        self.list_widget.addItem("Sorting")

        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        page_layout.setContentsMargins(0, 0, 0, 0)

        sorting_group = QGroupBox("", page)  # No title set
        group_layout = QVBoxLayout(sorting_group)

        sorting_label = QLabel("Sort mods", sorting_group)
        group_layout.addWidget(sorting_label)

        alphabetical_button = QRadioButton("Alphabetically", sorting_group)
        alphabetical_button.setChecked(True)
        group_layout.addWidget(alphabetical_button)

        topological_button = QRadioButton("Topologically", sorting_group)
        group_layout.addWidget(topological_button)

        explanatory_text = (
            "Alphabetical sorting sorts mods alphabetically. "
            "If I knew what topological sorting did, I'd explain it here."
        )
        explanatory_label = QLabel(explanatory_text, sorting_group)
        explanatory_label.setWordWrap(True)
        group_layout.addWidget(explanatory_label)

        page_layout.addWidget(sorting_group)

        self.stacked_widget.addWidget(page)
