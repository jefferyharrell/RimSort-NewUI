from typing import Optional, TYPE_CHECKING

from PySide6.QtCore import Qt
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

from models.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.settings = settings

        self.settings.settings_changed.connect(self.on_settings_changed)

        close_shortcut = QShortcut(QKeySequence.StandardKey.Close, self)
        close_shortcut.activated.connect(self.close)

        self.setWindowTitle("Settings")

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
        page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        page_layout.setContentsMargins(0, 0, 0, 0)

        sorting_group = QGroupBox("", page)  # No title set
        group_layout = QVBoxLayout(sorting_group)

        sorting_label = QLabel("Sort mods", sorting_group)
        group_layout.addWidget(sorting_label)

        self.alphabetical_button = QRadioButton("Alphabetically", sorting_group)
        self.alphabetical_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        group_layout.addWidget(self.alphabetical_button)

        self.topological_button = QRadioButton("Topologically", sorting_group)
        self.topological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        group_layout.addWidget(self.topological_button)

        self.radiological_button = QRadioButton("Radiologically", sorting_group)
        self.radiological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        group_layout.addWidget(self.radiological_button)

        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.topological_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.RADIOLOGICAL:
            self.radiological_button.setChecked(True)

        explanatory_text = (
            "Alphabetical sorting sorts mods alphabetically. "
            "If I knew what topological sorting did, I'd explain it here."
        )
        explanatory_label = QLabel(explanatory_text, sorting_group)
        explanatory_label.setWordWrap(True)
        group_layout.addWidget(explanatory_label)

        page_layout.addWidget(sorting_group)

        self.stacked_widget.addWidget(page)

    def _on_sorting_algorithm_button_toggled(self, checked: bool) -> None:
        if checked:
            if self.sender() == self.alphabetical_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.ALPHABETICAL
            elif self.sender() == self.topological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
            elif self.sender() == self.radiological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.RADIOLOGICAL

    def on_settings_changed(self) -> None:
        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.topological_button.setChecked(True)
