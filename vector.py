import math


class vector:
    """класс для работы с набором координат"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __truediv__(self, n):
        #деление /
        new_vect = self.copy()
        if isinstance(n, (int, float)):
            new_vect.x /= n
            new_vect.y /= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return new_vect

    def __itruediv__(self, n):
        if isinstance(n, (int, float)):
            self.x /= n
            self.y /= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return self

    def __floordiv__(self, n):
        #целочисленное деление x//y
        new_vect = self.copy()
        if isinstance(n, (int, float)):
            new_vect.x //= n
            new_vect.y //= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return new_vect

    def __ifloordiv__(self, n):
        if isinstance(n, (int, float)):
            self.x //= n
            self.y //= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return self

    def __add__(self, v):
        #+
        new_vect = self.copy()
        if isinstance(v, vector):
            new_vect.x += v.x
            new_vect.y += v.y
        else:
            raise TypeError(str(type(v)) + " : not a vector")
        return new_vect

    def __iadd__(self, v):
        if isinstance(v, vector):
            self.x += v.x
            self.y += v.y
        else:
            raise TypeError(str(type(v)) + " : not a vector")
        return self

    def __sub__(self, v):
        #-
        new_vect = self.copy()
        if isinstance(v, vector):
            new_vect.x -= v.x
            new_vect.y -= v.y
        else:
            raise TypeError(str(type(v)) + " : not a vector")
        return new_vect

    def __isub__(self, v):
        if isinstance(v, vector):
            self.x -= v.x
            self.y -= v.y
        else:
            raise TypeError(str(type(v)) + " : not a vector")
        return self

    def __mul__(self, n):
        #*
        new_vect = self.copy()
        if isinstance(n, (int, float)):
            new_vect.x *= n
            new_vect.y *= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return new_vect

    def __imul__(self, n):
        if isinstance(n, (int, float)):
            self.x *= n
            self.y *= n
        else:
            raise TypeError(str(type(n)) + " : not a number")
        return self

    def __eq__(self, v):
        #эквивалент
        precision = 10 ** 9
        if isinstance(v, vector):
            res = (int(self.x * precision) == int(v.x * precision)
                   and int(self.y * precision) == int(v.y * precision))
        else:
            raise TypeError(str(type(v)) + " : not a vector")
        return res

    def copy(self):
        new_vect = vector(self.x, self.y)
        return new_vect

    def toint(self):
        new_vect = self.copy()
        new_vect.x = int(new_vect.x)
        new_vect.y = int(new_vect.y)
        return new_vect

    def totuple(self):
        vect_tuple = (self.x, self.y)
        return vect_tuple

    def normalize(self):
        sum_coords = (self.x ** 2 + self.y ** 2) ** 0.5
        if sum_coords == 0:
            new_vect = vector(0, 0)
        else:
            new_vect = self / sum_coords
        return new_vect

    @classmethod
    def distant(cls, v1, v2):
        """Квадрат расстояния
        """
        dist = (v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2
        return dist

    @classmethod
    def dist(cls, v1, v2):
        dist = cls.distant(v1, v2) ** 0.5
        return dist

    def sq_norm(self):
        """Квадрат нормы"""
        if self.x == 0 and self.y == 0:
            length = 0
        else:
            length = vector.distant(self, vector(0, 0))
        return length

    def length(self):
        if self.x == 0 and self.y == 0:
            length = 0
        else:
            length = self.sq_norm() ** 0.5
        return length

    @staticmethod
    def scalar(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def get_angle(v1, v2):
        v1 = v1.copy().normalize()
        v2 = v2.copy().normalize()
        angle = vector.scalar(v1, v2) / (v1.length() * v2.length())
        if angle > 1:
            angle = 1
        angle = math.acos(angle)
        angle = math.degrees(angle)
        return angle
