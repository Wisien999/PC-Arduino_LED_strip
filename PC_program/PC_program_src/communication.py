import serial
import re
import sys
import glob
import serial
import time

from PC_program_src import constances
from PC_program_src import config

class Serial_comunication():
    def __init__(self, port: str) -> None:
        self.serialcom = serial.Serial(port, 9600)
        self.history = []

        self.send_command("PING")
        time.sleep(0.1)

    def send_command(self, command: str) -> None:
        if not command.endswith(";"): command += ";"
        print("command", command)
        print("encoded:", command.encode())
        self.serialcom.write(command.encode())
        self.history.append(command)


def parse_input_command(input_command: str):
    parsed_commands = []

    for command in filter(len, map(lambda x: x.strip(), input_command.split(";"))): # ignore empty commands
        parsed_command = []
        command = command.upper().replace(" ", "_").strip("_")
        command = command+";"
        # command = command if command.endswith(";") else command+";"

        command = re.sub(f'{config.COMMAND_PART_SEPARATOR}_*', config.COMMAND_PART_SEPARATOR, command)
        command = re.sub(r'_*,_*', ',', command)


        try:
            i = command.index(config.COMMAND_PART_SEPARATOR) # Get index of the order name end + separator 
            order = command[:i]
            if not order.isnumeric():
                order = (constances.OrdersIDs[order].value)
            parsed_command.append(order)
            parsed_command.append(config.COMMAND_PART_SEPARATOR)
            command = command[i+1:]
        except ValueError:
            raise SyntaxError("Invalid command syntax")


        sign_expected_after_place = config.COMMAND_PART_SEPARATOR
        if parsed_command[0] == constances.OrdersIDs.STOP.value: # STOP order is a little specific
            sign_expected_after_place = ";"
        

        i = command.index(sign_expected_after_place)
        place_num = command[:i]
        if not place_num.isnumeric():
            raise SyntaxError("Invalid command syntax") 
        if int(place_num) in range(0, 2):
            parsed_command.append(place_num)
            parsed_command.append(":")
        else: raise KeyError("You have to choose place 0 or 1")
        parsed_command.append("0")
        parsed_command.append("0")
    
        command = command[i+1:] # Go to the arguments


        arguments = filter(lambda arg: len(arg) > 0, command.split(","))
        for argument in arguments:
            argument = argument.rstrip(";")
            if not argument.isnumeric():
                argument = int(constances.Transition_function[argument])
            parsed_command.append(argument)
            parsed_command.append(",")

        parsed_command[-1] = ";"

        parsed_commands.append("".join(map(str, parsed_command)))            

    return parsed_commands 


def list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """

    if sys.platform.startswith('win'):
        ports = [f'COM{i+1}' for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


            
if __name__ == "__main__":
    print(parse_input_command("stop:1;TRAVELING_PIXELS:0:54,TRIWAVE"))
    print(list_serial_ports())