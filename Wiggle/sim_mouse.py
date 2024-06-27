"""
Will record the CPU/Ram usage of a given process or system

Usage:
  sim_mouse.py
  sim_mouse.py [--record]
  sim_mouse.py [--duration=<duration>]
  sim_mouse.py -h | --help

Example:
  sim_mouse.py --duration=180
  sim_mouse.py --record
  sim_mouse.py --help

Options:
  -h --help                  : Show this screen.
  -r --record                : Sets Wiggle into Record mode [default: False].
  -d --duration=<duration>   : Set the time of inactivity required to trigger a wiggle [default: 180].
"""

import ctypes
import random
import time
import pyautogui
from docopt import docopt

from Wiggle.internal.DirectInput import DetectInput
from Wiggle.internal.MouseSim import MouseSim
from Wiggle.internal.read import read

user32 = ctypes.windll.user32

def main():
    arguments = docopt(__doc__)
    _record = arguments["--record"]
    _timer = int(arguments["--duration"])

    if _record:
        _record_pattern()
    else:
        _wiggle(timer_default=_timer)

def _record_pattern():
    pass

def _wiggle(timer_default, debug=False):
    mouse = MouseSim()
    keyboard = DetectInput()

    timer = timer_default
    _pos = mouse.get_cursor_pos()

    while True:  # Program loop
        while True:  # Timer trigger loop
            pos = mouse.get_cursor_pos()
            timer -= 1
            time.sleep(1)
            _pos = mouse.get_cursor_pos()

            if debug:
                print(f"keyboard.detected: {timer}")

            # Reset timer due to user input
            if pos != _pos or keyboard.detected:
                timer = timer_default
                keyboard.detected = False

            # Reset timer and trigger pattern
            if timer <= 0:
                timer = timer_default
                keyboard.detected = False
                break

        # Movement
        if pos == _pos:
            x = pos.get("x")
            y = pos.get("y")
            for _ in range(1):
                pattern = random.randint(1,5)
                deltas = read(pattern)

                for delta in deltas:
                    mouse.move(x + delta[0], y + delta[1])
                    time.sleep(0.02)
            mouse.move(x, y)
            pyautogui.keyDown("shift")
            pyautogui.keyUp("shift")


if __name__ == "__main__":
    main()
    # #record()
    #


