from PySide6.QtCore import QObject, Signal, Qt


class EventBus(QObject):
    database_ready = Signal()

    menu_bar_about_triggered = Signal()
    menu_bar_check_for_update_triggered = Signal()
    menu_bar_settings_triggered = Signal()
    menu_bar_quit_action_triggered = Signal()

    menu_bar_cut_triggered = Signal()
    menu_bar_copy_triggered = Signal()
    menu_bar_paste_triggered = Signal()

    menu_bar_minimize_triggered = Signal()
    menu_bar_zoom_triggered = Signal()

    main_window_state_changed = Signal(Qt.WindowState)

    _instance = None

    def __new__(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_is_initialized") and self._is_initialized:
            return
        super().__init__()
        self._is_initialized: bool = True
