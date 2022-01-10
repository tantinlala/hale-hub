import serial
import serial.tools.list_ports
from hale_hub.constants import STARTING_OUTLET_COMMAND, SERIAL_BAUD_RATE, SERIAL_TIMEOUT
from hale_hub.ifttt_logger import send_ifttt_log


class _Outlet:
    def __init__(self, name):
        self.state = 0
        self.name = name


class _OutletInterface:
    def __init__(self):
        self.outlets = [_Outlet('Outlet 0'), _Outlet('Outlet 1'), _Outlet('Outlet 2')]
        self.serial_interface = None
        self.serial_interface_string = None

    def set_outlet_name(self, name, outlet_id):
        if outlet_id < len(self.outlets):
            self.outlets[outlet_id].name = name

    def set_serial_interface(self, serial_interface_string):
        try:
            print('Setting serial interface with description: {}'.format(serial_interface_string))
            self.serial_interface_string = serial_interface_string
            ports = [p.device for p in serial.tools.list_ports.comports() if self.serial_interface_string in p.description]
            self.serial_interface = serial.Serial(ports[0], SERIAL_BAUD_RATE, timeout=SERIAL_TIMEOUT)
        except IndexError:
            send_ifttt_log(__name__, 'No serial ports could be upon!')

    def _send_outlet_command(self, outlet_id, outlet_state):
        try:
            print('Changing outlet {0} to {1} state'.format(outlet_id, outlet_state))
            command = bytearray([STARTING_OUTLET_COMMAND + (outlet_id << 1) + outlet_state])
            print('Writing {0} to serial'.format(command))
            self.serial_interface.write(command)
        except (serial.SerialException, AttributeError):
            send_ifttt_log(__name__, 'No serial bytes could be written')
            if self.serial_interface.is_open():
                self.serial_interface.close()
            self.set_serial_interface(self.serial_interface_string)

    def toggle_outlet(self, outlet_id):
        if outlet_id < len(self.outlets):
            self.outlets[outlet_id].state ^= 1
            self._send_outlet_command(outlet_id, self.outlets[outlet_id].state)

    def turn_on_outlet(self, outlet_id):
        if outlet_id < len(self.outlets):
            self.outlets[outlet_id].state = 1
            self._send_outlet_command(outlet_id, self.outlets[outlet_id].state)

    def turn_off_outlet(self, outlet_id):
        if outlet_id < len(self.outlets):
            self.outlets[outlet_id].state = 0
            self._send_outlet_command(outlet_id, self.outlets[outlet_id].state)

    def get_outlets(self):
        return self.outlets


_outlet_interface = _OutletInterface()
set_outlet_serial_interface = _outlet_interface.set_serial_interface
toggle_outlet = _outlet_interface.toggle_outlet
turn_on_outlet = _outlet_interface.turn_on_outlet
turn_off_outlet = _outlet_interface.turn_off_outlet
get_outlets = _outlet_interface.get_outlets
set_outlet_name = _outlet_interface.set_outlet_name
