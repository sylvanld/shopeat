import pytest

from shopeat.core.config import Config


def test_get_non_existing_config_with_default_value():
    value = Config.get("example.key", default="something")
    assert value == "something"

    value = Config.get("example.key", default=None)
    assert value is None


def test_get_non_existing_config_without_default_value():
    with pytest.raises(ValueError):
        Config.get("example.key")
