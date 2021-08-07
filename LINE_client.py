import dbus
import dbus.mainloop.glib
import dbus.service

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
BUS_NAME = 'jp.kimura.LINEService'
OBJECT_PATH = '/jp/kimura/LINEServer'
INTERFACE = 'jp.kimura.LINE'

url = 'https://api.line.me/v2/bot/message/broadcast'
with open("access_token.txt") as f:
    access_token = f.read().strip()
header = {'Content-Type': 'application/json',
          'Authorization': access_token}

class LINEClient(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(LINEClient, self).__init__(bus_name, OBJECT_PATH)
        self._proxy = bus.get_object(BUS_NAME, OBJECT_PATH)
    def broadcast(self, message):
       self._proxy.broadcast(message)

if __name__ == '__main__':
    line_client = LINEClient()
    line_client.broadcast("てすとてすと〜")
