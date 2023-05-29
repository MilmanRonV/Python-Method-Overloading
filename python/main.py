from typing import Any

# from __future__ import annotations --- this changes type annotations from type to str, breaking the function dispatcher


def overload(func):
    func.__overload__ = True
    return func


class FunctionDispatcher:
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
        print(func.__annotations__.values())
        signature = tuple([x for x in func.__annotations__.values()])
        self.functions[signature] = func

    def build_signature(self, *args, **kwargs):
        params = []
        for arg in args:
            params.append(type(arg))
        for _, value in kwargs.items():
            params.append(type(value))

        return tuple(params)


class MethodOverloadDict(dict):
    def __setitem__(self, __key: Any, __value: Any) -> None:
        overloaded = getattr(__value, "__overload__", False)

        if overloaded:
            if not self.get(__key):
                self.__setitem__(__key, FunctionDispatcher())

            self.get(__key).register_function(__value)
        else:
            super().__setitem__(__key, __value)


class Overload(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return MethodOverloadDict()

    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)


class Foo(metaclass=Overload):
    @overload
    def bar(self, a: int):
        print("int!")

    @overload
    def bar(self, a: str):
        print("str!")


f = Foo()
print(f.bar)

f.bar(1)
f.bar("")
