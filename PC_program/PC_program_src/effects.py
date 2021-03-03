from typing import Any
from PC_program_src import summary_tools
from PC_program_src.constances import EffectsIDs
from PC_program_src import config

from abc import ABC
from PyQt5 import QtCore, QtGui, QtWidgets

def set_last_led(effect_config, value):
    effect_config['last_led'] = value

def set_property(efffect_property: str, value: Any, effect_config: dict):
    effect_config[efffect_property] = value

def load_default_color(hue: QtWidgets.QDoubleSpinBox, sat: QtWidgets.QDoubleSpinBox, val: QtWidgets.QDoubleSpinBox, color: dict):
    hue.setValue(color['hue'])
    sat.setValue(color['saturation'])
    val.setValue(color['value'])

def append_color_to_command_args(args: list, color: dict):
    args.append(color['hue'])
    args.append(color['saturation'])
    args.append(color['value'])


class Effect(ABC):
    def __init__(self, place: int, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView, effect_config: dict, effect_type: EffectsIDs) -> None:
        super().__init__()

        self.effect_type = effect_type
        self.place = place
        # self.effect_config = effects_config[effect_type.name]
        self.effect_config = effect_config
        self.summary_model = summary_model
        self.summary_widget = summary_widget


        self.make_summary()

    def prepare_command(self): # Return the command (here with empty args)
        return f"{self.effect_type}:{self.place}:"

    def make_summary(self): 
        pass



class Fill_solid(Effect):
    def __init__(self, place: int, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView, effect_config: dict, effect_type: EffectsIDs) -> None:
        super().__init__(place, summary_model, summary_widget, effect_config, effect_type)

    def make_summary(self):
        # Create summary items and configuration widgets
        # last_led_widget = summary_tools._CREATE_ITEM_WITH_NUMBER("Last led:", config.NUM_OF_LEDS, self.summary_model.invisibleRootItem(), self.summary_model, self.summary_widget)
        last_led_widget = summary_tools.CREATE_LAST_LED_ITEM(self.summary_model, self.summary_widget)
        hue, sat, val = summary_tools.CREATE_ITEM_WITH_COLOR("Color:", self.summary_model.invisibleRootItem(), self.summary_model, self.summary_widget)

        # Visualize default effect configuration
        last_led_widget.setValue(self.effect_config.get('last_led'))
        load_default_color(hue, sat, val, self.effect_config['color'])

        # Update logical configuration (self.effect_config) on visible ones change
        last_led_widget.valueChanged.connect(lambda: set_last_led(self.effect_config, int(last_led_widget.value())))

        hue.valueChanged.connect(lambda: set_property('hue', int(hue.value()), self.effect_config['color']))
        sat.valueChanged.connect(lambda: set_property('saturation', int(sat.value()), self.effect_config['color']))
        val.valueChanged.connect(lambda: set_property('value', int(val.value()), self.effect_config['color']))


    def prepare_command(self):
        prefix = super().prepare_command()

        args = []

        args.append(self.effect_config['last_led'])
        append_color_to_command_args(args, self.effect_config['color'])

        return prefix + ",".join(map(str, args))


class Linear_colors(Effect):
    def __init__(self, place: int, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView, effects_config: dict, effect_type: EffectsIDs) -> None:
        super().__init__(place, summary_model, summary_widget, effects_config, effect_type)
    

    def make_summary(self):
        # Create summary items and configuration widgets
        last_led_widget = summary_tools.CREATE_LAST_LED_ITEM(self.summary_model, self.summary_widget)
        transition_time_widget = summary_tools.CREATE_TRANSITION_TIME_ITEM(self.summary_model, self.summary_widget)

        root = self.summary_model.invisibleRootItem()
        change_colors_each_cycle_widget = summary_tools.CREATE_ITEM_WITH_CHECKBOX("Sliightly change colors each cycle:", root, self.summary_model, self.summary_widget)
        
        # Visualize default effect configuration
        last_led_widget.setValue(self.effect_config['last_led'])
        transition_time_widget.setValue(self.effect_config['transition_time'])
        change_colors_each_cycle_widget.setChecked(not self.effect_config['fix_colors'])


        # Update logical configuration (self.effect_config) on visible ones change
        last_led_widget.valueChanged.connect(lambda: set_last_led(self.effect_config, int(last_led_widget.value())))
        transition_time_widget.valueChanged.connect(lambda: set_property('transition_time', int(transition_time_widget.value()), self.effect_config))
        change_colors_each_cycle_widget.stateChanged.connect(lambda: set_property('fix_colors', not change_colors_each_cycle_widget.isChecked(), self.effect_config))


    def prepare_command(self):
        prefix = super().prepare_command()

        args = []

        args.append(self.effect_config['last_led'])
        args.append(self.effect_config['transition_time'])
        args.append(int(self.effect_config['fix_colors']))

        return prefix + ",".join(map(str, args))

class Traveling_pixels(Effect):
    def __init__(self, place: int, summary_model: QtGui.QStandardItemModel, summary_widget: QtWidgets.QTreeView, effects_config: dict, effect_type: EffectsIDs) -> None:
        super().__init__(place, summary_model, summary_widget, effects_config, effect_type)

    
    def make_summary(self):
        # Create summary items and configuration widgets
        root = self.summary_model.invisibleRootItem()
        last_led_widget = summary_tools.CREATE_LAST_LED_ITEM(self.summary_model, self.summary_widget)
        transition_time_widget = summary_tools.CREATE_TRANSITION_TIME_ITEM(self.summary_model, self.summary_widget)
        pixel_spacing_widget = summary_tools.CREATE_ITEM_WITH_NUMBER("Pixel spacing", config.NUM_OF_LEDS, root, self.summary_model, self.summary_widget)
        pixel_spacing_widget.setDecimals(0)
        blur_radius_widget = summary_tools.CREATE_ITEM_WITH_NUMBER("Blur radius", config.NUM_OF_LEDS, root, self.summary_model, self.summary_widget)
        blur_radius_widget.setDecimals(0)
        
        color1_hue, color1_sat, color1_val = summary_tools.CREATE_ITEM_WITH_COLOR("Traveling pixel color:", self.summary_model.invisibleRootItem(), self.summary_model, self.summary_widget)
        color2_hue, color2_sat, color2_val = summary_tools.CREATE_ITEM_WITH_COLOR("Background color", self.summary_model.invisibleRootItem(), self.summary_model, self.summary_widget)
        
        # Visualize default effect configuration
        last_led_widget.setValue(self.effect_config['last_led'])
        transition_time_widget.setValue(self.effect_config['transition_time'])
        pixel_spacing_widget.setValue(self.effect_config['pixel_spacing'])
        blur_radius_widget.setValue(self.effect_config['blur_radius'])

        load_default_color(color1_hue, color1_sat, color1_val, self.effect_config['color'])
        load_default_color(color2_hue, color2_sat, color2_val, self.effect_config['background_color'])
        
        # Update logical configuration (self.effect_config) on visible ones change
        last_led_widget.valueChanged.connect(lambda: set_last_led(self.effect_config, int(last_led_widget.value())))
        transition_time_widget.valueChanged.connect(lambda: set_property('transition_time', int(transition_time_widget.value()), self.effect_config))
        pixel_spacing_widget.valueChanged.connect(lambda: set_property('pixel_spacing', int(pixel_spacing_widget.value()), self.effect_config))
        blur_radius_widget.valueChanged.connect(lambda: set_property('blur_radius', int(blur_radius_widget.value()), self.effect_config))

        color1_hue.valueChanged.connect(lambda: set_property('hue', int(color1_hue.value()), self.effect_config['color']))
        color1_sat.valueChanged.connect(lambda: set_property('saturation', int(color1_sat.value()), self.effect_config['color']))
        color1_val.valueChanged.connect(lambda: set_property('value', int(color1_val.value()), self.effect_config['color']))

        color2_hue.valueChanged.connect(lambda: set_property('hue', int(color2_hue.value()), self.effect_config['background_color']))
        color2_sat.valueChanged.connect(lambda: set_property('saturation', int(color2_sat.value()), self.effect_config['background_color']))
        color2_val.valueChanged.connect(lambda: set_property('value', int(color2_val.value()), self.effect_config['background_color']))

    
    def prepare_command(self):
        prefix = super().prepare_command()

        args = []

        args.append(self.effect_config['last_led'])
        args.append(self.effect_config['transition_time'])
        args.append(self.effect_config['pixel_spacing'])
        args.append(self.effect_config['blur_radius'])
        append_color_to_command_args(args, self.effect_config['color'])
        append_color_to_command_args(args, self.effect_config['background_color'])

        return prefix + ",".join(map(str, args))

create_effect = {
    EffectsIDs.FILL_SOLID: Fill_solid,
    EffectsIDs.LINEAR_COLORS: Linear_colors,
    EffectsIDs.TRAVELING_PIXELS: Traveling_pixels
}
