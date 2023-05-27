import inspect
from collections import defaultdict
from typing import Any


def overload(func):
    func.__overload__ = True
    return func


class FunctionDispatcher:
    def __init__(self) -> None:
        self.functions = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        desired_sig = self.build_signature(*args, **kwds)
        func = self.functions.get(desired_sig)
        if func is not None:
            return func(*args, **kwds)
        else:
            raise NotImplementedError("Function not found")

    def register_function(self, func):
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
                self.get(__key).register_function(__value)
            return

        super().__setitem__(__key, __value)


class Overload(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return MethodOverloadDict()

    def __new__(cls, name, bases, attrs):
        print(attrs)
        return super().__new__(cls, name, bases, attrs)


class Foo(metaclass=Overload):
    @overload
    def bar(a: int):
        print("int!")

    @overload
    def bar(a: str):
        print("str!")


f = Foo()

f.bar("")
f.bar(1)
