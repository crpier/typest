from typing import Annotated

import pytest
from main import cringe_fixture, cringe_check, check

A = Annotated

# This seems like a concise way to go about it, but it's weird because
# - the fixture is named like class to make the annotation look not surprising
#   - the reverse would be to make the annotation look surprising, in order to make the fixture look normal
# - the "user" param's type is misleading: it's not `UserID`, it's `int`


@cringe_fixture
def UserID() -> int:
    return 32


@cringe_check
def test_user(user: UserID):
    assert user == 32


# That seems to me like a nicer way to go about it, but it's more verbose


@pytest.fixture
def new_sku() -> str:
    return "42"


@check
def test_sku(sku: A[str, new_sku]):
    assert sku == "42"
