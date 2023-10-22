from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    menu_bar_about_action_triggered = Signal()
    menu_bar_settings_action_triggered = Signal()
    menu_bar_zoom_action_triggered = Signal()
    menu_bar_quit_action_triggered = Signal()

    _instance = None

    @classmethod
    def instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance
