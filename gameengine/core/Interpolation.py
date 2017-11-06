interpolations = []


class Linear:
    def __init__(self):
        self.interpolator = CubicBezier(0, 0, 1, 1)

    def ease(self, t):
        return self.interpolator.ease(t)


class Interpolation:
    """Gère les interpolations des valeurs.
    Permet d'utiliser une fonction de type cubic bezier (http://cubic-bezier.com) pour intérpoler les valeurs."""

    def __init__(self, start, stop, milliseconds: int, callback, method=Linear, args=()):
        self.startValue = type(start)(start)  # Use the copy constructor, workaround for copy.copy()
        self.stopValue = type(stop)(stop)

        self.milliseconds = milliseconds
        self.method = method
        self.args = args
        self.callback = callback

        self.generator = self.Generator()
        self.paused = False

    def Generator(self):
        interpolator = self.method(*self.args)

        seconds = self.milliseconds / 1000.0
        diff = self.stopValue - self.startValue
        inc = 1.0 / 60  # pygame.time.Clock.get_fps()
        progression = self.startValue * 0
        current_second = inc

        while current_second < seconds:
            percent = 1 - ((seconds - current_second)) / seconds

            previous_step = progression
            progression = diff * interpolator.ease(percent)

            yield (self.startValue + progression, progression - previous_step)
            current_second += inc

        yield (self.stopValue, self.stopValue - (self.startValue + progression))

    def start(self):
        self.resume()
        if self not in interpolations:
            interpolations.append(self)
        return self

    def stop(self):
        if self in interpolations:
            interpolations.remove(self)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def interpolate(self):
        if not self.paused:
            try:
                self.callback(*next(self.generator))
            except StopIteration:
                interpolations.remove(self)


def updateInterpolations():
    for interpolation in interpolations:
        interpolation.interpolate()




# Predefined Cubic Bezier classes
class Ease:
    def __init__(self):
        self.interpolator = CubicBezier(.25, .1, .25, 1)

    def ease(self, t):
        return self.interpolator.ease(t)


class EaseIn:
    def __init__(self):
        self.interpolator = CubicBezier(.42, 0, 1, 1)

    def ease(self, t):
        return self.interpolator.ease(t)


class EaseOut:
    def __init__(self):
        self.interpolator = CubicBezier(0, 0, .58, 1)

    def ease(self, t):
        return self.interpolator.ease(t)


class EaseInOut:
    def __init__(self):
        self.interpolator = CubicBezier(.42, 0, .58, 1)

    def ease(self, t):
        return self.interpolator.ease(t)


# Un grand merci pour https://github.com/gre/bezier-easing/blob/master/src/index.js
# Librairie js qui implémente Cubic Bezier, souvent utilisé pour créer des animations en CSS
class CubicBezier:
    NEWTON_ITERATIONS = 4
    NEWTON_MIN_SLOPE = 0.001
    SUBDIVISION_PRECISION = 0.0000001
    SUBDIVISION_MAX_ITERATIONS = 10

    kSplineTableSize = 11
    kSampleStepSize = 1.0 / (kSplineTableSize - 1.0)

    def __init__(self, x1, y1, x2, y2):
        if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
            raise RuntimeError("bezier x values must be in [0, 1] range")

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.sampleValues = []
        if self.x1 != self.y1 or self.x2 != self.y2:
            for i in range(self.kSplineTableSize):
                self.sampleValues.append(self.calcBezier(i * self.kSampleStepSize, self.x1, self.x2))

    def ease(self, t):
        if self.x1 == self.y1 and self.x2 == self.y2:
            return t

        if t == 0:
            return 0
        if t == 1:
            return 1

        return self.calcBezier(self.getTForX(t), self.y1, self.y2)

    def getTForX(self, aX):
        intervalStart = 0.0
        currentSample = 1
        lastSample = self.kSplineTableSize - 1

        while currentSample != lastSample and self.sampleValues[currentSample] <= aX:
            intervalStart += self.kSampleStepSize
            currentSample += 1
        currentSample -= 1

        dist = (aX - self.sampleValues[currentSample]) / (
        self.sampleValues[currentSample + 1] - self.sampleValues[currentSample])
        guessForT = intervalStart + dist * self.kSampleStepSize

        initialSlope = self.getSlope(guessForT, self.x1, self.x2)
        if initialSlope >= self.NEWTON_MIN_SLOPE:
            return self.newtonRaphsonIterate(aX, guessForT, self.x1, self.x2)

        elif initialSlope == 0:
            return guessForT

        else:
            return self.binarySubdivide(aX, intervalStart, intervalStart + self.kSampleStepSize, self.x1, self.x2)

    @classmethod
    def A(cls, aA1, aA2):
        return 1.0 - 3.0 * aA2 + 3.0 * aA1

    @classmethod
    def B(cls, aA1, aA2):
        return 3.0 * aA2 - 6.0 * aA1

    @classmethod
    def C(cls, aA1):
        return 3.0 * aA1

    @classmethod
    def calcBezier(cls, aT, aA1, aA2):
        return ((cls.A(aA1, aA2) * aT + cls.B(aA1, aA2)) * aT + cls.C(aA1)) * aT

    @classmethod
    def getSlope(cls, aT, aA1, aA2):
        return 3.0 * cls.A(aA1, aA2) * aT * aT + 2.0 * cls.B(aA1, aA2) * aT + cls.C(aA1)

    @classmethod
    def binarySubdivide(cls, aX, aA, aB, mX1, mX2):
        currentX = 0
        currentT = 0
        i = 0

        firstTime = True

        while firstTime or (abs(currentX) > cls.SUBDIVISION_PRECISION and i < cls.SUBDIVISION_MAX_ITERATIONS):
            currentT = aA + (aB - aA) / 2.0
            currentX = cls.calcBezier(currentT, mX1, mX2) - aX
            if currentX > 0:
                aB = currentT
            else:
                aA = currentT

            i += 1
            firstTime = False

        return currentT

    @classmethod
    def newtonRaphsonIterate(cls, aX, aGuessT, mX1, mX2):
        for i in range(cls.NEWTON_ITERATIONS):
            currentSlope = cls.getSlope(aGuessT, mX1, mX2)
            if currentSlope == 0:
                return aGuessT

            currentX = cls.calcBezier(aGuessT, mX1, mX2) - aX
            aGuessT -= currentX / currentSlope

        return aGuessT
