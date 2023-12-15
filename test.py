from main import fixture, some_test


@fixture
def UserId() -> int:
    return 32


@some_test
def test_user(user: UserId):
    assert user == 32
