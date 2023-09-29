import sys

if "__future__" not in sys.modules:
    import warnings

    warnings.warn("This package requires 'from __future__ import annotations' to work properly")

__all__ = [
    "DictionaryFunctionDispatcher",
    "FunctionDispatcher",
    "MethodOverloadDict",
    "OverloadMeta",
    "OverloadSelector",
    "overload",
]

from .overloading import (
    DictionaryFunctionDispatcher,
    FunctionDispatcher,
    MethodOverloadDict,
    OverloadMeta,
    OverloadSelector,
    overload,
)
