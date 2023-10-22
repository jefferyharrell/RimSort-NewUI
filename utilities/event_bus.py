from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    main_menu_zoom_action_triggered = Signal()
    main_menu_quit_action_triggered = Signal()

    _instance = None

    @classmethod
    def instance(cls) -> "EventBus":
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance
