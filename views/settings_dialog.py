from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QCheckBox,
    QLineEdit,
    QGroupBox,
    QToolButton,
    QBoxLayout,
)

from utilities.gui_info import GUIInfo


class SettingsDialog(QDialog):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Initialize the QTabWidget
        self._tab_widget = QTabWidget()
        main_layout.addWidget(self._tab_widget)

        # Initialize the tabs
        self._do_locations_tab()
        self._do_databases_tab()
        self._do_sorting_tab()
        self._do_steamcmd_tab()
        self._do_todds_tab()
        self._do_advanced_tab()

        # "Cancel" and "Apply" buttons layout
        button_layout = QHBoxLayout()

        self.global_reset_to_defaults_button = QPushButton("Reset to Defaults", self)
        button_layout.addWidget(self.global_reset_to_defaults_button)

        button_layout.addStretch(1)  # Push buttons to the right

        # Cancel button
        self.global_cancel_button = QPushButton("Cancel", self)
        button_layout.addWidget(self.global_cancel_button)

        # OK button
        self.global_ok_button = QPushButton("OK", self)
        self.global_ok_button.setDefault(True)
        button_layout.addWidget(self.global_ok_button)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

    def _do_locations_tab(self) -> None:
        tab = QWidget()
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
        self.locations_clear_button = QPushButton("Clear", tab)
        buttons_layout.addWidget(self.locations_clear_button)

        # Create the "Autodetect" button and connect its signal
        self.locations_autodetect_button = QPushButton("Autodetect", tab)
        buttons_layout.addWidget(self.locations_autodetect_button)

        # Add the buttons layout to the main QVBoxLayout
        tab_layout.addLayout(buttons_layout)

        self._tab_widget.addTab(tab, "Locations")

    def _do_game_location_area(self, tab_layout: QVBoxLayout) -> None:
        header_layout = QHBoxLayout()
        tab_layout.addLayout(header_layout)

        section_label = QLabel("Game Location")
        section_label.setFont(GUIInfo().emphasis_font)
        header_layout.addWidget(section_label)

        self.game_location_choose_button = QToolButton()
        self.game_location_choose_button.setText("Choose…")
        header_layout.addWidget(self.game_location_choose_button)

        self.game_location = QLineEdit()
        self.game_location.setTextMargins(GUIInfo().text_field_margins)
        self.game_location.setFixedHeight(GUIInfo().default_font_line_height * 2)
        self.game_location.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        tab_layout.addWidget(self.game_location)

    def _do_config_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        header_layout = QHBoxLayout()
        tab_layout.addLayout(header_layout)

        section_label = QLabel("Config Folder Location")
        section_label.setFont(GUIInfo().emphasis_font)
        header_layout.addWidget(section_label)

        self.config_folder_location_choose_button = QToolButton()
        self.config_folder_location_choose_button.setText("Choose…")
        header_layout.addWidget(self.config_folder_location_choose_button)

        self.config_folder_location = QLineEdit()
        self.config_folder_location.setTextMargins(GUIInfo().text_field_margins)
        self.config_folder_location.setFixedHeight(
            GUIInfo().default_font_line_height * 2
        )
        self.config_folder_location.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        tab_layout.addWidget(self.config_folder_location)

    def _do_steam_mods_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        header_layout = QHBoxLayout()
        tab_layout.addLayout(header_layout)

        section_label = QLabel("Steam Mods Folder Location")
        section_label.setFont(GUIInfo().emphasis_font)
        header_layout.addWidget(section_label)

        self.steam_mods_folder_location_choose_button = QToolButton()
        self.steam_mods_folder_location_choose_button.setText("Choose…")
        header_layout.addWidget(self.steam_mods_folder_location_choose_button)

        self.steam_mods_folder_location = QLineEdit()
        self.steam_mods_folder_location.setTextMargins(GUIInfo().text_field_margins)
        self.steam_mods_folder_location.setFixedHeight(
            GUIInfo().default_font_line_height * 2
        )
        self.steam_mods_folder_location.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        tab_layout.addWidget(self.steam_mods_folder_location)

    def _do_local_mods_folder_location_area(self, tab_layout: QVBoxLayout) -> None:
        header_layout = QHBoxLayout()
        tab_layout.addLayout(header_layout)

        section_label = QLabel("Local Mods Folder Location")
        section_label.setFont(GUIInfo().emphasis_font)
        header_layout.addWidget(section_label)

        self.local_mods_folder_location_choose_button = QToolButton()
        self.local_mods_folder_location_choose_button.setText("Choose…")
        header_layout.addWidget(self.local_mods_folder_location_choose_button)

        self.local_mods_folder_location = QLineEdit()
        self.local_mods_folder_location.setTextMargins(GUIInfo().text_field_margins)
        self.local_mods_folder_location.setFixedHeight(
            GUIInfo().default_font_line_height * 2
        )
        self.local_mods_folder_location.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        tab_layout.addWidget(self.local_mods_folder_location)

    def _do_databases_tab(self) -> None:
        tab = QWidget()
        self._tab_widget.addTab(tab, "Databases")

        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)

        self._do_community_rules_db_group(tab_layout)
        self._do_steam_workshop_db_group(tab_layout)

    def _do_community_rules_db_group(self, tab_layout: QBoxLayout) -> None:
        group = QGroupBox()
        tab_layout.addWidget(group, stretch=1)

        group_layout = QVBoxLayout()
        group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        group.setLayout(group_layout)

        section_label = QLabel("Community Rules Database")
        section_label.setFont(GUIInfo().emphasis_font)
        section_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        group_layout.addWidget(section_label)

        section_layout = QVBoxLayout()
        section_layout.setSpacing(0)
        group_layout.addLayout(section_layout)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        self.community_rules_db_none_radio = QRadioButton("None")
        self.community_rules_db_none_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        self.community_rules_db_none_radio.setChecked(True)
        item_layout.addWidget(self.community_rules_db_none_radio, stretch=2)

        label = QLabel("No community rules database will be used.")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        label.setEnabled(False)
        item_layout.addWidget(label, stretch=8)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        self.community_rules_db_github_radio = QRadioButton("GitHub")
        self.community_rules_db_github_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        item_layout.addWidget(self.community_rules_db_github_radio, stretch=2)
        self.community_rules_db_github_url = QLineEdit()
        self.community_rules_db_github_url.setTextMargins(GUIInfo().text_field_margins)
        self.community_rules_db_github_url.setPlaceholderText(
            "https://github.com/RimSort/Community-Rules-Database or whatever"
        )
        self.community_rules_db_github_url.setClearButtonEnabled(True)
        self.community_rules_db_github_url.setEnabled(False)
        item_layout.addWidget(self.community_rules_db_github_url, stretch=8)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)
        self.community_rules_db_local_file_radio = QRadioButton("Local File")
        self.community_rules_db_local_file_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        item_layout.addWidget(self.community_rules_db_local_file_radio, stretch=2)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)
        item_layout.addLayout(row_layout, stretch=8)

        self.community_rules_db_local_file = QLineEdit()
        self.community_rules_db_local_file.setTextMargins(GUIInfo().text_field_margins)
        self.community_rules_db_local_file.setClearButtonEnabled(True)
        self.community_rules_db_local_file.setEnabled(False)
        row_layout.addWidget(self.community_rules_db_local_file)

        self.community_rules_db_local_file_choose_button = QToolButton()
        self.community_rules_db_local_file_choose_button.setText("Choose…")
        self.community_rules_db_local_file_choose_button.setEnabled(False)
        row_layout.addWidget(self.community_rules_db_local_file_choose_button)

        section_layout.addStretch(1)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        info_label = QLabel(
            "Some explanatory information should go here. For instance we could explain what a community rules "
            "database is and what it does. There's room for about two or three lines of text, so we should be concise. "
            "But I think we need to explain these options in a clear and understandable way (because I don't fully "
            "understand them myself)."
        )
        info_label.setWordWrap(True)
        item_layout.addWidget(info_label)

    def _do_steam_workshop_db_group(self, tab_layout: QBoxLayout) -> None:
        group = QGroupBox()
        tab_layout.addWidget(group, stretch=1)

        group_layout = QVBoxLayout()
        group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        group.setLayout(group_layout)

        section_label = QLabel("Steam Workshop Database")
        section_label.setFont(GUIInfo().emphasis_font)
        section_label.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        group_layout.addWidget(section_label)

        section_layout = QVBoxLayout()
        section_layout.setSpacing(0)
        group_layout.addLayout(section_layout)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        self.steam_workshop_db_none_radio = QRadioButton("None")
        self.steam_workshop_db_none_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        self.steam_workshop_db_none_radio.setChecked(True)
        item_layout.addWidget(self.steam_workshop_db_none_radio, stretch=2)

        label = QLabel("No Steam workshop database will be used.")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        label.setEnabled(False)
        item_layout.addWidget(label, stretch=8)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        self.steam_workshop_db_github_radio = QRadioButton("GitHub")
        self.steam_workshop_db_github_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        item_layout.addWidget(self.steam_workshop_db_github_radio, stretch=2)
        self.steam_workshop_db_github_url = QLineEdit()
        self.steam_workshop_db_github_url.setTextMargins(GUIInfo().text_field_margins)
        self.steam_workshop_db_github_url.setPlaceholderText(
            "https://github.com/RimSort/Steam-Workshop-Database or what have you"
        )
        self.steam_workshop_db_github_url.setClearButtonEnabled(True)
        self.steam_workshop_db_github_url.setEnabled(False)
        item_layout.addWidget(self.steam_workshop_db_github_url, stretch=8)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)
        self.steam_workshop_db_local_file_radio = QRadioButton("Local File")
        self.steam_workshop_db_local_file_radio.setMinimumSize(
            0, GUIInfo().default_font_line_height * 2
        )
        item_layout.addWidget(self.steam_workshop_db_local_file_radio, stretch=2)

        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)
        item_layout.addLayout(row_layout, stretch=8)

        self.steam_workshop_db_local_file = QLineEdit()
        self.steam_workshop_db_local_file.setTextMargins(GUIInfo().text_field_margins)
        self.steam_workshop_db_local_file.setClearButtonEnabled(True)
        self.steam_workshop_db_local_file.setEnabled(False)
        row_layout.addWidget(self.steam_workshop_db_local_file)

        self.steam_workshop_db_local_file_choose_button = QToolButton()
        self.steam_workshop_db_local_file_choose_button.setText("Choose…")
        self.steam_workshop_db_local_file_choose_button.setEnabled(False)
        row_layout.addWidget(self.steam_workshop_db_local_file_choose_button)

        section_layout.addStretch(1)

        item_layout = QHBoxLayout()
        section_layout.addLayout(item_layout, stretch=1)

        info_label = QLabel(
            "This is where we should explain what a Steam workshop database is and what it does. While we're on the "
            'topic, is there any reason why "None" should be the default instead of "GitHub"? It seems like that\'s '
            "what's intended, but I'm not sure."
        )
        info_label.setWordWrap(True)
        item_layout.addWidget(info_label)

    def _do_sorting_tab(self) -> None:
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        sorting_label = QLabel("Sort Mods")
        sorting_label.setFont(GUIInfo().emphasis_font)
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

    def _do_steamcmd_tab(self) -> None:
        tab = QWidget()
        self._tab_widget.addTab(tab, "SteamCMD")

        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)

    def _do_todds_tab(self) -> None:
        tab = QWidget()
        self._tab_widget.addTab(tab, "todds")

        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)

    def _do_advanced_tab(self) -> None:
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.debug_logging_checkbox = QCheckBox("Enable debug logging", tab)
        tab_layout.addWidget(self.debug_logging_checkbox)

        self._tab_widget.addTab(tab, "Advanced")
