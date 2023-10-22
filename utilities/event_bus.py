from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    zoom_action_triggered = Signal()

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance
