import json
import time
import mouse
import keyboard
import threading
import asyncio, winrt.windows.media.control as wmc
from win32gui import GetWindowText, GetForegroundWindow

keyboard_keys = ("e", "E") # keys to pause media. case sensitive
mouse_buttons = (mouse.X, mouse.X2) # side buttons
game = "FiveM"
key = -179 # media play/pause key
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        key = config["key"]
        keyboard_keys = config["keys"]
        mouse_buttons = config["mouse"]
        game = config["game"]
except FileNotFoundError:
    print("No config file found, using default settings.")

async def getMediaSession():
    sessions = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = sessions.get_current_session()
    return session

def mediaIs(state):
    session = asyncio.run(getMediaSession())
    if session == None:
        return False
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status #get media state enum and compare to current main media session state


pausedMouse = False
pausedKeyboard = False

def mouse_handler(e):
    global pausedMouse
    global pausedKeyboard
    if pausedKeyboard:
        return
    if not isinstance(e, mouse.ButtonEvent):
        return
    if not e.button in mouse_buttons:
        return
    if game not in GetWindowText(GetForegroundWindow()):
        return
    
    if mediaIs("PLAYING") and e.event_type == "down":
        keyboard.send(key)
        print("Mouse detected, paused.")
        pausedMouse = True
    elif pausedMouse and e.event_type == "up":
        print("Mouse detected, unpaused.")
        keyboard.send(key)
        pausedMouse = False

def key_handler(e):
    global pausedKeyboard
    global pausedMouse
    if pausedMouse:
        return
    if not e.name in keyboard_keys:
        return
    if game not in GetWindowText(GetForegroundWindow()):
        return
    if mediaIs("PLAYING") and e.event_type == "down":
        keyboard.send(key)
        print("Key detected, paused.")
        pausedKeyboard = True
    elif pausedKeyboard and e.event_type == "up":
        print("Key detected, unpaused.")
        keyboard.send(key)
        pausedKeyboard = False
    


    
mouse.hook(mouse_handler)
keyboard.hook(key_handler)
print("Started with following config: ")
print("Trigger Keys: ", keyboard_keys)
print("Trigger Mouse: ", mouse_buttons)
print("Game: ", game)
print("Key to press: ", key)
keyboard.wait()