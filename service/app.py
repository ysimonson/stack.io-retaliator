#!/usr/bin/python
from stackio import StackIO
import platform
import time
import usb.core
import usb.util

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

class Retaliator(object):
    def __init__(self, id_vendor=0x2123, id_product=0x1010):
        # Tested only with the Cheeky Dream Thunder
        self.device = usb.core.find(idVendor=id_vendor, idProduct=id_product)

        if self.device is None:
            raise ValueError('Missile device not found')

        # On Linux we need to detach usb HID first
        if "Linux" == platform.system():
            try:
                self.device.detach_kernel_driver(0)
            except Exception, e:
                pass # already unregistered    

        self.device.set_configuration()

    def _send_cmd(self, cmd):
        self.device.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])


    def _send_move(self, cmd, duration_ms):
        self._send_cmd(cmd)
        time.sleep(duration_ms / 1000.0)
        self._send_cmd(STOP)

    def right(self, value):
        self._send_move(RIGHT, value)

    def left(self, value):
        self._send_move(LEFT, value)

    def up(self, value):
        self._send_move(UP, value)

    def down(self, value):
        self._send_move(DOWN, value)

    def park(self):
        self._send_move(DOWN, 2000)
        self._send_move(LEFT, 8000)

    def fire(self, amount=1):
        for i in xrange(min(4, max(1, amount))):
            self._send_cmd(FIRE)
            time.sleep(4.5)

def main():
    client = StackIO()
    client.expose("retaliator", Retaliator())

if __name__ == '__main__':
    main()