from __future__ import annotations

from typing import Any

# from __future__ import annotations changes type annotations from
# type to str, breaking the function dispatcher. meaning this won't work in
# specific python versions


"""
An exercise in metaclasses that also turned out to be an exercise in
descriptors :).
Apparently, there is already simillar functionality in functools via
singledispatchmethod. singledispatchmethod uses only the first argument's type
to determine which function should be dispatched, as opposed to the exact
permutation like in my implementation. Apparently, it also implemented in a
similar fashion (utilizing a descriptor returning a function).

P.S. Have fun with your linter :D
"""


def overload(func):
    """
    A decorator that marks a function as an overload.
    (Done in the same manner as abc.abstractmethod)
    """
    func.__overload__ = True
    return func


class FunctionDispatcher:
    """
    A non-data descriptor that dispatches a callable which picks a function
    from registered functions based on argument types
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
    A dictionary, handles registration of functions through FunctionDispatcher.
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
    a metaclass the provides a MethodOverloadDict to __new__
    """

    @classmethod
    def __prepare__(cls, name, bases):
        return MethodOverloadDict()

    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)


class Foo(metaclass=Overload):
    """an example :)"""

    @overload
    def bar(self, a: int):
        print("int!")

    @overload
    def bar(self, a: str):
        print("str!")

    @overload
    def bar(self, a: Foo):
        print("Foo!")


f = Foo()
print(f.bar)

f.bar(1)
f.bar("")
f.bar(Foo())
f.bar(int)
