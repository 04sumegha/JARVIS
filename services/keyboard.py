import os
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

def increase_brightness(amount=10):
    current = sbc.get_brightness()[0]
    new_level = min(100, current + amount)
    sbc.set_brightness(new_level)
    return new_level


def decrease_brightness(amount=10):
    current = sbc.get_brightness()[0]
    new_level = max(0, current - amount)
    sbc.set_brightness(new_level)
    return new_level

def increase_volume(amount=5):
    for _ in range(amount):
        pyautogui.press("volumeup")
    return "Volume increased"


def decrease_volume(amount=5):
    for _ in range(amount):
        pyautogui.press("volumedown")
    return "Volume decreased"

def get_current_volume_percent():
    devices = AudioUtilities.GetSpeakers()
    if hasattr(devices, "Activate"):
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
    elif hasattr(devices, "EndpointVolume"):
        volume = devices.EndpointVolume
    else:
        raise RuntimeError("Audio endpoint volume interface not available on this system.")
    return int(round(volume.GetMasterVolumeLevelScalar() * 100))

def adjust_system_level(target, direction=None, amount=None, action="adjust"):
    target = (target or "").strip().lower()
    direction = (direction or "").strip().lower()
    action = (action or "adjust").strip().lower()

    if target == "brightness":
        if action == "query":
            return sbc.get_brightness()[0]
        if amount is None:
            amount = 10
        if direction == "increase":
            return increase_brightness(amount=amount)
        if direction == "decrease":
            return decrease_brightness(amount=amount)
    elif target == "volume":
        if action == "query":
            return get_current_volume_percent()
        if amount is None:
            amount = 5
        if direction == "increase":
            return increase_volume(amount=amount)
        if direction == "decrease":
            return decrease_volume(amount=amount)

    raise ValueError("Invalid request. Use target: brightness|volume and action: adjust|query. For adjust, provide direction: increase|decrease.")

def mute_volume():
    pyautogui.press("volumemute")
    return "Muted"


def unmute_volume():
    pyautogui.press("volumemute")
    return "Unmuted"

def take_screenshot(name: str = None, folder: str = "screenshots"):
    os.makedirs(folder, exist_ok=True)

    if not name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"screenshot_{timestamp}"

    if not name.endswith(".png"):
        name += ".png"

    filepath = os.path.join(folder, name)

    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    return filepath