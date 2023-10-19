from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QApplication,
    QTabWidget,
    QCheckBox,
)


class SettingsDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup main UI components."""
        self.setWindowTitle("Settings")
        self.resize(800, 600)

        self.default_font = QApplication.font()
        self.emphasis_font = self.default_font
        self.emphasis_font.setWeight(QFont.Weight.Bold)
        self.default_font_line_height = QFontMetrics(self.default_font).lineSpacing()

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Initialize the QTabWidget
        self._tab_widget = QTabWidget(self)
        main_layout.addWidget(self._tab_widget)

        # Initialize the tabs
        self._do_general_tab()
        self._do_sorting_tab()
        self._do_advanced_tab()

        # "Cancel" and "Apply" buttons layout
        button_layout = QHBoxLayout()

        self.global_reset_to_defaults_button = QPushButton("Reset to Defaults", self)
        button_layout.addWidget(self.global_reset_to_defaults_button)

        button_layout.addStretch(1)  # Push buttons to the right

        # Cancel button
        self.global_cancel_button = QPushButton("Cancel", self)
        button_layout.addWidget(self.global_cancel_button)

        # Apply button
        self.global_apply_button = QPushButton("Apply", self)
        self.global_apply_button.setEnabled(False)
        button_layout.addWidget(self.global_apply_button)

        # OK button
        self.global_ok_button = QPushButton("OK", self)
        self.global_ok_button.setDefault(True)
        button_layout.addWidget(self.global_ok_button)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

    def _do_general_tab(self) -> None:
        tab = QWidget(self)
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._do_game_location_area(tab_layout)
        self._do_config_folder_location_area(tab_layout)
        self._do_steam_mods_folder_location_area(tab_layout)
        self._do_local_mods_folder_location_area(tab_layout)

        # Push the buttons to the bottom
        tab_layout.addStretch(1)

        # Create a QHBoxLayout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)

        # Create the "Clear" button and connect its signal
        self.general_clear_button = QPushButton("Clear", tab)
        buttons_layout.addWidget(self.general_clear_button)

        # Create the "Autodetect" button and connect its signal
        self.general_autodetect_button = QPushButton("Autodetect", tab)
        buttons_layout.addWidget(self.general_autodetect_button)

        # Add the buttons layout to the main QVBoxLayout
        tab_layout.addLayout(buttons_layout)

        self._tab_widget.addTab(tab, "General")

    def _do_game_location_area(self, tab_layout: QVBoxLayout) -> None:
        section_label = QLabel("Game Location")
        section_label.setFont(self.emphasis_font)
        tab_layout.addWidget(section_label)

        self.game_location_value_label = QLabel()
        self.game_location_value_label.setWordWrap(True)
        self.game_location_value_label.setMinimumHeight(
            self.default_font_line_height * 2
        )

        self.game_location_choose_button = QPushButton("Choose…")
        self.game_location_choose_button.setFixedWidth(
            self.game_location_choose_button.sizeHint().width()
        )

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.game_location_value_label)
        box_layout.addSpacerItem(
            QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        )
        box_layout.addWidget(self.game_location_choose_button)

        tab_layout.addLayout(box_layout)

    def _do_config_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        section_label = QLabel("Config Folder Location")
        section_label.setFont(self.emphasis_font)
        tab_layout.addWidget(section_label)

        self.config_folder_location_value_label = QLabel()
        self.config_folder_location_value_label.setWordWrap(True)
        self.config_folder_location_value_label.setMinimumHeight(
            self.default_font_line_height * 2
        )

        self.config_folder_location_choose_button = QPushButton("Choose…")
        self.config_folder_location_choose_button.setFixedWidth(
            self.config_folder_location_choose_button.sizeHint().width()
        )

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.config_folder_location_value_label)
        box_layout.addSpacerItem(
            QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        )
        box_layout.addWidget(self.config_folder_location_choose_button)

        tab_layout.addLayout(box_layout)

    def _do_steam_mods_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        section_label = QLabel("Steam Mods Folder Location")
        section_label.setFont(self.emphasis_font)
        tab_layout.addWidget(section_label)

        self.steam_mods_folder_location_value_label = QLabel()
        self.steam_mods_folder_location_value_label.setWordWrap(True)
        self.steam_mods_folder_location_value_label.setMinimumHeight(
            self.default_font_line_height * 2
        )

        self.steam_mods_folder_location_choose_button = QPushButton("Choose…")
        self.steam_mods_folder_location_choose_button.setFixedWidth(
            self.steam_mods_folder_location_choose_button.sizeHint().width()
        )

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.steam_mods_folder_location_value_label)
        box_layout.addSpacerItem(
            QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        )
        box_layout.addWidget(self.steam_mods_folder_location_choose_button)

        tab_layout.addLayout(box_layout)

    def _do_local_mods_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        section_label = QLabel("Local Mods Folder Location")
        section_label.setFont(self.emphasis_font)
        tab_layout.addWidget(section_label)

        self.local_mods_folder_location_value_label = QLabel()
        self.local_mods_folder_location_value_label.setWordWrap(True)
        self.local_mods_folder_location_value_label.setMinimumHeight(
            self.default_font_line_height * 2
        )

        self.local_mods_folder_location_choose_button = QPushButton("Choose…")
        self.local_mods_folder_location_choose_button.setFixedWidth(
            self.local_mods_folder_location_choose_button.sizeHint().width()
        )

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.local_mods_folder_location_value_label)
        box_layout.addSpacerItem(
            QSpacerItem(12, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        )
        box_layout.addWidget(self.local_mods_folder_location_choose_button)

        tab_layout.addLayout(box_layout)

    def _do_sorting_tab(self) -> None:
        tab = QWidget(self)
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        sorting_label = QLabel("Sort Mods")
        sorting_label.setFont(self.emphasis_font)
        tab_layout.addWidget(sorting_label)

        self.alphabetical_button = QRadioButton("Alphabetically")
        tab_layout.addWidget(self.alphabetical_button)

        self.topological_button = QRadioButton("Topologically")
        tab_layout.addWidget(self.topological_button)

        self.radiological_button = QRadioButton("Radiologically")
        tab_layout.addWidget(self.radiological_button)

        tab_layout.addStretch(1)

        explanatory_text = (
            "Alphabetical sorting sorts mods alphabetically. "
            "If I knew what topological sorting did, I'd explain it here. "
            "Radiological sorting isn't a real thing. It's just there for demonstration purposes."
        )
        explanatory_label = QLabel(explanatory_text)
        explanatory_label.setWordWrap(True)
        tab_layout.addWidget(explanatory_label)

        self._tab_widget.addTab(tab, "Sorting")

    def _do_advanced_tab(self) -> None:
        tab = QWidget(self)
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.debug_logging_checkbox = QCheckBox("Enable debug logging", tab)
        tab_layout.addWidget(self.debug_logging_checkbox)

        self._tab_widget.addTab(tab, "Advanced")
