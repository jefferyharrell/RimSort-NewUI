from typing import Optional

from PySide6.QtCore import Qt
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
    QPushButton,
)

from models.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.settings = settings

        # Load settings and connect signals
        self._setup_settings()

        # Setup UI components
        self._setup_ui()

    def _setup_settings(self) -> None:
        """Load settings and connect related signals."""
        self.settings.load()
        self.settings.settings_changed.connect(self.on_settings_changed)

    def _setup_ui(self) -> None:
        """Setup main UI components."""
        self.setWindowTitle("Settings")
        self.resize(768, 480)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # List and Stacked Widgets layout
        list_and_stacked_layout = QHBoxLayout()

        self.list_widget = QListWidget(self)
        list_and_stacked_layout.addWidget(self.list_widget)

        self.stacked_widget = QStackedWidget(self)
        list_and_stacked_layout.addWidget(self.stacked_widget)

        list_and_stacked_layout.setStretchFactor(
            self.list_widget, 2
        )  # 20% of the space
        list_and_stacked_layout.setStretchFactor(
            self.stacked_widget, 8
        )  # 80% of the space

        self._do_sorting_page()

        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.list_widget.setCurrentRow(0)

        # Add the main layout to the dialog
        main_layout.addLayout(list_and_stacked_layout)

        # "Cancel" and "Apply" buttons layout
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Push buttons to the right

        # Cancel button
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        # Apply button
        self.apply_button = QPushButton("Apply", self)
        self.apply_button.setDefault(True)
        self.apply_button.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_button)

        # Add button layout to the main layout
        self.layout().addLayout(button_layout)

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

    def _apply_settings(self) -> None:
        self.settings.save()
        self.close()

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
