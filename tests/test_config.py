import pytest
from shopeat.config import Config


def test_get_non_existing_with_default_value():
    value = Config.get("example.key", default="something")
    assert value == "something"

    value = Config.get("example.key", default=None)
    assert value is None


def test_get_non_existing_in_strict_mode():
    with pytest.raises(ValueError):
        Config.get("example.key")
