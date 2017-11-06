import pygame
from pygame.time import wait

from gameengine.util.Vector2 import Vector2

# le path où se trouve le module gameengine si on l'execute par le terminal
import sys
sys.path.append("../../..")

from gameengine.components.Script import Script
from gameengine.core.GameObject import GameObject
from gameengine.core.Grid import Grid
from gameengine.core.Scene import Scene
from gameengine.core.World import World
from gameengine.managers.PhysicsManager import PhysicsManager
from gameengine.managers.SceneManager import SceneManager

pygame.init()
clock = pygame.time.Clock()

World.display = pygame.display.set_mode((800, 464), pygame.DOUBLEBUF, 32)

from gameengine.tests.SuperMarioBros.sprites import *
from gameengine.tests.SuperMarioBros.Player import Player
from gameengine.tests.SuperMarioBros.blocks import BrickBlock, QuestionBlock, Ground, BillBlaster, Pipe, HardBlock
from gameengine.tests.SuperMarioBros.items import Mushroom, Coin, SuperStar
from gameengine.tests.SuperMarioBros.enemies import Goomba, KoopaTroopa, KoopaParatroopa, BulletBill, \
    StompedKoopaTroopaState
from gameengine.tests.SuperMarioBros.Background import Background


class Listener(GameObject, Script):
    def __init__(self):
        super().__init__()
        self.addScript(self)
        from gameengine.components.Input import Input
        self.addComponent(Input)

    def onKeyDown(self, key):
        if key == pygame.K_r:
            from gameengine.managers.SceneManager import SceneManager
            from gameengine.tests.SuperMarioBros import Level1
            SceneManager().loadScene(Level1)


from gameengine.core.Interpolation import Interpolation, EaseOut
from gameengine.core.Interpolation import Ease


class CameraScript(Script):
    def onCreate(self):
        from gameengine.components.Input import Input
        self.gameObject.addComponent(Input)

    def onMouseDown(self, pos, button):
        def setZoom(abs, rel):
            camera.zoomAt(*pos, camera.zoom + rel)

        camera = self.gameObject
        if button == 4:
            Interpolation(camera.zoom, camera.zoom + 0.1, 300, setZoom, Ease).start()

        elif button == 5:
            Interpolation(camera.zoom, camera.zoom - 0.1, 300, setZoom, Ease).start()

    def onMouseDrag(self, pos, rel, buttons):
        def move(abs, rel):
            self.gameObject.transform.position -= rel

        Interpolation(Vector2(), Vector2(rel), 200, move, EaseOut).start()


class Level1(Scene):
    def onLoad(self):
        self.mainCamera.backgroundColor = (107, 140, 100)
        self.mainCamera.addScript(CameraScript)

        grid = Grid(Vector2(0, -16), Vector2(32, 32))

        # print(grid.at(0, 12).topLeft)
        # print(grid.at(0, 12).midLeft)
        # print(grid.at(0, 12).bottomLeft)
        # print(grid.at(0, 12).midTop)
        # print(grid.at(0, 12).center)
        # print(grid.at(0, 12).midBottom)
        # print(grid.at(0, 12).topRight)
        # print(grid.at(0, 12).midRight)
        # print(grid.at(0, 12).bottomRight)

        bg = Background()

        gd = Ground()
        gd.transform.position = grid.at(0, 13).topLeft
        gd.transform.size = Vector2(bg.transform.size.x, 32*3)

        # print("GD SIZE", gd.transform.size)

        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(4 + 12, 9).topLeft
        BrickBlock().transform.position = grid.at(8 + 12, 9).topLeft
        QuestionBlock(Mushroom).transform.position = grid.at(9+12, 9).topLeft
        BrickBlock().transform.position = grid.at(10 + 12, 9).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(11 + 12, 9).topLeft
        BrickBlock().transform.position = grid.at(12 + 12, 9).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(10 + 12, 5).topLeft

        Goomba().transform.position = grid.at(21, 12).topLeft
        Goomba().transform.position = grid.at(23, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft
        # Goomba().transform.position = grid.at(22, 12).topLeft

        Pipe(1*32).transform.position = grid.at(29, 12).bottomLeft
        Pipe(2*32).transform.position = grid.at(39, 12).bottomLeft

        Goomba().transform.position = grid.at(40, 12).topLeft

        Pipe(3*32).transform.position = grid.at(47, 12).bottomLeft

        Goomba().transform.position = grid.at(50, 12).topLeft
        Goomba().transform.position = grid.at(52, 12).topLeft

        Pipe(3*32).transform.position = grid.at(58, 12).bottomLeft


        BrickBlock().transform.position = grid.at(77, 9).topLeft
        QuestionBlock(Mushroom).transform.position = grid.at(78, 9).topLeft
        BrickBlock().transform.position = grid.at(79, 9).topLeft

        BrickBlock().transform.position = grid.at(80, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 1, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 2, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 3, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 4, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 5, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 6, 5).topLeft
        BrickBlock().transform.position = grid.at(80 + 7, 5).topLeft

        Goomba().transform.position = grid.at(80, 4).topLeft
        Goomba().transform.position = grid.at(82, 4).topLeft

        BrickBlock().transform.position = grid.at(91, 5).topLeft
        BrickBlock().transform.position = grid.at(91 + 1, 5).topLeft
        BrickBlock().transform.position = grid.at(91 + 2, 5).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(91 + 3, 5).topLeft

        BrickBlock().transform.position = grid.at(91 + 3, 9).topLeft

        Goomba().transform.position = grid.at(97, 12).topLeft
        Goomba().transform.position = grid.at(99, 12).topLeft

        BrickBlock().transform.position = grid.at(100, 9).topLeft
        QuestionBlock(SuperStar).transform.position = grid.at(101, 9).topLeft

        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(106, 9).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(109, 9).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(112, 9).topLeft
        QuestionBlock(Mushroom).transform.position = grid.at(109, 5).topLeft

        KoopaTroopa().transform.position = grid.at(107, 12).topLeft

        Goomba().transform.position = grid.at(114, 12).topLeft
        Goomba().transform.position = grid.at(116, 12).topLeft

        BrickBlock().transform.position = grid.at(118, 9).topLeft

        BrickBlock().transform.position = grid.at(121, 5).topLeft
        BrickBlock().transform.position = grid.at(122, 5).topLeft
        BrickBlock().transform.position = grid.at(123, 5).topLeft

        BrickBlock().transform.position = grid.at(128, 5).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(129, 5).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(130, 5).topLeft
        BrickBlock().transform.position = grid.at(131, 5).topLeft

        BrickBlock().transform.position = grid.at(129, 9).topLeft
        BrickBlock().transform.position = grid.at(130, 9).topLeft

        def stairs(iBase, jBase, height, ascending=True, continuation=0):
            if ascending:
                iMin = iBase
                for j in range(jBase, jBase - height, -1):
                    for i in range(iMin, iBase + height):
                        HardBlock().transform.position = grid.at(i, j).topLeft
                    iMin += 1

                for i in range(continuation):
                    for j in range(jBase, jBase - height, -1):
                        HardBlock().transform.position = grid.at(iBase + height + i, j).topLeft

            else:
                iMax = iBase + height
                for j in range(jBase, jBase - height, -1):
                    for i in range(iBase, iMax):
                        HardBlock().transform.position = grid.at(i, j).topLeft
                    iMax -= 1


        stairs(134, 12, 4)
        stairs(140, 12, 4, False)

        stairs(148, 12, 4, continuation=1)
        stairs(155, 12, 4, False)


        Pipe(1*32).transform.position = grid.at(164, 12).bottomLeft

        BrickBlock().transform.position = grid.at(168, 9).topLeft
        BrickBlock().transform.position = grid.at(169, 9).topLeft
        QuestionBlock(QuestionBlock.SpinningCoin).transform.position = grid.at(170, 9).topLeft
        BrickBlock().transform.position = grid.at(171, 9).topLeft

        Goomba().transform.position = grid.at(174, 12).topLeft
        Goomba().transform.position = grid.at(176, 12).topLeft

        Pipe(1*32).transform.position = grid.at(180, 12).bottomLeft

        stairs(181, 12, 8, continuation=1)

        self.player = Player()
        self.player.transform.position = grid.at(5, 12).midBottom

        # BrickBlock().transform.position = grid.at(5, 13).topLeft
        # self.player.transform.position = grid.at(16, 6).midBottom

        Listener()


if __name__ == "__main__":
    PhysicsManager().gravity = Vector2(0, 0.6)

    SceneManager().loadScene(Level1)

    while True:
        World.update()
        World.draw()

        clock.tick(60)
        # wait(1)