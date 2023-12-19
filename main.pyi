from typing import Callable, ParamSpec, Type, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

def cringe_fixture(func: Callable[P, T]) -> Type[T]: ...
def cringe_check(func: Callable[..., None]): ...
def check(func: Callable[..., None]): ...