import dbus
import dbus.mainloop.glib
import dbus.service

BUS_NAME = 'jp.kimura.SWITCHService'
OBJECT_PATH = '/jp/kimura/SWITCHServer'
INTERFACE = 'jp.kimura.SWITCH'

class SWITCHClient(dbus.service.Object):
    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(SWITCHClient, self).__init__(bus_name, OBJECT_PATH)
        self._proxy = bus.get_object(BUS_NAME, OBJECT_PATH)
    def is_closed(self, pin):
        closed = int(self._proxy.is_closed(pin))
        if closed == 0:
            return False
        elif closed ==1:
            return True
        else:
            return None
    def is_opened(self, pin):
        closed = int(self._proxy.is_closed(pin))
        if closed == 1:
            return False
        elif closed ==0:
            return True
        else:
            return None

if __name__ == '__main__':
    import time
    switch_client = SWITCHClient()
    while True:
        print(switch_client.is_closed(2))
        time.sleep(2)
        print(switch_client.is_closed(26))
        time.sleep(2)
