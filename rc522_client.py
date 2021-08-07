import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GObject, GLib

BUS_NAME = 'jp.kimura.RC522Service'
OBJECT_PATH = '/jp/kimura/RC522Server'
INTERFACE = 'jp.kimura.RC522'

class RC522Client(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(RC522Client, self).__init__(bus_name, OBJECT_PATH)
        bus.add_signal_receiver(
            self.get_RFID, dbus_interface=INTERFACE, bus_name=BUS_NAME, path=OBJECT_PATH)
        self.loop = GObject.MainLoop()
        self.id_ = None
    def wait_for_tag(self, timeout = 0):
        if not self.loop.get_context().acquire():
            raise "Cannot acquire."
        while self.loop.get_context().pending():
            self.loop.get_context().dispatch()
        self.id_ = None
        if timeout != 0:
            GLib.timeout_add(timeout, self.loop.quit)
        self.loop.run()
    def get_RFID(self, result):
        self.id_ = result
        self.loop.quit()
if __name__ == '__main__':
    import time
    rc522_client = RC522Client()
    while True:
        rc522_client.wait_for_tag()
        print(rc522_client.id_)
        time.sleep(0.1)
