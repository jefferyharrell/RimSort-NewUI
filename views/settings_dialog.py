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
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
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

        self._do_general_page()
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
        main_layout.addLayout(button_layout)

    def _do_general_page(self) -> None:
        self.list_widget.addItem("General")

        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        page_layout.setContentsMargins(0, 0, 0, 0)

        # Create a QGroupBox without a title
        group_box = QGroupBox(page)

        # Create a QVBoxLayout for the QGroupBox to hold the label and the QHBoxLayout
        group_box_layout = QVBoxLayout(group_box)
        group_box_layout.setSpacing(0)

        # Add a label at the top of the QGroupBox
        game_location_label = QLabel("Game Location", group_box)
        group_box_layout.addWidget(game_location_label)

        # Create a QHBoxLayout
        hbox_layout = QHBoxLayout()

        # Add a label to the left of the QHBoxLayout
        self.game_location = QLabel(self.settings.game_location, group_box)
        self.game_location.setWordWrap(True)
        font_metrics = self.game_location.fontMetrics()
        desired_line_count = 3
        min_height = font_metrics.lineSpacing() * desired_line_count
        self.game_location.setMinimumHeight(min_height)
        hbox_layout.addWidget(self.game_location)

        # Add a fixed-width spacer
        desired_width = 12
        spacer = QSpacerItem(desired_width, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        hbox_layout.addSpacerItem(spacer)

        # Add a button to the right of the QHBoxLayout
        game_location_choose_button = QPushButton("Choose…", group_box)
        button_width = game_location_choose_button.sizeHint().width()
        game_location_choose_button.setFixedWidth(button_width)
        game_location_choose_button.clicked.connect(self._on_choose_game_location)
        hbox_layout.addWidget(game_location_choose_button)

        # Add the QHBoxLayout to the QVBoxLayout of the QGroupBox
        group_box_layout.addLayout(hbox_layout)

        # Second row: Config Folder Location

        # Add a label at the top of the QGroupBox for the config folder location
        config_folder_location_label = QLabel("Config Folder Location", group_box)
        group_box_layout.addWidget(config_folder_location_label)

        # Create another QHBoxLayout for the config folder location
        hbox_layout_config = QHBoxLayout()

        # Add a label to the left of the QHBoxLayout for the config folder location
        self.config_folder_location = QLabel(
            self.settings.config_folder_location, group_box
        )
        self.config_folder_location.setWordWrap(True)
        font_metrics = self.config_folder_location.fontMetrics()
        desired_line_count = 3
        min_height = font_metrics.lineSpacing() * desired_line_count
        self.config_folder_location.setMinimumHeight(min_height)
        hbox_layout_config.addWidget(self.config_folder_location)

        # Add a fixed-width spacer
        desired_width = 12
        spacer = QSpacerItem(desired_width, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        hbox_layout_config.addSpacerItem(spacer)

        # Add another "Choose…" button to the right of the QHBoxLayout for the config folder location
        config_folder_location_choose_button = QPushButton("Choose…", group_box)
        button_width_config = config_folder_location_choose_button.sizeHint().width()
        config_folder_location_choose_button.setFixedWidth(button_width_config)
        config_folder_location_choose_button.clicked.connect(
            self._on_choose_config_folder_location
        )
        hbox_layout_config.addWidget(config_folder_location_choose_button)

        # Add the QHBoxLayout for the config folder location to the QVBoxLayout of the QGroupBox
        group_box_layout.addLayout(hbox_layout_config)

        # Add the QGroupBox to the main QVBoxLayout
        page_layout.addWidget(group_box)

        self.stacked_widget.addWidget(page)

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

    def _on_choose_game_location(self) -> None:
        game_location, _ = QFileDialog.getOpenFileName(self)
        if game_location != "":
            self.settings.game_location = game_location

    def _on_choose_config_folder_location(self) -> None:
        config_folder_location = QFileDialog.getExistingDirectory(self)
        if config_folder_location != "":
            self.settings.config_folder_location = config_folder_location

    def _on_sorting_algorithm_button_toggled(self, checked: bool) -> None:
        if checked:
            if self.sender() == self.alphabetical_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.ALPHABETICAL
            elif self.sender() == self.topological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.TOPOLOGICAL
            elif self.sender() == self.radiological_button:
                self.settings.sorting_algorithm = Settings.SortingAlgorithm.RADIOLOGICAL

    def on_settings_changed(self) -> None:
        self.game_location.setText(self.settings.game_location)
        self.config_folder_location.setText(self.settings.config_folder_location)
        # self.steam_mods_folder_location.setText(self.settings.steam_mods_folder_location)
        # self.local_mods_folder_location.setText(self.settings.local_mods_folder_location)

        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.topological_button.setChecked(True)
