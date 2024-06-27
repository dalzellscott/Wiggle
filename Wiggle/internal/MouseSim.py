import ctypes
import time
from Wiggle.internal.POINT import POINT
user32 = ctypes.windll.user32


class MouseSim:
    # Constants
    """
    This is a python helper class for interacting with the Win user32 mouse API
    This will allow us to send mouse events to the UI when testing
    Details of this API can be found here
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
    """
    LEFT_DOWN = 0x0002  # (2, 0, 0, 0, 0)
    LEFT_UP = 0x0004  # (4, 0, 0, 0, 0)
    RIGHT_DOWN = 0x0008  # (8, 0, 0, 0, 0)
    RIGHT_UP = 0x0010  # (16, 0, 0, 0, 0)
    MIDDLE_DOWN = 0x0020
    MIDDLE_UP = 0x0040
    MOUSEEVENTF_HWHEEL = 0x0800

    def get_cursor_pos(self):
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return {"x": pt.x, "y": pt.y}

    def wheel(
            self, x, y, up=True,
    ):
        t = 0.03
        counter = 0

        pos = self.get_cursor_pos()

        # Set position
        while counter < 5:
            user32.SetCursorPos(x, y)
            time.sleep(t)

            _pos = self.get_cursor_pos()
            if _pos.get("x") == x and _pos.get("y") == y:
                break
            counter += 1

        delta = 1200 if up else -1200
        user32.mouse_event(self.MOUSEEVENTF_HWHEEL, x, y, delta, 0)

    def move(self, x, y):
        """
        Use this when you wish to click on a section of the screen but you are have had too infer to position of
        the intended object by using an other
        For example using the Text at the centre of the inactive area on the OCTPlanning page to swap the eye
        of the current ONH/RNFL scan
        :param x: <int> : x position to click
        :param y: <int> : y position to click

        :return: None
        """
        t = 0.03
        counter = 0

        # Set position
        user32.SetCursorPos(x, y)
        time.sleep(t)

    def click(self, x, y, click=0, set_pos=True, double_click=False):
        """
        Use this when you wish to click on a section of the screen but you are have had too infer to position of
        the intended object by using an other
        For example using the Text at the centre of the inactive area on the OCTPlanning page to swap the eye
        of the current ONH/RNFL scan
        :param x: <int> : x position to click
        :param y: <int> : y position to click
        :param click: <int> : 0=Left, 1= Middle, 2=Right click
        :param set_pos: <bool> Set mouse to original position
        :param double_click: <bool> : True to perform a double click
        :return: None
        """
        t = 0.03
        counter = 0

        pos = self.get_cursor_pos()

        # Set position
        while counter < 5:
            user32.SetCursorPos(x, y)
            time.sleep(t)

            _pos = self.get_cursor_pos()
            if _pos.get("x") == x and _pos.get("y") == y:
                break
            counter += 1

        # Perform Click(s)
        while True:
            pair = None
            if click == 0:
                pair = [self.LEFT_DOWN, self.LEFT_UP]
            elif click == 1:
                pair = [self.MIDDLE_DOWN, self.MIDDLE_UP]
            elif click == 2:
                pair = [self.RIGHT_DOWN, self.RIGHT_UP]

            if pair is not None:
                user32.mouse_event(pair[0])  # down
                time.sleep(t)
                user32.mouse_event(pair[1])  # up

            if double_click:
                double_click = False
            else:
                break

        if set_pos:
            user32.SetCursorPos(pos.get("x"), pos.get("y"))

    def mouse_drag(
            self,
            offset=(0, 0),
            drag_duration=0.2,
            hold_time=0.0,
            start_loc=None,
            mouse_up=True,
    ):
        """
        This function will click on an object and then drag the mouse by the offset over the drag_duration
        it will then hold the mouse in the final location for the hold_time, before releasing it
        :param offset: <tuple> : (x,y) offset from centre of selected object x/y = 0 in topleft of screen
        :param drag_duration: <float> : time in seconds to drag from centre of offset location
        :param hold_time: <float>: time the mouse is held after the drag is complete before releasing
        :param start_loc: <tuple>: Location to place the cursor before dragging.
                                    If not provided start from the center of the object
        :param mouse_up: <bool>: True to perform mouse up after dragging (set ot false to allow verification steps
        :return: None

        Usage: app.drag_object("NudgeJoystickControl", offset=(0,50), hold_time=1.0)
        """
        t = 0.03
        time_per_step = 0.001

        # Drag end location
        dst = (int(start_loc[0] + offset[0]), int(start_loc[1] + offset[1]))

        # calculate steps to perform drag smoothly
        steps = int(drag_duration / time_per_step)
        delta = (
            float((dst[0] - start_loc[0]) / steps),
            float((dst[1] - start_loc[1]) / steps),
        )

        # Get Current Mouse location
        pos = self.get_cursor_pos()

        # Set position
        user32.SetCursorPos(start_loc[0], start_loc[1])
        time.sleep(t)

        user32.mouse_event(*self.LEFT_DOWN)  # left down
        time.sleep(t)

        # Perform mouse drag
        xx = 0
        yy = 0
        for step in range(0, steps):
            xx = int((start_loc[0] + (step * delta[0])))
            yy = int((start_loc[1] + (step * delta[1])))

            user32.SetCursorPos(xx, yy)
            time.sleep(time_per_step)

        user32.SetCursorPos(*dst)  # Final step to end location
        time.sleep(t)

        # Wait before releasing mouse
        time.sleep(hold_time)

        if mouse_up:
            user32.mouse_event(*self.LEFT_UP)  # left up
            time.sleep(t)

            # move mouse to where is being clicked
            user32.SetCursorPos(pos.get("x"), pos.get("y"))
