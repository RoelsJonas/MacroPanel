import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep as delay
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import rotaryio
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import config
from adafruit_onewire.bus import OneWireBus
import adafruit_ds18x20


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

layermap = config.layermap

LAYER_MAX = len(layermap) - 1
LAYER_MIN = 0

buttons = [
    DigitalInOut(board.GP2),
    DigitalInOut(board.GP3),
    DigitalInOut(board.GP4),
    DigitalInOut(board.GP5),
    DigitalInOut(board.GP6),
    DigitalInOut(board.GP7),
]

for btn in buttons:
    btn.direction = Direction.INPUT

state = [0,0,0,0,0,0]

layer = 0

encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)

owBus = OneWireBus(board.A3)
devices = owBus.scan()
# for device in devices:
#     print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))
ds18b20 = adafruit_ds18x20.DS18X20(owBus, devices[0])
ds18b20.resolution = 12
print('Resolution: {0} bits'.format(ds18b20.resolution))
print('Temperature: {0:0.3f} °C'.format(ds18b20.temperature))

displayio.release_displays()
display_bus = displayio.I2CDisplay (busio.I2C(board.GP27, board.GP26), device_address = 0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group()
display.show(splash)
layerText = label.Label(terminalio.FONT, text=("Layer: " + str(layer)), color=0xFFFFFF, x=0, y=5)
splash.append(layerText)
for i in range(len(layermap[layer])):
    if i < 3:
        splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*i + (7-len(layermap[layer][i][1]))*3, y=20))
    else:
        splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*(i-3) + (7-len(layermap[layer][i][1]))*3, y=42))
splash.append(label.Label(terminalio.FONT, text=("Temp: " + str(ds18b20.temperature) + "°C"), color=0xFFFFFF, x=64, y=5))  
print("Startup complete")

while True:
    for i in range(len(buttons)):
        if buttons[i].value != state[i]:
            state[i] = buttons[i].value
            if not state[i]:
                if layermap[layer][5-i][2] == 0:
                    kbd.send(layermap[layer][5-i][0][0])
                elif layermap[layer][5-i][2] == 1:
                    for key in layermap[layer][5-i][0]:
                        kbd.press(key)
                    for key in layermap[layer][5-i][0]:
                        kbd.release(key)
                else:
                    cc.send(layermap[layer][5-i][0][0])
                    
                    
    position = encoder.position
    if position != layer:
        layer = position
        if encoder.position < LAYER_MIN:
            encoder.position = LAYER_MIN
        elif encoder.position > LAYER_MAX:
            encoder.position = LAYER_MAX
        else:
            splash = displayio.Group()
            layerText = label.Label(terminalio.FONT, text=("Layer: " + str(layer)), color=0xFFFFFF, x=0, y =5)
            for i in range(len(layermap[layer])):
                if i < 3:
                    splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*i + (7-len(layermap[layer][i][1]))*3, y = 20))
                else:
                    splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*(i-3) + (7-len(layermap[layer][i][1]))*3, y = 42))
            splash.append(layerText)
            display.show(splash)
    
                
            
        