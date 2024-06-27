import time
from MouseSim import MouseSim

def record(duration=2):
    """
    Used to print out delta movement for the creation of pattens
    :param duration: <int> : time of recordings
    :return: None
    """
    print("Start")
    deltas = []
    mouse = MouseSim()
    _pos = mouse.get_cursor_pos()
    start = time.time()

    while time.time()-start <= duration:
        pos = mouse.get_cursor_pos()
        print(pos["x"]-_pos["x"], pos["y"]-_pos["y"])
        deltas.append((pos["x"]-_pos["x"], pos["y"]-_pos["y"]))
        time.sleep(0.03)
    print("End")
    return deltas