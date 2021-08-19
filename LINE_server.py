import dbus
import dbus.mainloop.glib
import dbus.service
from gi.repository import GObject, GLib
import requests
import json

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
BUS_NAME = 'jp.kimura.LINEService'
OBJECT_PATH = '/jp/kimura/LINEServer'
INTERFACE = 'jp.kimura.LINE'

url = 'https://api.line.me/v2/bot/message/broadcast'
with open("access_token.txt") as f:
    access_token = f.read().strip()
header = {'Content-Type': 'application/json',
          'Authorization': access_token}

class LINEServer(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super(LINEServer, self).__init__(bus_name, OBJECT_PATH)
    @dbus.service.method(INTERFACE, in_signature='s', out_signature='s')
    def broadcast(self, message):
       payload = {
          "messages": [
             {
                "type" : "text",
                "text" : message
             }
          ]
       }
       res = requests.post(url, headers = header, data = json.dumps(payload))
       print(res.text)
       return res.text

if __name__ == '__main__':
    loop = GObject.MainLoop()
    line_server = LINEServer()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
