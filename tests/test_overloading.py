from __future__ import annotations

import builtins
import itertools

import pytest

from pyoverload.overloading import (
    DictionaryFunctionDispatcher,
    OverloadMeta,
    OverloadSelector,
    overload,
)


@pytest.fixture
def loaded_overload_selector(int_func):
    return OverloadSelector(lambda: int_func)


@pytest.fixture
def overloaded_class(int_func, str_func):
    class TestClass(metaclass=OverloadMeta):
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
def complex_type_func():
    def f3(self, x: dict[int, list[tuple]]):
        return "complex"

    return f3


@pytest.fixture
def dispatcher():
    return DictionaryFunctionDispatcher()


@pytest.fixture
def dispatcher_container(dispatcher, int_func, str_func, complex_type_func):
    dispatcher.register_function(int_func)
    dispatcher.register_function(str_func)
    dispatcher.register_function(complex_type_func)

    class DispatcherContainer:
        method_dispatcher = dispatcher

    return DispatcherContainer


@pytest.fixture
def unique_type_instances():
    builtin_types = [t for t in builtins.__dict__.values() if isinstance(t, type)]
    instances = []
    for t in builtin_types:
        try:
            instances.append(t())
        except (TypeError, RuntimeError):
            pass

    return instances


def test_function_marked_as_overload():
    @overload
    def f():
        pass

    assert f.__overload__


def test_overload_selector(loaded_overload_selector, int_func):
    assert loaded_overload_selector()(1, 2) == int_func(1, 2)


def test_overload_metaclass(overloaded_class):
    assert isinstance(overloaded_class.foo, OverloadSelector)


def test_dispatcher_function_registration(
    dispatcher, int_func, str_func, complex_type_func
):
    dispatcher.register_function(int_func)
    dispatcher.register_function(str_func)
    dispatcher.register_function(complex_type_func)
    assert dispatcher.functions.get(("int",)) == int_func
    assert dispatcher.functions.get(("str",)) == str_func
    assert dispatcher.functions.get(("dict[int, list[tuple]]",)) == complex_type_func


def test_function_dispatching(dispatcher_container):
    assert dispatcher_container.method_dispatcher(1) == "int"
    assert dispatcher_container.method_dispatcher("str") == "str"


@pytest.mark.parametrize(
    "structure, expected_output",
    [
        # Test empty structures
        (list(), "list"),
        (set(), "set"),
        (dict(), "dict"),
        (tuple(), "tuple"),
        # Test populated structures
        ({"key": 42}, "dict[str, int]"),
        ([1, "two"], "list[int]"),
        (set(["a", "b"]), "set[str]"),
        (tuple([13.37, "a", "b"]), "tuple[float]"),
        # Test containers with nested structures
        ({"key": [1, 2]}, "dict[str, list[int]]"),
        ({"key": {"nested_key": "value"}}, "dict[str, dict[str, str]]"),
        # Test different data types
        (42, "int"),
        (3.14, "float"),
        ("Hello, World!", "str"),
        # Test None
        (None, "NoneType"),
        # Test a mix of complex structures
        (
            {"a": [({int: {}},)]},
            "dict[str, list[tuple[dict[type, dict]]]]",
        ),
    ],
)
def test_signature_build_edge_cases(dispatcher, structure, expected_output):
    assert dispatcher.build_signature(structure) == (expected_output,)


def test_signature_build(dispatcher, unique_type_instances):
    for combination in itertools.combinations(unique_type_instances, 4):
        assert dispatcher.build_signature(*combination)


def test_function_dispatching_unsupported_argument(dispatcher_container):
    with pytest.raises(NotImplementedError):
        dispatcher_container.method_dispatcher(True)


@pytest.mark.xfail
def test_method_overloading_inheritance():
    class Parent(metaclass=OverloadMeta):
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


def test_dispatch_lookup_performance(benchmark, dispatcher_container):
    def benchmark_function_dispatching():
        for _ in range(100000):
            dispatcher_container.method_dispatcher(1)

    benchmark(benchmark_function_dispatching)


def test_normal_lookup_performance(benchmark, int_func):
    class foo:
        bar = int_func

    obj = foo()

    def benchmark_function_dispatching():
        for _ in range(100000):
            obj.bar(1)

    benchmark(benchmark_function_dispatching)
