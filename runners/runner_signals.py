from PySide6.QtCore import QObject, Signal


class RunnerSignals(QObject):
    data_ready = Signal(object)
    finished = Signal()
