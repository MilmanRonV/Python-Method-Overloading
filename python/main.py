import inspect
from collections import defaultdict
from typing import Any

# class Uppercased(type):
#     def __new__(cls, name, bases, attrs):
#         print(cls, name, bases, attrs)
#         uppercased = {a.upper(): b for a, b in attrs.items()}
#         for k, v in uppercased.items():
#             if type(v) == type(lambda x: x):
#                 v.__name__ = v.__name__.upper()
#                 v.__qualname__ = ".".join(
#                     [
#                         *v.__qualname__.split(".")[:-1],
#                         v.__qualname__.split(".")[-1].upper(),
#                     ]
#                 )
#             else:
#                 print(v)
#         return super().__new__(cls, name, bases, uppercased)


# class Foo(metaclass=Uppercased):
#     def bar():
#         pass

# print(Foo().BAR)


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
        for key, value in kwargs.items():
            params.append(type(value))
        # return "(" + ", ".join(params) + ")"
        return tuple(params)


def add(a: int, b: int):
    return a + b


def addk(a: int, b: int, *, kwd: list):
    print("has keyword")
    return a + b


def addf(a: int, b: float):
    return a + b


dispatcher = FunctionDispatcher()
dispatcher.register_function(add)
dispatcher.register_function(addk)
dispatcher.register_function(addf)

print(dispatcher(1, 2))


class MethodOverloadDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # self.overloaded_methods = defaultdict(FunctionDispatcher)

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

    # def __getitem__(self, __key: Any) -> Any:
    #     try:
    #         print(super().__getitem__(__key))
    #     except KeyError:
    #         print((__key))
    #         pass
    #     try:
    #         return super().__getitem__(__key)
    #     except KeyError:
    #         try:
    #             dispatcher = self.overloaded_methods[__key]
    #             print(dispatcher.functions)
    #             return self.overloaded_methods[__key]
    #         except KeyError:
    #             raise KeyError()


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
