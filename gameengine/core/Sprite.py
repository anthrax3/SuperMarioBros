import pygame


class Sprite:
    """Structure d'un sprite, génère(découpe) les surfaces sur base des rectangles."""

    def __init__(self, source: pygame.Surface, rects=None, interval=-1):
        self.source = source
        self.rects = rects
        self.interval = interval

        self.frames = []

        if self.rects is None:
            surface = pygame.Surface((source.get_width(), source.get_height()), pygame.SRCALPHA, 32).convert_alpha()
            surface.blit(source, (0, 0))
            self.frames.append(surface)
        else:
            for rect in rects:
                surface = pygame.Surface(rect.size.tuple(), pygame.SRCALPHA, 32).convert_alpha()
                surface.blit(source, (0, 0), rect.toPygameRect())
                self.frames.append(surface)