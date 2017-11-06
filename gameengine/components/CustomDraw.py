from pygame.surface import Surface

from gameengine.core.Component import Component
from gameengine.managers.DrawingManager import DrawingManager


class CustomDraw(Component):
    """Composante qui permet de dessiner manuellement sur une surface."""

    def __init__(self, gameObject):
        super().__init__(gameObject)
        DrawingManager().addObject(self)

    def draw(self) -> Surface:
        surfaces = list(map(lambda script: script.onDraw(), self.gameObject.scripts))
        surfaces = [surface for surface in surfaces if surface is not None]
        if not surfaces:
            return None

        from functools import reduce
        final = reduce(lambda s1, s2: s1 if s1.blit(s2, self._localPosition) else s1, surfaces)

        return final

    def toString(self):
        return """[CustomDraw]"""
