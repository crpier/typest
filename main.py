from typing import Callable, NewType
from pytest import fixture, FixtureRequest
from _pytest.fixtures import FixtureFunctionMarker, FixtureDef
from inspect import signature

new_fixtures: list[Callable] = []


@fixture(autouse=True)
def fixture_generator(request: FixtureRequest):
    request.fixturenames.extend([fixture.__name__ for fixture in new_fixtures])
    fixturedef = FixtureDef(
        fixturemanager=request._fixturemanager,
        baseid="",
        argname="UserId",
        func=UserId,
        scope="function",
        params=None,
        unittest=False,
        ids=None,
    )
    request._fixturemanager._arg2fixturedefs["UserId"] = [fixturedef]


def new_fixture(wrapped_func: Callable):
    marker = FixtureFunctionMarker(
        scope="function", params=None, name=wrapped_func.__name__
    )
    wrapped_sig = signature(wrapped_func)
    fixtured_func = marker(wrapped_func)
    new_fixtures.append(wrapped_func)

    new_class = type(fixtured_func.__name__, (), {"__call__": fixtured_func})
    return fixtured_func


def new_test(wrapped_func: Callable):
    def dynamically_generated_func(UserId: int):
        return wrapped_func(UserId)

    return dynamically_generated_func


@new_fixture
def UserId() -> int:
    return 32

@new_test
def test_user(user: UserId):
    assert user == 32
