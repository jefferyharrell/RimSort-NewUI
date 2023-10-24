from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    database_ready = Signal()

    menu_bar_about_action_triggered = Signal()
    menu_bar_settings_action_triggered = Signal()
    menu_bar_zoom_action_triggered = Signal()
    menu_bar_quit_action_triggered = Signal()

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
