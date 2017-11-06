from gameengine.util.Vector2 import Vector2

a = Vector2(5, 6)
def recalcA(sender, old, new):
    a.set(new - Vector2(1, 1))
    print("new a", a)


b = Vector2(5, 6)
b.hasChanged += recalcA

def recalcB(senfer, old, new):
    b.set(new + Vector2(1, 1))
    print("new b", b)

a.hasChanged += recalcB

if __name__ == "__main__":
    a.set(5, 5)

    a.set(122, 2)

    b.set(45, 0)

    print(a)
    print(b)
