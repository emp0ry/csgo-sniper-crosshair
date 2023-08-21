from http.server import BaseHTTPRequestHandler, HTTPServer
import pygetwindow as gw
from time import sleep
import ctypes
import json

user32 = ctypes.windll.user32

class Point(ctypes.Structure):
    _fields_ = [('x',ctypes.c_long), ('y', ctypes.c_long)]

class CursorInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_uint),
        ('flags', ctypes.c_uint),
        ('hCursor', ctypes.c_void_p),
        ('ptScreenPos', Point)
    ]

def cursor_state():
    cinfo = CursorInfo(ctypes.sizeof(CursorInfo))
    ctypes.windll.user32.GetCursorInfo(ctypes.byref(cinfo))
    return not bool(cinfo.flags)

def get_screen_size():
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height

def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data)
            self.process_payload(payload)
        except json.JSONDecodeError:
            width, height = get_screen_size()
            crosshair_window.moveTo(width, height)
            print('Error decoding JSON data')

    def process_payload(self, payload):
        data = None
        width, height = get_screen_size()

        try:
            data = payload['player']['weapons']
        except:
            crosshair_window.moveTo(width, height)

        if data:
            found_keys = []
            for key, item in data.items():
                if 'type' in item and item['type'] == 'SniperRifle' and 'state' in item and item['state'] == 'active':
                    found_keys.append(key)
            if found_keys:
                if cursor_state():
                    x, y = int(width / 2 - 12), int(height / 2 - 12)
                    crosshair_window.moveTo(x, y)
                else:
                    crosshair_window.moveTo(width, height)
            else:
                crosshair_window.moveTo(width, height)
        else:
            crosshair_window.moveTo(width, height)

ctypes.windll.msvcrt.system(ctypes.c_char_p('cls'.encode()))
print('''
█▀ █▄░█ █ █▀█ █▀▀ █▀█   █▀▀ █▀█ █▀█ █▀ █▀ █░█ ▄▀█ █ █▀█
▄█ █░▀█ █ █▀▀ ██▄ █▀▄   █▄▄ █▄█ █▀▄ ▄█ ▄█ █▀█ █▀█ █ █▀▄

█▄▄ █▄█   █▀▀ █▀▄▀█ █▀█ █▀█ █▀█ █▄█
█▄█ ░█░   ██▄ █░▀░█ █▀▀ █▄█ █▀▄ ░█░
https://github.com/emp0ry/
''')

# Start crosshair.exe
ctypes.windll.msvcrt.system(ctypes.c_char_p('start "Crosshair" crosshair.exe'.encode()))
sleep(3)

# Set up the HTTP server
host_name = '127.0.0.1'
server_port = 23561
http_server = HTTPServer((host_name, server_port), MyHandler)

crosshair_window = gw.getWindowsWithTitle('Crosshair')[0]
width, height = get_screen_size()
crosshair_window.moveTo(width, height)
# Start the server
try:
    http_server.serve_forever()
except KeyboardInterrupt:
    http_server.server_close()
    ctypes.windll.msvcrt.system(ctypes.c_char_p('taskkill /f /IM crosshair.exe /t'.encode()))
    print("Server stopped.")
