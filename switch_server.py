import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GObject, GLib
import RPi.GPIO as GPIO

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
BUS_NAME = 'jp.kimura.SWITCHService'
OBJECT_PATH = '/jp/kimura/SWITCHServer'
INTERFACE = 'jp.kimura.SWITCH'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#  2: Lead Switch
# 26: Key Switch
PINS = {26, 2}
for pin in PINS:
   GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class SWITCHServer(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(SWITCHServer, self).__init__(bus_name, OBJECT_PATH)
    
    @dbus.service.method(INTERFACE, in_signature='y', out_signature='y') #byte
    def is_closed(self, pin):
        print("is_closed(pin={:})".format(pin))
        print(int(GPIO.input(pin) == GPIO.LOW))
        if pin in PINS:
            return int(GPIO.input(pin) == GPIO.LOW)
        else:
            return 0xFF

if __name__ == '__main__':
    loop = GObject.MainLoop()
    switch_server = SWITCHServer()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
