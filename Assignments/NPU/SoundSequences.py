from psychopy import visual, core, prefs, sound, event
from psychopy.iohub import launchHubServer
from psychopy.iohub.client.keyboard import Keyboard
import serial
import time


def report_event(ser: serial.Serial, event_num: int):
    if not ser.is_open:
        ser.open()
    print(f"Sending event {event_num} to BioPac - {hex(event_num).encode()}")
    ser.write(hex(event_num).encode())
    time.sleep(0.05)
    ser.write("RR".encode())
    ser.close()


AUDIO_PREFIX = './sound'
AUDIO_SUFFIX = '.mp3'

io = launchHubServer()
keyboard = io.devices.keyboard

ser = serial.Serial('COM4', 115200, bytesize=serial.EIGHTBITS, timeout=1)
window = visual.Window(monitor="testMonitor", color=(0.6, 0.6, 0.6), winType='pyglet',
                       fullscr=True, units="pix")


for i in range(1, 5):
    text = visual.TextStim(window, text=f"Sound {i}", height=44)
    text.draw()
    window.flip()

    report_event(ser, i * 10)

    sound_name = AUDIO_PREFIX + str(i) + AUDIO_SUFFIX
    audio_stim = sound.Sound(sound_name)

    audio_stim.play()
    while not audio_stim.isFinished:
        for event in keyboard.getEvents():
            if event.key == "escape":
                audio_stim.stop()
                window.close()
                core.quit()

    start_time = time.time()
    accept = False
    while time.time() < start_time + 600 and not accept:
        for event in keyboard.getEvents():
            if event.key == "escape":
                window.close()
                core.quit()
            elif event.key == " ":
                accept = True

