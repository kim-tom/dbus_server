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

class DS3225Server(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(DS3225Server, self).__init__(bus_name, OBJECT_PATH)
        self.ds3225 = DS3225(18, ZeroOffsetDuty=0, Angle=UNLOCKED_DEG)
    @dbus.service.method(INTERFACE, out_signature='q') # uint16
    def get_pos(self):
        return self.ds3225.pos
    @dbus.service.method(INTERFACE, in_signature='q') #uint16
    def set_pos(self, pos):
        print("set_pos:{:3}".format(pos))
        self.ds3225.SetPos(pos)

if __name__ == '__main__':
    loop = GObject.MainLoop()
    ds3225_server = DS3225Server()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
