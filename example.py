from __future__ import annotations

from dataclasses import dataclass

from pyoverload.overloading import OverloadMeta, overload


@dataclass
class Coordinate(metaclass=OverloadMeta):  # pragma: no cover
    """
    An example, has both Coordiante and scalar overload methods.
    Not particularly useful as you can just use a Coordiante with
    equal x and y values instead of a scalar, but a good demonstration.
    """

    x: int
    y: int

    @overload
    def __floordiv__(self, other: Coordinate):
        x = self.x // other.x
        y = self.y // other.y
        return Coordinate(x, y)

    @overload
    def __floordiv__(self, n: int):
        x = self.x // n
        y = self.y // n
        return Coordinate(x, y)

    @overload
    def __mul__(self, other: Coordinate):
        x = int(self.x * other.x)
        y = int(self.y * other.y)
        return Coordinate(x, y)

    @overload
    def __mul__(self, n: int):
        x = int(self.x * n)
        y = int(self.y * n)
        return Coordinate(x, y)

    @overload
    def __add__(self, other: Coordinate):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x, y)

    @overload
    def __add__(self, n: int):
        x = self.x + n
        y = self.y + n
        return Coordinate(x, y)

    @overload
    def __sub__(self, other: Coordinate):
        x = self.x - other.x
        y = self.y - other.y
        return Coordinate(x, y)

    @overload
    def __sub__(self, n: int):
        x = self.x - n
        y = self.y - n
        return Coordinate(x, y)

    @overload
    def __mod__(self, other: Coordinate):
        x = self.x % other.x
        y = self.x % other.y
        return Coordinate(x, y)

    @overload
    def __mod__(self, n: int):
        x = self.x % n
        y = self.x % n
        return Coordinate(x, y)

    @overload
    def __mod__(self, complex: dict[str, list[tuple[int]]]):
        x = self.x % complex["x"][0][0]
        y = self.x % complex["y"][0][0]
        return Coordinate(x, y)


if __name__ == "__main__":  # pragma: no cover
    c = Coordinate(10, 10)
    print(c // 2)
    print(c // Coordinate(2, 2))
    print(c * 2)
    print(c * Coordinate(2, 2))
    print(c + 2)
    print(c + Coordinate(2, 2))
    print(c - 2)
    print(c - Coordinate(2, 2))
    print(c % 2)
    print(c % Coordinate(2, 2))
    print(c % {"x": [(1,)], "y": [(1,)]})
