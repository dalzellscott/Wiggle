import ctypes

class POINT(ctypes.Structure):
    """
    Simple data structure for containing a C x,y position
    """
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]