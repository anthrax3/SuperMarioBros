from abc import ABC


class Events(ABC):
    """Interface avec tous les evenements"""

    def onCreate(self):
        pass

    def onPreUpdate(self):
        pass

    # Collider
    def onCollisionEnter(self, other, side):
        return False

    def onCollisionStay(self, other):
        pass

    def onCollisionExit(self, other, side):
        pass

    # Input
    def onMouseHover(self, pos, rel):
        return True

    def onMouseDown(self, pos, button):
        return True

    def onMouseDrag(self, pos, rel, buttons):
        pass

    def onMouseUp(self, pos, button):
        return True

    def onMouseClicked(self, pos):
        pass

    def onKeyDown(self, key):
        pass

    def onKeyUp(self, key):
        pass


    def onUpdate(self):
        pass

    # SpriteRenderer
    def alterSpriteFrame(self, frame):
        return frame

    # CustomDraw
    def onDraw(self):
        return None


    def onBecameVisible(self):
        pass

    def onBecameInvisible(self):
        pass


    def onMessageReceived(self, keyword, message):
        pass