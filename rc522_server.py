from rc522 import RC522
import dbus
import dbus.mainloop.glib
import dbus.service

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
BUS_NAME = 'jp.kimura.RC522Service'
OBJECT_PATH = '/jp/kimura/RC522Server'
INTERFACE = 'jp.kimura.RC522'

class RC522Server(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(RC522Server, self).__init__(bus_name, OBJECT_PATH)
        self.rc522 = RC522()
    def wait_for_tag(self):
        result = str(self.rc522.get_RFID(0)).strip("[]")
        self.get_RFID(result)
    @dbus.service.signal(INTERFACE, signature='s')
    def get_RFID(self, result):
        print(result)

if __name__ == '__main__':
    import time
    rc522_server = RC522Server()
    while True:
        rc522_server.wait_for_tag()
        time.sleep(0.1)
