import sys
from abc import ABC

import pygame

from gameengine.core.Interpolation import updateInterpolations
from gameengine.managers.CameraManager import CameraManager
from gameengine.managers.CollisionManager import CollisionManager
from gameengine.managers.InputManager import InputManager
from gameengine.managers.PhysicsManager import PhysicsManager
from gameengine.util.Queue import Queue
from gameengine.util.Timer import updateTimers


class World(ABC):
    """Gére l'existance des GameObjects.
    Fournit des méthodes pour chercher des GameObjects par son nom unique ou tag(plusieurs)"""

    display: pygame.Surface = None
    gameObjects = []

    gameObjectCreationQueue = Queue()
    gameObjectDestructionQueue = Queue()

    @classmethod
    def instantiate(cls, Class, position, parent=None, instantiateInWorldSpace=True):
        gameObject = Class()

        if parent is not None:
            gameObject.transform.parent = parent
            if instantiateInWorldSpace is True:
                gameObject.transform.position = position
            else:
                gameObject.transform.localPosition = position
        else:
            gameObject.transform.position = position

        cls.gameObjectCreationQueue.put(gameObject)

        return gameObject

    @classmethod
    def _addGameObjects(cls):
        for gameObject in cls.gameObjectCreationQueue.get():
            cls.gameObjects.append(gameObject)

    @classmethod
    def _removeGameObjects(cls):
        for gameObject in cls.gameObjectDestructionQueue.get():
            gameObject.onDestroy()

            cls.gameObjects.remove(gameObject)

            for script in gameObject.scripts:
                gameObject.removeScript(script)

            for component in gameObject.components:
                gameObject.removeComponent(component)

    @classmethod
    def destroyGameObject(cls, gameObject):
        if gameObject not in cls.gameObjectDestructionQueue:
            cls.gameObjectDestructionQueue.put(gameObject)

    @classmethod
    def update(cls):
        from gameengine.core.GameObject import GameObject

        World._removeGameObjects()
        World._addGameObjects()

        GameObject._removeScripts()
        GameObject._addScripts()

        GameObject._removeComponents()
        GameObject._addComponents()

        for gameObject in cls.gameObjects:
            for script in gameObject.scripts:
                script.onPreUpdate()

        PhysicsManager().onUpdate()
        CollisionManager().onUpdate()
        InputManager().onUpdate()

        for gameObject in cls.gameObjects:
            for script in gameObject.scripts:
                script.onUpdate()

        updateTimers()
        updateInterpolations()

    @classmethod
    def draw(cls):
        if cls.display == None:
            print("Pygame display not set")
            cls.shutdown()

        # Clear display
        cls.display.fill((0, 0, 0))

        # Draw
        CameraManager().draw()

        # Update screen
        pygame.display.update()

    @classmethod
    def find(cls, name):
        for gameObject in cls.gameObjects:
            if gameObject.name == name:
                return gameObject
        return None

    @classmethod
    def findGameObjectsWithTag(cls, tag):
        list = []
        for gameObject in cls.gameObjects:
            if tag in gameObject.tags:
                list.append(gameObject)
        return list

    @classmethod
    def shutdown(cls):
        pygame.quit()
        sys.exit()

    @classmethod
    def toString(cls):
        string = ""
        for gameObject in cls.gameObjects:
            string += gameObject.toString()
        return string