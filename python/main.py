from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# 'from __future__ import annotations' changes type annotations from
# type to str and enables annotating a class within its own decleration.
# removing this import will require altering the signature lookup logic.


"""
An exercise in metaclasses that also turned out to be an exercise in
descriptors :).
Apparently, there is already simillar functionality in functools via
singledispatchmethod. singledispatchmethod uses only the first argument's type
to determine which function should be dispatched, as opposed to the exact
permutation like in my implementation. Apparently, it is also implemented in a
similar fashion, utilizing a descriptor returning a function, but without
using a metaclass.

P.S. Have fun with your linter :D
"""


def overload(func):
    """
    A decorator that marks a function as an overload
    (Done in the same manner as abc.abstractmethod).
    """
    func.__overload__ = True
    return func


class FunctionDispatcher:
    """
    A non-data descriptor that dispatches a callable which picks a function
    from registered functions based on the passed argument types.
    """

    def __init__(self) -> None:
        self.functions = {}

    def __get__(self, obj, type=None):
        def dispatch_function(*args, **kwds):
            desired_sig = self.build_signature(*args, **kwds)
            func = self.functions.get(desired_sig)
            if func is not None:
                return func(obj, *args, **kwds)
            else:
                raise NotImplementedError("Function not found")

        return dispatch_function

    def register_function(self, func):
        signature = tuple([x for x in func.__annotations__.values()])
        self.functions[signature] = func

    def build_signature(self, *args, **kwargs):
        params = []
        for arg in args:
            params.append(type(arg).__name__)
        for _, value in kwargs.items():
            params.append(type(value).__name__)
        return tuple(params)


class MethodOverloadDict(dict):
    """
    A dictionary, handles registration of functions using FunctionDispatcher.
    """

    def __setitem__(self, __key: Any, __value: Any) -> None:
        overloaded = getattr(__value, "__overload__", False)

        if overloaded:
            if not self.get(__key):
                self.__setitem__(__key, FunctionDispatcher())

            self.get(__key).register_function(__value)
        else:
            super().__setitem__(__key, __value)


class Overload(type):
    """
    A metaclass the provides a MethodOverloadDict to __new__ instead of
    a regular dict.
    """

    @classmethod
    def __prepare__(cls, name, bases):
        return MethodOverloadDict()

    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)


@dataclass
class Coordinate(metaclass=Overload):
    """
    An example, adds Coordiante and scalar overload methods.
    Not particularly useful as you can just use a Coordiante with
    equal x and y values instead of a scalar.
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


if __name__ == "__main__":
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
