from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
KEY = 0
MACRO = 1
MEDIA = 2
TEMP = 3

# Change this value to the layer that needs to be chosen at boot
defaultLayer = 0


l0 = [
    [[Keycode.PAGE_UP], "Mute", KEY],
    [[Keycode.PAGE_DOWN], "Deafen", KEY],
    [[Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE], "TaskMan", MACRO],
    [[ConsumerControlCode.SCAN_PREVIOUS_TRACK], "Prev", MEDIA],
    [[ConsumerControlCode.PLAY_PAUSE], "Pause", MEDIA],
    [[ConsumerControlCode.SCAN_NEXT_TRACK], "Next", MEDIA],
    ]

l1= [
    [[Keycode.WINDOWS, Keycode.SHIFT, Keycode.S], "Snip", MACRO],
    [[Keycode.WINDOWS, Keycode.E], "Files", MACRO],
    [[Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE], "TaskMan", MACRO],
    [[Keycode.WINDOWS, Keycode.THREE], "Brave", MACRO],
    [[Keycode.WINDOWS, Keycode.FOUR], "Spotify", MACRO],
    [[Keycode.WINDOWS, Keycode.D], "Desktop", MACRO],
    ]

l2 = [
    [[ConsumerControlCode.MUTE], "VolMute", MEDIA],
    [[ConsumerControlCode.VOLUME_DECREMENT], "VolDown", MEDIA],
    [[ConsumerControlCode.VOLUME_INCREMENT], "VolUp", MEDIA],
    [[ConsumerControlCode.SCAN_PREVIOUS_TRACK], "Prev", MEDIA],
    [[ConsumerControlCode.PLAY_PAUSE], "Pause", MEDIA],
    [[ConsumerControlCode.SCAN_NEXT_TRACK], "Next", MEDIA],
    ]

l3= [
    [None, "Temp", TEMP],
    [[Keycode.B], "B", KEY],
    [[Keycode.C], "C", KEY],
    [[Keycode.D], "D", KEY],
    [[Keycode.E], "E", KEY],
    [[Keycode.F], "F", KEY],
    ]

l4 = [
    [None, "Temp", TEMP],
    [[Keycode.PAGE_DOWN], "Deafen", KEY],
    [[ConsumerControlCode.PLAY_PAUSE], "Pause", MEDIA],
    [[Keycode.THREE], "THREE", KEY],
    [[Keycode.FOUR], "FOUR", KEY],
    [[Keycode.FIVE], "FIVE", KEY],
    ]

l5= [
    [[Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE], "TaskMan", MACRO],
    [[Keycode.B], "B", KEY],
    [[Keycode.C], "C", KEY],
    [[Keycode.D], "D", KEY],
    [[Keycode.E], "E", KEY],
    [[Keycode.F], "F", KEY],
    ]

layermap = {
    (0): l0,
    (1): l1,
    (2): l2,
    (3): l3,
#    (4): l4,
#    (5): l5,
    }
