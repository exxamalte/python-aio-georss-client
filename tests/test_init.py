"""Tests for general setup."""
from aio_georss_client import __version__


def test_version():
    """Test for version tag."""
    assert __version__ is not None
