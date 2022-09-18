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


# Generate the display image for the current selected layer
def generateSplash(temp=False):
    splash = displayio.Group()
    layerText = label.Label(terminalio.FONT, text=("Layer: " + str(layer)), color=0xFFFFFF, x=0, y =5)
    splash.append(layerText)
    for i in range(len(layermap[layer])):
        if i < 3:
            splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*i + (7-len(layermap[layer][i][1]))*3, y = 20))
        else:
            splash.append(label.Label(terminalio.FONT, text=layermap[layer][i][1], color=0xFFFFFF, x=43*(i-3) + (7-len(layermap[layer][i][1]))*3, y = 42))
    if temp:
        splash.append(label.Label(terminalio.FONT, text=("Temp: " + str(ds18b20.temperature) + "°C"), color=0xFFFFFF, x=64, y=5)) 
    return splash

# Configure all the GPIO pins that are connected to the buttons as input
def attachButtons():
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
    return buttons

# Configure the thermometer
def attachThermometer():
    owBus = OneWireBus(board.A3)
    devices = owBus.scan()
    ds18b20 = adafruit_ds18x20.DS18X20(owBus, devices[0])
    ds18b20.resolution = 12
    return ds18b20

# Configure the screen and display initial layer
def attachDisplay():
    displayio.release_displays()
    display_bus = displayio.I2CDisplay (busio.I2C(board.GP27, board.GP26), device_address = 0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
    splash = generateSplash(temp=True)
    display.show(splash)
    return display

# Send a combination of keystrokes
def sendMacro(keys):
    for key in keys:
        kbd.press(key)
    for key in keys:
        kbd.release(key)
        
def loop():
    global layer
    
    # Check if button has been pressed or released
    for i in range(len(buttons)):
        if buttons[i].value != state[i]:
            state[i] = buttons[i].value
            if not state[i]:
                if layermap[layer][5-i][2] == 0:
                    kbd.send(layermap[layer][5-i][0][0])
                elif layermap[layer][5-i][2] == 1:
                    sendMacro(layermap[layer][5-i][0])
                elif layermap[layer][5-i][2] == 2:
                    cc.send(layermap[layer][5-i][0][0])
                elif layermap[layer][5-i][2] == 3:
                    splash = generateSplash(temp=True)
                    display.show(splash)
                else:
                    print("Invalid Config")
                   
    # Check if the layer has been changed
    position = encoder.position
    if position != layer:
        if encoder.position < LAYER_MIN:
            encoder.position = LAYER_MIN
        elif encoder.position > LAYER_MAX:
            encoder.position = LAYER_MAX
        else:
            layer = position
            splash = generateSplash()
            display.show(splash)
    

##############################
            Main
##############################

# Setup HID device (both keys and media input)
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Configure button binding
layermap = config.layermap
LAYER_MAX = len(layermap) - 1
LAYER_MIN = 0
layer = config.defaultLayer

buttons = attachButtons()
state = [0,0,0,0,0,0]
encoder = rotaryio.IncrementalEncoder(board.GP15, board.GP14)

ds18b20 = attachThermometer()
display = attachDisplay()

print("Startup complete")

while True:
    loop()
