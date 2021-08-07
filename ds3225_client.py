from ds3225 import DS3225
import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GObject, GLib

UNLOCKED_DEG = 175

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
BUS_NAME = 'jp.kimura.DS3225Service'
OBJECT_PATH = '/jp/kimura/DS3225Server'
INTERFACE = 'jp.kimura.DS3225'

class DS3225Client(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(DS3225Client, self).__init__(bus_name, OBJECT_PATH)
        self._proxy = bus.get_object(BUS_NAME, OBJECT_PATH)
        
    def get_pos(self):
        return self._proxy.get_pos()
    def set_pos(self, pos):
        self._proxy.set_pos(pos)

if __name__ == '__main__':
    import time
    ds3225_client = DS3225Client()
    while True:
        ds3225_client.set_pos(UNLOCKED_DEG)
        time.sleep(2)
        ds3225_client.set_pos(UNLOCKED_DEG-90)
        time.sleep(2)
