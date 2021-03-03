# from PySide2 import QtWidgets, QtCore, QtGui
import json
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import PyQt5

from PC_program_src.ui import ui_MainWindow
from PC_program_src import config
from PC_program_src.ui import material_slider
from PC_program_src import constances
from PC_program_src import comunication
from PC_program_src import summary_tools
from PC_program_src import effects

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi()

        self.attachActions()
        self.show()

        if len(self.available_usb_ports) > 0:
            self.communication_master = comunication.Serial_comunication(self.available_usb_ports[0])


    def setupUi(self):
        self.ui = ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.onOffButton = material_slider.Switch(self.ui.onoff_frame, track_radius=10, thumb_radius=14)
        self.ui.onOffButton.setObjectName(u"onOffButton")
        self.ui.onOffButton.move(10, (self.ui.onoff_frame.height() - self.ui.onOffButton._track_radius)//2)
        
        enum_pretty_print = lambda x: x.name.lower().replace("_", " ").capitalize()

        for i, effect in enumerate(constances.EffectsIDs):
            self.ui.effect1_choose_combobox.insertItem(i, enum_pretty_print(effect), effect)
            self.ui.effect2_choose_combobox.insertItem(i, enum_pretty_print(effect), effect)

        self.ui.effect1_summary.setWordWrap(True)
        self.ui.effect2_summary.setWordWrap(True)
        self.effect1_summary_model = QtGui.QStandardItemModel(self.ui.effect1_summary)
        self.effect2_summary_model = QtGui.QStandardItemModel(self.ui.effect2_summary)
        # self.effect1_summary_model.setColumnCount(2)


        self.update_available_devices()
        

    def attachActions(self):
        self.ui.left_menu_toggleButton.clicked.connect(self.toggle_left_menu)
        self.ui.effectsButton.clicked.connect(lambda: self.change_visible_site(0))
        self.ui.paintButton.clicked.connect(lambda: self.change_visible_site(1))
        self.ui.commandsButton.clicked.connect(lambda: self.change_visible_site(2))

        self.ui.refresh_usb_portsButton.clicked.connect(self.update_available_devices)
        self.ui.onOffButton.toggled.connect(lambda power: self.toggle_LEDS_power(power))

        self.ui.effect1_choose_combobox.currentIndexChanged.connect(lambda: self.show_summary(self.ui.effect1_choose_combobox.currentData()))

        self.ui.applyButton.clicked.connect(self.upload_effects)
    

    def upload_effects(self):
        if not hasattr(self, 'communication_master'):
            print("creating com master")
            port = self.ui.usb_port_list.currentText()
            self.communication_master = comunication.Serial_comunication(port)
        
        if not self.power_state:
            print("power is off")
            return

        blend_ratio = self.ui.blend_slider.value()
        self.communication_master.send_command(f"{constances.OrdersIDs.STOP}:0:0;{constances.OrdersIDs.STOP}:1:0")
        if hasattr(self, 'effect1') and self.ui.effect1_active:
            print("uploading effect1")
            self.communication_master.send_command(self.effect1.prepare_command())
        else:
            blend_ratio = 255
        if hasattr(self, 'effect2') and self.ui.effect2_active:
            print("uploading effect2")
            self.communication_master.send_command(self.effect2.prepare_command())
        else:
            blend_ratio = 0
        
        cmd = f"{int(constances.OrdersIDs.SET_BLENDING_RATIO)}:{blend_ratio}:1;"

        self.communication_master.send_command(cmd)
    

    @QtCore.pyqtSlot()
    def show_summary(self, effect):
        self.effect1_summary_model.clear()
        with open("PC_program_src/default_effects_config/linear_colors.json", "r") as default_effects_config_file:
            default_effects_config = json.load(default_effects_config_file)

        effect_config = default_effects_config[effect.name].copy()
        effect_type = self.ui.effect1_choose_combobox.currentData()

        self.effect1 = effects.create_effect[effect_type](0, self.effect1_summary_model, self.ui.effect1_summary, default_effects_config, effect_type)
        # self.effect2 = effects.create_effect[effect_type](1, self.effect2_summary_model, self.ui.effect2_summary, default_effects_config, effect_type)



        # Apply model to visible QListView
        self.ui.effect1_summary.setModel(self.effect1_summary_model)


    @QtCore.pyqtSlot()
    def toggle_LEDS_power(self, power: bool):
        self.power_state = power

        if power:
            self.upload_effects()
        else:
            self.communication_master.send_command(f"{constances.OrdersIDs.STOP}:0:0;{constances.OrdersIDs.STOP}:1:0")


    @QtCore.pyqtSlot()
    def update_available_devices(self):
        self.available_usb_ports = comunication.list_serial_ports()
        self.ui.usb_port_list.addItems(self.available_usb_ports)


    @QtCore.pyqtSlot()
    def change_visible_site(self, index):
        self.ui.content.setCurrentIndex(index)
        
        # Go through evry button in the menu bar
        for site_button in self.ui.menu_bar_frame.findChildren(QtWidgets.QPushButton):
            # and reset its style sheet
            default_qss = site_button.styleSheet().replace("border-bottom: 2px solid red;", "").replace("border-left: 2px solid red;", "")
            site_button.setStyleSheet(default_qss)
        # Add active site indicator to the clicked button
        self.sender().setStyleSheet(self.sender().styleSheet()+"\nborder-bottom: 2px solid red;\nborder-left: 2px solid red;")


    # expand or contract left menu
    @QtCore.pyqtSlot()
    def toggle_left_menu(self):
        menu = self.ui.menu_bar_frame

        if menu.width() == config.LEFT_MENU_BAR_CONTRACTED_WIDTH:
            # print("jest wsunięte")
            new_width = config.LEFT_MENU_BAR_EXPANDED_WIDH
        else:
            # print("jest wysunięte")
            new_width = config.LEFT_MENU_BAR_CONTRACTED_WIDTH

        # menu.setMaximumWidth(new_width)

        # self.animation1 = QtCore.QPropertyAnimation(menu, b"minimumWidth")
        # self.animation1.setDuration(config.LEFT_MENU_BAR_TRANSITION_TIME)
        # self.animation1.setStartValue(menu.width())
        # self.animation1.setEndValue(new_width)
        # self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        # self.animation1.start()

        self.animation2 = QtCore.QPropertyAnimation(menu, b"maximumWidth")
        self.animation2.setDuration(config.LEFT_MENU_BAR_TRANSITION_TIME)
        self.animation2.setStartValue(menu.width())
        self.animation2.setEndValue(new_width)
        self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation2.start()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # mw = QtWidgets.QMainWindow()
    # ui = MainWindow()
    # ui.setupUi(mw)
    # mw.show()

    mw = MainWindow()
    sys.exit(app.exec_())
