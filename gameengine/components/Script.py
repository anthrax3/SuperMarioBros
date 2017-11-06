from abc import ABC

from gameengine.core.Events import Events
from gameengine.core.Object import Object


class Script(Object, Events, ABC):
    """Similares aux scripts en Unity, on crée un script et on l'attache à un GameObject pour gestionner les evenements
    produits pas les composants."""

    def __init__(self):
        super().__init__()
        self.gameObject = None

        self._order = 0

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value
        self.gameObject.scripts.sort(key=lambda script: script.order)

    def toString(self):
        return __class__

    def destroy(self):
        self.gameObject.removeScript(self)
