import pygame
from gameengine.util.Vector2 import Vector2

from gameengine.core.ObjectManager import ObjectManager
from gameengine.managers.CameraManager import CameraManager
from gameengine.util.util import Singleton


@Singleton
class InputManager(ObjectManager):
    def __init__(self):
        super().__init__()

        self.gameObject = None
        self.isDragged = False

    def onUpdate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from gameengine.core.World import World
                World.shutdown()
            elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN or \
                event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

                self.dispatchEvent(event)

    def dispatchEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouseMotion(Vector2(event.pos), Vector2(event.rel), event.buttons)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDown(Vector2(event.pos), event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouseUp(Vector2(event.pos), event.button)
        elif event.type == pygame.KEYDOWN:
            self.keyDown(event.key)
        elif event.type == pygame.KEYUP:
            self.keyUp(event.key)

    def mouseMotion(self, windowPos, rel, buttons):
        frontCamera = next(self.getCamerasAt(*windowPos), None)

        if frontCamera is None:
            return

        if buttons[0] or buttons[1] or buttons[2]:
            if self.gameObject:
                self.isDragged = True
                gamePos = frontCamera.windowToGamePos(*windowPos)
                for script in self.gameObject.scripts:
                    script.onMouseDrag(gamePos, rel / frontCamera.zoom, buttons)
        else:
            self.gameObject = next(self.getGameObjectsAt(*windowPos), None)

            if self.gameObject:
                gamePos = frontCamera.windowToGamePos(*windowPos)
                for script in self.gameObject.scripts:
                    script.onMouseHover(gamePos, rel / frontCamera.zoom)
            else:
                self.gameObject = None

    def mouseDown(self, windowPos, button):
        frontCamera = next(self.getCamerasAt(*windowPos), None)
        if frontCamera is None:
            return

        self.gameObject = next(self.getGameObjectsAt(*windowPos), None)

        if self.gameObject:
            gamePos = frontCamera.windowToGamePos(*windowPos)
            for script in self.gameObject.scripts:
                script.onMouseDown(gamePos, button)

    def mouseUp(self, windowPos, button):
        frontCamera = next(self.getCamerasAt(*windowPos), None)
        if frontCamera is None:
            return

        gamePos = frontCamera.windowToGamePos(*windowPos)

        if self.gameObject:
            for script in self.gameObject.scripts:
                script.onMouseUp(gamePos, button)

        if button == 1:
            if not self.isDragged:
                if self.gameObject:
                    for script in self.gameObject.scripts:
                        script.onMouseClicked(windowPos)
            self.isDragged = False

        self.gameObject = None

    def keyDown(self, key):
        for i in range(len(self.objects)):
            for script in self.objects[i].gameObject.scripts:
                script.onKeyDown(key)

    def keyUp(self, key):
        for i in range(len(self.objects)):
            for script in self.objects[i].gameObject.scripts:
                script.onKeyUp(key)

    def getCamerasAt(self, windowX, windowY):
        for camera in CameraManager().objects:
            if camera.windowRect.collidePoint(windowX, windowY):
                yield camera

    def getGameObjectsAt(self, windowX, windowY):
        for camera in self.getCamerasAt(windowX, windowY):
            gamePos = camera.windowToGamePos(windowX, windowY)

            for i in range(len(self.objects) - 1, -1, -1):
                component = self.objects[i]
                if not component.enabled:
                    continue

                if component.worldRect.collidePoint(gamePos.x, gamePos.y):
                    yield component.gameObject

    def objectListChanged(self):
        self.sort()

    def sort(self):
        self.objects.sort(key=lambda c: c.gameObject.transform.depth)
