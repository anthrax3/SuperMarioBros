import pygame

from gameengine.core.ObjectManager import ObjectManager
from gameengine.managers.DrawingManager import DrawingManager
from gameengine.util.util import Singleton


@Singleton
class CameraManager(ObjectManager):
    def __init__(self):
        super().__init__()

        self.visibleGameObjects = []

    def draw(self):
        for camera in CameraManager().objects:
            if not camera.enabled:
                continue

            cameraSurface = pygame.Surface(camera.windowRect.size.tuple())

            cameraSurface.fill(camera.backgroundColor)

            for component in DrawingManager().objects:
                if not component.enabled:
                    continue

                if camera.transform.worldRect.collideRect(component.worldRect):
                    # onBecameVisible()
                    if component.gameObject not in self.visibleGameObjects:
                        self.visibleGameObjects.append(component.gameObject)
                        for script in component.gameObject.scripts:
                            script.onBecameVisible()

                    # Draw
                    drawingSurface = component.draw()
                    if drawingSurface is None:
                        continue

                    # drawingPos = component.position - camera.transform.position
                    drawingPos = (component.worldRect.topLeft - camera.transform.worldRect.topLeft) * camera.zoom

                    from gameengine.util.Vector2 import Vector2
                    newSize = Vector2(drawingSurface.get_size()) * camera.zoom

                    if camera.zoom != 1.0:
                        drawingSurface = pygame.transform.scale(drawingSurface, (int(newSize.x), int(newSize.y)))

                    cameraSurface.blit(drawingSurface, drawingPos.tuple())

                else:
                    # onBecameInvisible()
                    if component.gameObject in self.visibleGameObjects:
                        self.visibleGameObjects.remove(component.gameObject)
                        for script in component.gameObject.scripts:
                            script.onBecameInvisible()

            # cameraSurface = pygame.transform.rotate(cameraSurface, self.i)
            # self.i += 1

            from gameengine.core.World import World
            World.display.blit(cameraSurface, camera.windowRect.topLeft.tuple())

    def objectListChanged(self):
        self.sort()

    def sort(self):
        self.objects.sort(key=lambda camera: camera.transform.depth)