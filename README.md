# Python Method Overloading

This Python script demonstrates method overloading using a metaclass and a descriptor. It dispatches functions based on the types/type hints of their arguments.

The script defines the following classes:

- `Overload`: A metaclass that provides a `MethodOverloadDict` to `__new__` instead of a regular namespace.
- `MethodOverloadDict`: A dictionary subclass that handles method registration using `FunctionDispatcher`.
- `FunctionDispatcher`: An abstract base class that defines the interface for a function dispatcher.
- `DictionaryFunctionDispatcher`: A descriptor that dispatches a callable responsible for selecting the right function based on registered functions and the provided arguments' types.

The script also includes an `overload` decorator that marks methods as overloads.

## Usage

You can find an example usage below.

```python
class Foo(metaclass=Overload):
    @overload
    def bar(self, x: int):
        print(f"Bar function with integer argument: {x}")

    @overload
    def bar(self, s: str):
        print(f"Bar function with string argument: {s}")


f = Foo()
f.bar(42)  # Output: Bar function with integer argument: 42
f.bar("Hello")  # Output: Bar function with string argument: Hello
```

In this example, the `Foo` class demonstrates method overloading with the `bar` method. The `bar` method can be called with either an integer or a string argument. Depending on the argument type, the corresponding overloaded version of the function will be dispatched.

Note: Similar functionality can be achieved using `functools.singledispatchmethod`, but this implementation offers a more precise dispatching mechanism.

Enjoy exploring function overloading with this script!

Happy Coding!
