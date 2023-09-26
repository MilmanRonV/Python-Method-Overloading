from __future__ import annotations

from abc import ABC, abstractmethod
from types import GenericAlias
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


class FunctionDispatcher(ABC):  # pragma: no cover
    """
    An abstract base class that defines the interface for a function
    dispatcher.
    """

    @abstractmethod
    def __get__(self, obj, type=None):
        raise NotImplementedError

    @abstractmethod
    def register_function(self, obj):
        raise NotImplementedError


class OverloadSelector:
    def __init__(self, selector_function) -> None:
        self.selector_function = selector_function

    def __call__(self, *args: Any, **kwds: Any):
        return self.selector_function(*args, **kwds)


class DictionaryFunctionDispatcher(FunctionDispatcher):
    """
    A descriptor that dispatches a callable which selects a function
    from registered functions based on the passed argument types.
    """

    def __init__(self) -> None:
        self.functions = {}

    def __get__(self, instance, type=None):
        return self.get_selector(instance)

    def get_selector(self, instance):
        def selector(*args, **kwds):
            desired_sig = self.build_signature(*args, **kwds)
            selected_func = self.functions.get(desired_sig)
            if selected_func is not None:
                return selected_func(instance, *args, **kwds)
            else:
                raise NotImplementedError("Function not found")

        return OverloadSelector(selector)

    def register_function(self, func):
        signature = tuple(func.__annotations__.values())
        self.functions[signature] = func

    def build_signature(self, *args, **kwargs):
        def get_hint(arg):
            if isinstance(arg, dict) and arg:
                key, val = next(iter(arg.items()))
                hint = eval(get_hint(key)), eval(get_hint(val))
            elif isinstance(arg, (list, tuple, set)) and arg:
                hint = eval(get_hint(next(iter(arg))))
            else:
                return type(arg).__name__
            return str(GenericAlias(type(arg), hint))

        params = [get_hint(arg) for arg in args]
        params.extend(get_hint(value) for value in kwargs.values())

        return tuple(params)


class MethodOverloadDict(dict):
    """
    A dictionary, handles registration of methods using FunctionDispatcher.
    """

    def __setitem__(self, __key: Any, __value: Any) -> None:
        overloaded = getattr(__value, "__overload__", False)

        if overloaded:
            if not self.get(__key):
                self.__setitem__(__key, DictionaryFunctionDispatcher())

            self.get(__key).register_function(__value)
        else:
            super().__setitem__(__key, __value)


class OverloadMeta(type):
    """
    A metaclass that provides a MethodOverloadDict to __new__ instead of
    a regular dict.
    """

    @classmethod
    def __prepare__(cls, name, bases):
        return MethodOverloadDict()

    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)
