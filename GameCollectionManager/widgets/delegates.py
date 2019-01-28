#!/usr/bin/env python

from PySide2.QtCore import QEvent, QRect, QSize, Qt
from PySide2.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionViewItem


class CheckboxDelegate(QStyledItemDelegate):
    """
    Item delegate to center checkboxes in the cells
    https://wiki.qt.io/Technical_FAQ#How_can_I_align_the_checkboxes_in_a_view.3F
    """

    def __init__(self, header, parent=None):
        """
        :param header: Column header
        :param parent: Parent widget
        """

        super(CheckboxDelegate, self).__init__(parent=parent)
        self.header = header

    def paint(self, painter, option, index):
        viewItemOption = QStyleOptionViewItem(option)

        if self.header in ("Game", "Console", "Accessory", "Box", "Manual"):
            textMargin = QApplication.style().pixelMetric(QStyle.PM_FocusFrameHMargin) + 1
            newRect = QRect(QStyle.alignedRect(option.direction, Qt.AlignCenter,
                                               QSize(option.decorationSize.width() + 5,
                                                     option.decorationSize.height()),
                                               QRect(option.rect.x() + textMargin, option.rect.y(),
                                                     option.rect.width() - (2 * textMargin),
                                                     option.rect.height())))
            viewItemOption.rect = newRect
        super().paint(painter, viewItemOption, index)

    def editorEvent(self, event, model, option, index):
        """
        Currently only checked items has CheckStateRole for some reason
        """
        flags = Qt.ItemFlags(model.flags(index))
        # Make sure the item is checkable
        if not (flags & Qt.ItemIsUserCheckable) or not (flags & Qt.ItemIsEnabled):
            return False
        # Make sure we have a check state
        value = index.data(Qt.CheckStateRole)
        if not value:
            return False
        # Make sure we have the right event type
        if event.type() == QEvent.MouseButtonRelease:
            textMargin = QApplication.style().pixelMetric(QStyle.PM_FocusFrameHMargin) + 1
            checkRect = QStyle.alignedRect(option.direction, Qt.AlignCenter,
                                           option.decorationSize,
                                           QRect(option.rect.x() + (2 * textMargin), option.rect.y(),
                                                 option.rect.width() - (2 * textMargin),
                                                 option.rect.height()))
            # Handle mouse event
            if not checkRect.contains(event.pos()):
                return False
        # And key press event
        elif event.type() == QEvent.KeyPress:
            if event.key() is not Qt.Key_Space and event.key() is not Qt.Key_Select:
                return False
        else:
            return False
        state = Qt.Unchecked if Qt.CheckState(value) == Qt.Checked else Qt.Checked
        return model.setData(index, state, Qt.CheckStateRole)
