import pygame
# from pygame.rect import Rect
from gameengine.util.Vector2 import Vector2

from gameengine.core.Sprite import Sprite
from gameengine.util.Rect import Rect
from gameengine.util.util import scaleRect

zoom = 2

bigMarioSize = Vector2(16, 32)
smallMarioSize = Vector2(16, 16)
blockSize1 = Vector2(16, 16)
blockSize2 = Vector2(16, 32)
itemSize = Vector2(16, 16)
enemySize1 = Vector2(16, 16)
enemySize2 = Vector2(16, 24)

bgOverworldSurface = pygame.image.load("sprites/bgOverworld.png").convert_alpha()
bgOverworldSurface = pygame.transform.scale(bgOverworldSurface, (bgOverworldSurface.get_width() * zoom, bgOverworldSurface.get_height() * zoom))

playerSheet = pygame.image.load("sprites/player.png").convert_alpha()
playerSheet = pygame.transform.scale(playerSheet, (playerSheet.get_width() * zoom, playerSheet.get_height() * zoom))

playerSprites = {
    "small": {
        "stand":    Sprite(playerSheet, [scaleRect(Rect(80, 34, *smallMarioSize), zoom)], -1),

        "walk":     Sprite(playerSheet, [scaleRect(Rect(97, 34, *smallMarioSize), zoom),
                                        scaleRect(Rect(114, 34, *smallMarioSize), zoom),
                                        scaleRect(Rect(131, 34, *smallMarioSize), zoom)], 100),

        "break":    Sprite(playerSheet, [scaleRect(Rect(148, 34, *smallMarioSize), zoom)], -1),

        "jump":     Sprite(playerSheet, [scaleRect(Rect(165, 34, *smallMarioSize), zoom)], -1),

        "crouch":   Sprite(playerSheet, [scaleRect(Rect(80, 34, *smallMarioSize), zoom)], -1),

        "dying":    Sprite(playerSheet, [scaleRect(Rect(182, 34, *smallMarioSize), zoom)], -1)
    },

    "big": {
        "stand": Sprite(playerSheet, [scaleRect(Rect(80, 1, *bigMarioSize), zoom)], -1),

        "walk": Sprite(playerSheet, [scaleRect(Rect(97, 1, *bigMarioSize), zoom),
                                    scaleRect(Rect(114, 1, *bigMarioSize), zoom),
                                    scaleRect(Rect(131, 1, *bigMarioSize), zoom)], 100),

        "break": Sprite(playerSheet, [scaleRect(Rect(148, 1, *bigMarioSize), zoom)], -1),

        "jump": Sprite(playerSheet, [scaleRect(Rect(165, 1, *bigMarioSize), zoom)], -1),

        "crouch": Sprite(playerSheet, [scaleRect(Rect(182, 1, *bigMarioSize), zoom)], -1)
    }
}



tilesetSheet = pygame.image.load("sprites/tileset.png").convert_alpha()
tilesetSheet = pygame.transform.scale(tilesetSheet, (tilesetSheet.get_width() * zoom, tilesetSheet.get_height() * zoom))

tilesetSprites = {
    "ground":       Sprite(tilesetSheet, [scaleRect(Rect(0, 0, *blockSize1), zoom)], -1),

    "bill_blaster": Sprite(tilesetSheet, [scaleRect(Rect(144, 0, *blockSize2), zoom)], -1),

    "pipeHead":     Sprite(tilesetSheet, [scaleRect(Rect(0, 128, 32, 16), zoom)], -1),

    "pipeBody":     Sprite(tilesetSheet, [scaleRect(Rect(2, 144, 28, 16), zoom)], -1),

    "hard":         Sprite(tilesetSheet, [scaleRect(Rect(0, 16, *blockSize1), zoom)], -1)
}

blocksSheet = pygame.image.load("sprites/blocks.png").convert_alpha()
blocksSheet = pygame.transform.scale(blocksSheet, (blocksSheet.get_width() * zoom, blocksSheet.get_height() * zoom))

blocksSprites = {
    "brick": {
        "normal": Sprite(blocksSheet, [scaleRect(Rect(272, 112, *blockSize1), zoom)], -1),

        "hit_empty": Sprite(blocksSheet, [scaleRect(Rect(288, 112, *blockSize1), zoom)], -1),

        "pieces": {
            "1": Sprite(blocksSheet, [scaleRect(Rect(304, 112, 8, 8), zoom)], -1),

            "2": Sprite(blocksSheet, [scaleRect(Rect(312, 112, 8, 8), zoom)], -1),

            "3": Sprite(blocksSheet, [scaleRect(Rect(304, 120, 8, 8), zoom)], -1),

            "4": Sprite(blocksSheet, [scaleRect(Rect(312, 120, 8, 8), zoom)], -1)
        },
        "hit": Sprite(blocksSheet, [scaleRect(Rect(320, 112, *blockSize1), zoom)], -1),

        "hit_after": Sprite(blocksSheet, [scaleRect(Rect(336, 112, *blockSize1), zoom)], -1)
    },

    "question": {
        "normal": Sprite(blocksSheet, [scaleRect(Rect(80, 112, *blockSize1), zoom),
                      scaleRect(Rect(96, 112, *blockSize1), zoom),
                      scaleRect(Rect(112, 112, *blockSize1), zoom),
                      scaleRect(Rect(96, 112, *blockSize1), zoom),
                      scaleRect(Rect(80, 112, *blockSize1), zoom),
                      scaleRect(Rect(80, 112, *blockSize1), zoom)], 100),

        "hit": Sprite(blocksSheet, [scaleRect(Rect(128, 112, *blockSize1), zoom)], -1),

        "hit_after": Sprite(blocksSheet, [scaleRect(Rect(144, 112, *blockSize1), zoom)], -1)
    }
}

itemsSheet = pygame.image.load("sprites/items.png").convert_alpha()
itemsSheet = pygame.transform.scale(itemsSheet, (itemsSheet.get_width() * zoom, itemsSheet.get_height() * zoom))

itemsSprites = {
    "coin": Sprite(itemsSheet, [scaleRect(Rect(384, 16, *itemSize), zoom),
                  scaleRect(Rect(400, 16, *itemSize), zoom),
                  scaleRect(Rect(416, 16, *itemSize), zoom),
                  scaleRect(Rect(400, 16, *itemSize), zoom),
                  scaleRect(Rect(384, 16, *itemSize), zoom),
                  scaleRect(Rect(384, 16, *itemSize), zoom)], 100),

    "rotatingCoin": Sprite(itemsSheet, [scaleRect(Rect(0, 112, *itemSize), zoom),
                  scaleRect(Rect(16, 112, *itemSize), zoom),
                  scaleRect(Rect(32, 112, *itemSize), zoom)], 50),

    "mushroom": Sprite(itemsSheet, [scaleRect(Rect(0, 0, *itemSize), zoom)], -1),

    "superStar": Sprite(itemsSheet, [scaleRect(Rect(0, 48, *itemSize), zoom),
                  scaleRect(Rect(16, 48, *itemSize), zoom),
                  scaleRect(Rect(32, 48, *itemSize), zoom),
                  scaleRect(Rect(48, 48, *itemSize), zoom)], 100)
}

enemiesSheet = pygame.image.load("sprites/enemies.png").convert_alpha()
enemiesSheet = pygame.transform.scale(enemiesSheet, (enemiesSheet.get_width() * zoom, enemiesSheet.get_height() * zoom))

enemiesSprites = {
    "goomba": {
        "walking": Sprite(enemiesSheet, [scaleRect(Rect(0, 16, *enemySize1), zoom),
                                scaleRect(Rect(16, 16, *enemySize1), zoom)], 200),

        "stomped": Sprite(enemiesSheet, [scaleRect(Rect(32, 16, *enemySize1), zoom)], -1)
    },

    "koopa_troopa": {
        "walking": Sprite(enemiesSheet, [scaleRect(Rect(96, 8, *enemySize2), zoom),
                                scaleRect(Rect(112, 8, *enemySize2), zoom)], 200),

        "stomped": Sprite(enemiesSheet, [scaleRect(Rect(160, 16, *enemySize1), zoom)], -1),

        "recovering": Sprite(enemiesSheet, [scaleRect(Rect(160, 16, *enemySize1), zoom),
                                    scaleRect(Rect(176, 16, *enemySize1), zoom)], 200),

        "flying": Sprite(enemiesSheet, [scaleRect(Rect(128, 8, *enemySize2), zoom),
                                scaleRect(Rect(144, 8, *enemySize2), zoom)], 200)
    },

    "bullet_bill": Sprite(enemiesSheet, [scaleRect(Rect(560, 16, *enemySize1), zoom)], -1)
}