from inspect import signature
from typing import Callable
from pytest import fixture, FixtureRequest
from _pytest.fixtures import FixtureFunctionMarker, FixtureDef


new_fixtures = []


@fixture(autouse=True)
def fixture_generator(request: FixtureRequest):
    request.fixturenames.extend(new_fixtures)
    fixturedef = FixtureDef(
        fixturemanager=request._fixturemanager,
        baseid="",
        argname="user",
        func=user,
        scope="function",
        params=None,
        unittest=False,
        ids=None,
    )
    request._fixturemanager._arg2fixturedefs["user"] = [fixturedef]
    print("\n\nfixture_generator")
    print(request.fixturenames)


def new_fixture(wrapped_func: Callable):
    marker = FixtureFunctionMarker(scope="function", params=None, name="user")
    new_fixture = marker(wrapped_func)
    wrapped_func = new_fixture
    new_fixtures.append(wrapped_func.__name__)
    sig = signature(wrapped_func)
    print(sig.return_annotation)
    print("\n\nnew_fixture")

    return wrapped_func


@new_fixture
def user() -> int:
    print("\n\nuser")
    return 32


def test_user(user):
    assert True
