import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.core.Component import Component
from gameengine.core.Sprite import Sprite
from gameengine.managers.DrawingManager import DrawingManager
from gameengine.util.Timer import Timer


class SpriteRenderer(Component):
    """Permet l'animation d'un Sprite, gére le timing et le conteur du frame"""

    def __init__(self, gameObject):
        super().__init__(gameObject)
        DrawingManager().addObject(self)

        self.sprite = None
        self.iFrame = 0
        self._interval = 0
        self.timer = None

        self.repeatImage = False

    def setSprite(self, sprite: Sprite, overrideTransformSize=True):
        if self.sprite == sprite:
            return

        self.sprite = sprite
        self.iFrame = 0
        self._interval = sprite.interval

        self.overrideTransformSize = overrideTransformSize

        self.stop()
        if self._interval > -1:
            self.start()

        if self.overrideTransformSize:
            self.gameObject.transform.size = Vector2(self.sprite.frames[0].get_size())
        else:
            self.size = Vector2(self.sprite.frames[0].get_size())

        return self

    def onDestroy(self):
        self.sprite = None
        self.stop()

    def start(self):
        if self.timer is not None:
            self.timer.stop()
        self.timer = Timer(self._interval, self.step).start()

    def stop(self):
        if self.timer is not None:
            self.timer.stop()

    def pause(self):
        if self.timer is not None:
            self.timer.pause()

    def resume(self):
        if self.timer is not None:
            self.timer.resume()

    def step(self):
        self.iFrame += 1
        if self.iFrame >= len(self.sprite.frames):
            self.iFrame = 0

    def getFrame(self) -> pygame.Surface:
        frame = self.sprite.frames[self.iFrame]
        for script in self.gameObject.scripts:
            frame = script.alterSpriteFrame(frame)

        return frame

    def getFrameSize(self) -> Vector2:
        assert self.sprite.frames
        return Vector2(self.sprite.frames[self.iFrame].get_size())

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        if self.timer is not None:
            self.timer.interval = value

    def draw(self):
        if not self.sprite or not self.sprite.frames:
            return None

        frame = self.getFrame()

        if not self.repeatImage:
            return frame
        else:
            tiledSurface = pygame.Surface(self.size.tuple()).convert_alpha()
            tiledSurface.fill((255, 255, 255))

            for i in range(0, int(self.size.x), frame.get_width()):
                for j in range(0, int(self.size.y), frame.get_height()):
                    tiledSurface.blit(frame, (i, j), special_flags=pygame.BLEND_RGBA_MIN)

            return tiledSurface


    def toString(self):
        return """[SpriteRenderer]
Interval: {}ms
Current frame index: {}
Total frames: {}""".format(self.interval, self.iFrame, len(self.sprite.frames))