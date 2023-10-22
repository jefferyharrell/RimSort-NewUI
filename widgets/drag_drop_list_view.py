from typing import Optional

from PySide6.QtGui import QDragMoveEvent, QDropEvent, QKeyEvent
from PySide6.QtWidgets import QListView, QAbstractItemView, QWidget
from PySide6.QtCore import Qt


class DragDropListView(QListView):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super(DragDropListView, self).__init__(parent)

        # Enable drag and drop
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)

        # Disable editing
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Look and feel
        self.setAlternatingRowColors(True)

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        super().dragMoveEvent(event)

        # If the drop indicator is "OnItem", ignore the drop action
        if (
            self.dropIndicatorPosition()
            == QAbstractItemView.DropIndicatorPosition.OnItem
        ):
            event.setDropAction(Qt.DropAction.IgnoreAction)

    def dropEvent(self, event: QDropEvent) -> None:
        # Call the base class's dropEvent method to ensure default behavior is executed
        super().dropEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # Get the current selection
        current_index = self.currentIndex()

        # Check for the down arrow key
        if event.key() == Qt.Key.Key_Down:
            # Get the next index
            next_index = self.model().index(
                current_index.row() + 1, current_index.column()
            )
            if next_index.isValid():
                self.setCurrentIndex(next_index)
                return

        # Check for the up arrow key
        elif event.key() == Qt.Key.Key_Up:
            # Get the previous index
            previous_index = self.model().index(
                current_index.row() - 1, current_index.column()
            )
            if previous_index.isValid():
                self.setCurrentIndex(previous_index)
                return

        # Call the base class's keyPressEvent for other keys
        super().keyPressEvent(event)
