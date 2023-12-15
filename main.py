from functools import partial
from typing import Callable, ParamSpec, Type, TypeVar
import pytest
from _pytest.fixtures import FixtureDef
from inspect import signature

new_fixtures: list[Callable] = []

P = ParamSpec("P")
T = TypeVar("T")


@pytest.fixture(autouse=True)
def fixture_generator(request: pytest.FixtureRequest):
    for new_fixture in new_fixtures:
        request.fixturenames.append(new_fixture.__name__)
        fixturedef = FixtureDef(
            fixturemanager=request._fixturemanager,
            baseid="",
            argname=new_fixture.__name__,
            func=new_fixture,
            scope="function",
            params=None,
            unittest=False,
            ids=None,
        )
        request._fixturemanager._arg2fixturedefs[fixture.__name__] = [fixturedef]


def fixture(func: Callable[P, T]) -> Type[T]:
    new_fixtures.append(func)
    return func  # type: ignore


def some_test(func: Callable[..., None]):
    sig = signature(func)
    params = [value.annotation() for value in sig.parameters.values()]
    new_func = partial(func, *params)
    return new_func
