from pynput import keyboard

class DetectInput():
    """
    This class is used to listen for when any key is pressed
    if it is then restart the timer
    """
    def __init__(self):
        self.keyboard_listener = self._listen_keyboard()
        self.keyboard_listener.start()

        self.detected = False


    def _listen_keyboard(self):
        listener = keyboard.Listener(on_press=self._on_press)
        return listener

    def _on_press(self, key):
        self.detected = True