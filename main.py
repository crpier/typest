from typing import Callable, NewType
from pytest import fixture, FixtureRequest
from _pytest.fixtures import FixtureFunctionMarker, FixtureDef

new_fixtures: list[Callable] = []


@fixture(autouse=True)
def fixture_generator(request: FixtureRequest):
    request.fixturenames.extend([fixture.__name__ for fixture in new_fixtures])
    fixturedef = FixtureDef(
        fixturemanager=request._fixturemanager,
        baseid="",
        argname="User",
        func=User,
        scope="function",
        params=None,
        unittest=False,
        ids=None,
    )
    request._fixturemanager._arg2fixturedefs["User"] = [fixturedef]


def new_fixture(wrapped_func: Callable):
    marker = FixtureFunctionMarker(
        scope="function", params=None, name=wrapped_func.__name__
    )
    new_fixture = marker(wrapped_func)
    wrapped_func = new_fixture
    new_fixtures.append(wrapped_func)

    new_class = type(wrapped_func.__name__, (), {"__call__": wrapped_func})
    return new_class


def new_test(wrapped_func: Callable):
    def dynamically_generated_func(User: int):
        return wrapped_func(User)

    return dynamically_generated_func


@new_fixture
def User() -> int:
    return 32


def pula(kek: int):
    print(kek)


@new_test
def test_user(user: User):
    assert True
