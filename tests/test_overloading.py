from __future__ import annotations

import builtins
import itertools

import pytest

from overload import DictionaryFunctionDispatcher, Overload, OverloadSelector, overload


@pytest.fixture
def overloaded_class(int_func, str_func):
    class TestClass(metaclass=Overload):
        foo = overload(int_func)
        foo = overload(str_func)

    return TestClass


@pytest.fixture
def int_func():
    def f1(self, x: int):
        return "int"

    return f1


@pytest.fixture
def str_func():
    def f2(self, x: str):
        return "str"

    return f2


@pytest.fixture
def dispatcher():
    return DictionaryFunctionDispatcher()


@pytest.fixture
def dispatcher_container(dispatcher, int_func, str_func):
    dispatcher.register_function(int_func)
    dispatcher.register_function(str_func)

    class DispatcherContainer:
        method_dispatcher = dispatcher

    return DispatcherContainer


@pytest.fixture
def unique_types():
    builtin_types = [t for t in builtins.__dict__.values() if isinstance(t, type)]
    instances = []
    for t in builtin_types:
        try:
            instances.append(t())
        except (TypeError, RuntimeError):
            pass

    return instances


def test_overload_decorator():
    @overload
    def f():
        pass

    assert f.__overload__


def test_overload_metaclass(overloaded_class):
    assert isinstance(overloaded_class.foo, OverloadSelector)


def test_function_registration(dispatcher, int_func, str_func):
    dispatcher.register_function(int_func)
    dispatcher.register_function(str_func)
    assert (
        dispatcher.functions.get(tuple(int_func.__annotations__.values())) == int_func
    )
    assert (
        dispatcher.functions.get(tuple(str_func.__annotations__.values())) == str_func
    )


def test_function_dispatching(dispatcher_container):
    assert dispatcher_container.method_dispatcher(1) == "int"
    assert dispatcher_container.method_dispatcher("str") == "str"


def test_signature_build(dispatcher, unique_types):
    for combination in itertools.combinations(unique_types, 4):
        assert dispatcher.build_signature(*combination)


def test_function_dispatching_unsupported_argument(dispatcher_container):
    with pytest.raises(NotImplementedError):
        dispatcher_container.method_dispatcher(True)


def test_method_overloading_inheritance():
    class Parent(metaclass=Overload):
        @overload
        def foo(self, x: int):
            return "Parent int"

        @overload
        def foo(self, x: str):
            return "Parent str"

    class Child(Parent):
        @overload
        def foo(self, x: float):
            return "Parent str"

    obj = Child()

    assert obj.foo(1.0)
    assert obj.foo("str")
    assert obj.foo(1)


def test_performance(benchmark, dispatcher_container):
    def benchmark_function_dispatching():
        for _ in range(100000):
            dispatcher_container.method_dispatcher(1)

    benchmark(benchmark_function_dispatching)


def test_performance_normal(benchmark, int_func):
    class foo:
        bar = int_func

    obj = foo()

    def benchmark_function_dispatching():
        for _ in range(100000):
            obj.bar(1)

    benchmark(benchmark_function_dispatching)
