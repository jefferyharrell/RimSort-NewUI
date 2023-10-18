from pathlib import Path
from typing import Optional, Callable, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
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
from utilities.system_info import SystemInfo


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

        group_box = QGroupBox(page)
        group_box_layout = QVBoxLayout(group_box)
        group_box_layout.setSpacing(0)

        # Helper function to create a QHBoxLayout with a label, spacer, and button
        def create_hbox_layout(
            label_text: str, settings_value: str, button_callback: Callable[[], None]
        ) -> Tuple[QHBoxLayout, QLabel]:
            label = QLabel(settings_value, group_box)
            label.setWordWrap(True)
            font_metrics = label.fontMetrics()
            min_height = font_metrics.lineSpacing() * 3
            label.setMinimumHeight(min_height)

            spacer_width = 12
            spacer = QSpacerItem(
                spacer_width, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
            )

            button = QPushButton("Choose…", group_box)
            button.setFixedWidth(button.sizeHint().width())
            button.clicked.connect(button_callback)

            hbox_layout = QHBoxLayout()
            hbox_layout.addWidget(label)
            hbox_layout.addSpacerItem(spacer)
            hbox_layout.addWidget(button)

            return (
                hbox_layout,
                label,
            )  # Return the layout and label for further use if needed

        # Game Location Row
        game_location_label = QLabel("Game Location", group_box)
        font = game_location_label.font()
        font.setWeight(QFont.Weight.DemiBold)
        game_location_label.setFont(font)
        group_box_layout.addWidget(game_location_label)
        game_location_layout, self.game_location = create_hbox_layout(
            "Game Location", self.settings.game_location, self._on_choose_game_location
        )
        group_box_layout.addLayout(game_location_layout)

        # Config Folder Location Row
        config_folder_location_label = QLabel("Config Folder Location", group_box)
        font = config_folder_location_label.font()
        font.setWeight(QFont.Weight.DemiBold)
        config_folder_location_label.setFont(font)
        group_box_layout.addWidget(config_folder_location_label)
        config_folder_location_layout, self.config_folder_location = create_hbox_layout(
            "Config Folder Location",
            self.settings.config_folder_location,
            self._on_choose_config_folder_location,
        )
        group_box_layout.addLayout(config_folder_location_layout)

        # Steam Mods Folder Location Row
        steam_mods_folder_location_label = QLabel(
            "Steam Mods Folder Location", group_box
        )
        font = steam_mods_folder_location_label.font()
        font.setWeight(QFont.Weight.DemiBold)
        steam_mods_folder_location_label.setFont(font)
        group_box_layout.addWidget(steam_mods_folder_location_label)
        (
            steam_mods_folder_location_layout,
            self.steam_mods_folder_location,
        ) = create_hbox_layout(
            "Steam Mods Folder Location",
            self.settings.steam_mods_folder_location,
            self._on_choose_steam_mods_folder_location,
        )
        group_box_layout.addLayout(steam_mods_folder_location_layout)

        # Local Mods Folder Location Row
        local_mods_folder_location_label = QLabel(
            "Local Mods Folder Location", group_box
        )
        font = local_mods_folder_location_label.font()
        font.setWeight(QFont.Weight.DemiBold)
        local_mods_folder_location_label.setFont(font)
        group_box_layout.addWidget(local_mods_folder_location_label)
        (
            local_mods_folder_location_layout,
            self.local_mods_folder_location,
        ) = create_hbox_layout(
            "Local Mods Folder Location",
            self.settings.local_mods_folder_location,
            self._on_choose_local_mods_folder_location,
        )
        group_box_layout.addLayout(local_mods_folder_location_layout)

        # Add the QGroupBox to the main QVBoxLayout
        page_layout.addWidget(group_box)

        # Create a QHBoxLayout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)

        # Create the "Clear" button and connect its signal
        clear_button = QPushButton("Clear", page)
        clear_button.clicked.connect(self._on_clear_button_clicked)
        buttons_layout.addWidget(clear_button)

        # Create the "Autodetect" button and connect its signal
        autodetect_button = QPushButton("Autodetect", page)
        autodetect_button.clicked.connect(self._on_autodetect_button_clicked)
        buttons_layout.addWidget(autodetect_button)

        # Add the buttons layout to the main QVBoxLayout
        page_layout.addLayout(buttons_layout)

        self.stacked_widget.addWidget(page)

    def _do_sorting_page(self) -> None:
        self.list_widget.addItem("Sorting")

        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        page_layout.setContentsMargins(0, 0, 0, 0)

        sorting_group = QGroupBox("", page)  # No title set
        group_layout = QVBoxLayout(sorting_group)

        sorting_label = QLabel("Sort Mods", sorting_group)
        font = sorting_label.font()
        font.setWeight(QFont.Weight.DemiBold)
        sorting_label.setFont(font)
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

    def _on_choose_steam_mods_folder_location(self) -> None:
        steam_mods_folder_location = QFileDialog.getExistingDirectory(self)
        if steam_mods_folder_location != "":
            self.settings.steam_mods_folder_location = steam_mods_folder_location

    def _on_choose_local_mods_folder_location(self) -> None:
        local_mods_folder_location = QFileDialog.getExistingDirectory(self)
        if local_mods_folder_location != "":
            self.settings.local_mods_folder_location = local_mods_folder_location

    def _on_autodetect_button_clicked(self) -> None:
        if SystemInfo.operating_system() == SystemInfo.OperatingSystem.WINDOWS:
            self._autodetect_locations_windows()
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.LINUX:
            self._autodetect_locations_linux()
        elif SystemInfo.operating_system() == SystemInfo.OperatingSystem.MACOS:
            self._autodetect_locations_macos()

    def _autodetect_locations_windows(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

    def _autodetect_locations_linux(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

    def _autodetect_locations_macos(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

        home_folder_path: Path = Path.home()
        steam_folder_candidate_path: Path = (
            home_folder_path / "Library/Application Support/Steam"
        )
        app_support_candidate_path: Path = Path.home() / "Library/Application Support"

        game_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/common/RimWorld/RimWorldMac.app"
        )
        if game_location_candidate.exists():
            self.settings.game_location = str(game_location_candidate)

        config_folder_location_candidate: Path = (
            app_support_candidate_path / "RimWorld/Config"
        )
        if config_folder_location_candidate.exists():
            self.settings.config_folder_location = str(config_folder_location_candidate)

        steam_mods_folder_location_candidate: Path = (
            steam_folder_candidate_path / "steamapps/workshop/content/294100"
        )
        if steam_mods_folder_location_candidate.exists():
            self.settings.steam_mods_folder_location = str(
                steam_mods_folder_location_candidate
            )

        local_mods_folder_location_candidate: Path = game_location_candidate / "Mods"
        if local_mods_folder_location_candidate.exists():
            self.settings.local_mods_folder_location = str(
                local_mods_folder_location_candidate
            )

    def _on_clear_button_clicked(self) -> None:
        self.settings.game_location = ""
        self.settings.config_folder_location = ""
        self.settings.steam_mods_folder_location = ""
        self.settings.local_mods_folder_location = ""

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
        self.steam_mods_folder_location.setText(
            self.settings.steam_mods_folder_location
        )
        self.local_mods_folder_location.setText(
            self.settings.local_mods_folder_location
        )

        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.topological_button.setChecked(True)
