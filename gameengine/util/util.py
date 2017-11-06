import re
from array import array

import cairo
import gi

gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg

import pygame

from gameengine.core.Constants import *
from gameengine.util.Rect import Rect


def Singleton(class_):
    class class_w(class_):
        _instance = None

        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w,
                                          class_).__new__(class_,
                                                          *args,
                                                          **kwargs)
                class_w._instance._sealed = False
            return class_w._instance

        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True

    class_w.__name__ = class_.__name__
    return class_w


def vecToSide(dx, dy):
    if dx < 0:
        return LEFT_SIDE
    elif dx > 0:
        return RIGHT_SIDE
    if dy < 0:
        return TOP_SIDE
    elif dy > 0:
        return BOTTOM_SIDE


def scaleRect(rect: Rect, n: int) -> Rect:
    copy = rect.copy()
    copy.x *= n
    copy.y *= n
    copy.width *= n
    copy.height *= n
    return copy

def svgToSurface(filename, width, height):
    file = open(filename, 'r')
    fileStr = file.read()

    fileStr = re.sub('width\s*=\s*\"([0-9]+)\"', 'width=\"{}\"'.format(width), fileStr, 1)
    fileStr = re.sub('height\s*=\s*\"([0-9]+)\"', 'height=\"{}\"'.format(height), fileStr, 1)

    handle = Rsvg.Handle()
    svg = handle.new_from_data(fileStr.encode())

    width, height = map(svg.get_property, ("width", "height"))

    data = array('b')
    data.frombytes((chr(0) * width * height * 4).encode())

    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, width, height, width * 4)
    ctx = cairo.Context(surface)
    svg.render_cairo(ctx)

    image = pygame.image.frombuffer(data.tostring(), (width, height), "RGBA")

    return image


def clamp(val, minVal, maxVal): return max(minVal, min(val, maxVal))

def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

from time import time
def print_timing(func):
    def wrapper(*arg):
        t1 = time()
        res = func(*arg)
        t2 = time()
        print('{} took {:0.3f} ms'.format(func.__name__, (t2 - t1) * 1000.0))
        return res

    return wrapper