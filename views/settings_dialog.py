from pathlib import Path
from typing import Optional, Callable, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QApplication,
    QTabWidget,
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

        self.default_font = QApplication.font()
        self.emphasis_font = self.default_font
        self.emphasis_font.setWeight(QFont.Weight.Bold)

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Initialize the QTabWidget
        self._tab_widget = QTabWidget(self)
        main_layout.addWidget(self._tab_widget)

        self._do_general_tab()
        self._do_sorting_tab()

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

    def _do_general_tab(self) -> None:
        tab = QWidget(self)
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Helper function to create a QHBoxLayout with a label, spacer, and button
        def create_hbox_layout(
            label_text: str, settings_value: str, button_callback: Callable[[], None]
        ) -> Tuple[QHBoxLayout, QLabel]:
            label = QLabel(settings_value)
            label.setWordWrap(True)
            font_metrics = label.fontMetrics()
            min_height = font_metrics.lineSpacing() * 3
            label.setMinimumHeight(min_height)

            spacer_width = 12
            spacer = QSpacerItem(
                spacer_width, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
            )

            button = QPushButton("Choose…")
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
        game_location_label = QLabel("Game Location")
        game_location_label.setFont(self.emphasis_font)
        tab_layout.addWidget(game_location_label)
        game_location_layout, self.game_location = create_hbox_layout(
            "Game Location", self.settings.game_location, self._on_choose_game_location
        )
        tab_layout.addLayout(game_location_layout)

        # Config Folder Location Row
        config_folder_location_label = QLabel("Config Folder Location")
        config_folder_location_label.setFont(self.emphasis_font)
        tab_layout.addWidget(config_folder_location_label)
        config_folder_location_layout, self.config_folder_location = create_hbox_layout(
            "Config Folder Location",
            self.settings.config_folder_location,
            self._on_choose_config_folder_location,
        )
        tab_layout.addLayout(config_folder_location_layout)

        # Steam Mods Folder Location Row
        steam_mods_folder_location_label = QLabel("Steam Mods Folder Location")
        steam_mods_folder_location_label.setFont(self.emphasis_font)
        tab_layout.addWidget(steam_mods_folder_location_label)
        (
            steam_mods_folder_location_layout,
            self.steam_mods_folder_location,
        ) = create_hbox_layout(
            "Steam Mods Folder Location",
            self.settings.steam_mods_folder_location,
            self._on_choose_steam_mods_folder_location,
        )
        tab_layout.addLayout(steam_mods_folder_location_layout)

        # Local Mods Folder Location Row
        local_mods_folder_location_label = QLabel("Local Mods Folder Location")
        local_mods_folder_location_label.setFont(self.emphasis_font)
        tab_layout.addWidget(local_mods_folder_location_label)
        (
            local_mods_folder_location_layout,
            self.local_mods_folder_location,
        ) = create_hbox_layout(
            "Local Mods Folder Location",
            self.settings.local_mods_folder_location,
            self._on_choose_local_mods_folder_location,
        )
        tab_layout.addLayout(local_mods_folder_location_layout)

        # Create a QHBoxLayout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)

        # Create the "Clear" button and connect its signal
        clear_button = QPushButton("Clear", tab)
        clear_button.clicked.connect(self._on_clear_button_clicked)
        buttons_layout.addWidget(clear_button)

        # Create the "Autodetect" button and connect its signal
        autodetect_button = QPushButton("Autodetect", tab)
        autodetect_button.clicked.connect(self._on_autodetect_button_clicked)
        buttons_layout.addWidget(autodetect_button)

        # Add the buttons layout to the main QVBoxLayout
        tab_layout.addLayout(buttons_layout)

        self._tab_widget.addTab(tab, "General")

    def _do_sorting_tab(self) -> None:
        tab = QWidget(self)
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        sorting_label = QLabel("Sort Mods")
        sorting_label.setFont(self.emphasis_font)
        tab_layout.addWidget(sorting_label)

        self.alphabetical_button = QRadioButton("Alphabetically")
        self.alphabetical_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        tab_layout.addWidget(self.alphabetical_button)

        self.topological_button = QRadioButton("Topologically")
        self.topological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        tab_layout.addWidget(self.topological_button)

        self.radiological_button = QRadioButton("Radiologically")
        self.radiological_button.toggled.connect(
            self._on_sorting_algorithm_button_toggled
        )
        tab_layout.addWidget(self.radiological_button)

        if self.settings.sorting_algorithm == Settings.SortingAlgorithm.ALPHABETICAL:
            self.alphabetical_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.TOPOLOGICAL:
            self.topological_button.setChecked(True)
        elif self.settings.sorting_algorithm == Settings.SortingAlgorithm.RADIOLOGICAL:
            self.radiological_button.setChecked(True)

        tab_layout.addStretch(1)  # Push buttons to the right

        explanatory_text = (
            "Alphabetical sorting sorts mods alphabetically. "
            "If I knew what topological sorting did, I'd explain it here. "
            "Radiological sorting isn't a real thing. It's just there for demonstration purposes."
        )
        explanatory_label = QLabel(explanatory_text)
        explanatory_label.setWordWrap(True)
        tab_layout.addWidget(explanatory_label)

        self._tab_widget.addTab(tab, "Sorting")

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
