from typing import Any, Iterable
import colorsys
from PyQt5 import QtCore, QtWidgets, QtGui
import math


import PC_program_src.config as config
from PC_program_src.constances import EffectsIDs


def summarize(effect: EffectsIDs, config: dict, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView):
    pass


def _ALIGN_WIDGET_RIGHT(widget: QtWidgets.QWidget, right_margin: int = 5) -> QtWidgets.QWidget:
    """
    Takes widget that should be aligned to right. Return QWidget that have to be put in place of taken widget
    """
    outer_widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(outer_widget)
    layout.setContentsMargins(0, 0, right_margin, 0)
    layout.addStretch()
    layout.addWidget(widget)

    return outer_widget


def CREATE_ITEM_WITH_COMBOBOX(name: str, combobox_options: Iterable, combobox_data: Iterable, parent_item: QtGui.QStandardItem, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView): 
    left_column = QtGui.QStandardItem(name)
    right_column = QtGui.QStandardItem()
    parent_item.appendRow([left_column, right_column])
    summary_widget.setModel(summary_model)
    
    combobox = QtWidgets.QComboBox(summary_widget)
    aligned_combobox = _ALIGN_WIDGET_RIGHT(combobox)

    for text, data in zip(combobox_options, combobox_data):
        combobox.addItem(text, data)
    
    summary_widget.setIndexWidget(summary_model.indexFromItem(right_column), aligned_combobox)    

    return combobox


def CREATE_ITEM_WITH_CHECKBOX(name: str, parent_item: QtGui.QStandardItem, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView):
    left_column = QtGui.QStandardItem(name)
    right_column = QtGui.QStandardItem()
    # right_column.setData(QtCore.Qt.AlignRight, QtCore.Qt.TextAlignmentRole)
    parent_item.appendRow([left_column, right_column])
    summary_widget.setModel(summary_model)

    checkbox = QtWidgets.QCheckBox(summary_widget)
    aligned_checkbox = _ALIGN_WIDGET_RIGHT(checkbox, 10)

    summary_widget.setIndexWidget(summary_model.indexFromItem(right_column), aligned_checkbox)



    return checkbox


def CREATE_ITEM_WITH_NUMBER(name: str, max_value: int, parent_item: QtGui.QStandardItem, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView):
    left_column = QtGui.QStandardItem(name)
    right_column = QtGui.QStandardItem()
    parent_item.appendRow([left_column, right_column])
    summary_widget.setModel(summary_model)

    number_edit = QtWidgets.QDoubleSpinBox(summary_widget)
    number_edit.setDecimals(0)
    number_edit.setMinimum(0)
    number_edit.setMaximum(max_value)
    aligned_number_edit = _ALIGN_WIDGET_RIGHT(number_edit, 10)

    summary_widget.setIndexWidget(summary_model.indexFromItem(right_column), aligned_number_edit)

    return number_edit


def CREATE_ITEM_WITH_COLOR(name: str, parent_item: QtGui.QStandardItem, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView):
    left_column = QtGui.QStandardItem(name)
    right_column = QtGui.QStandardItem()
    right_column.setTextAlignment(QtCore.Qt.AlignRight)
    parent_item.appendRow([left_column, right_column])

    summary_widget.setModel(summary_model)


    hue_input = CREATE_ITEM_WITH_NUMBER("Hue:", 255, left_column, summary_model, summary_widget)
    saturation_input = CREATE_ITEM_WITH_NUMBER("Sauration:", 255, left_column, summary_model, summary_widget)
    value_input = CREATE_ITEM_WITH_NUMBER("Value:", 255, left_column, summary_model, summary_widget)

    pass_update_color = lambda: update_color(hue_input.text(), saturation_input.text(), value_input.text(), right_column)
    hue_input.valueChanged.connect(pass_update_color)
    saturation_input.valueChanged.connect(pass_update_color)
    value_input.valueChanged.connect(pass_update_color)

    return hue_input, saturation_input, value_input
    # return right_column


def update_color(hue: str, sat: str, val: str, item: QtGui.QStandardItem) -> None:
    inner = ", ".join([hue, sat, val])
    item.setText("HSV(" + inner + ")")

    r, g, b = map(lambda x: x*255, colorsys.hsv_to_rgb(int(hue)/255, int(sat)/255, int(val)/255))
    pixmap = QtGui.QPixmap(20, 20)
    pixmap.fill(QtGui.QColor(r, g, b))

    item.setIcon(QtGui.QIcon(pixmap))
    

def CREATE_LAST_LED_ITEM(summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView) -> QtWidgets.QDoubleSpinBox:
    return CREATE_ITEM_WITH_NUMBER("Last led:", config.NUM_OF_LEDS, summary_model.invisibleRootItem(), summary_model, summary_widget)


def CREATE_TRANSITION_TIME_ITEM(summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView) -> QtWidgets.QDoubleSpinBox:
    return CREATE_ITEM_WITH_NUMBER("Transition time", math.inf, summary_model.invisibleRootItem(), summary_model, summary_widget)


