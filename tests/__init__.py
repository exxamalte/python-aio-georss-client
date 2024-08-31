"""Tests for georss-client library."""

from __future__ import annotations

from typing import Final

from aio_georss_client.feed import GeoRssFeed
from aio_georss_client.feed_entry import DEFAULT_FEATURES, FeedEntry
from aio_georss_client.xml_parser.feed_item import FeedItem
from aio_georss_client.xml_parser.geometry import Geometry

MOCK_HOME_COORDINATES: Final = (0.0, 0.0)


class MockFeedEntry(FeedEntry):
    """Generic feed entry."""

    @property
    def attribution(self) -> str | None:
        """Return attribution."""
        return None


class MockGeoRssFeed(GeoRssFeed[MockFeedEntry]):
    """Mock GeoRSS feed."""

    def _new_entry(
        self,
        home_coordinates: tuple[float, float],
        rss_entry: FeedItem,
        global_data: dict,
    ) -> MockFeedEntry:
        """Generate a new entry."""
        return MockFeedEntry(home_coordinates, rss_entry)


class MockSimpleFeedEntry(FeedEntry):
    """Mock feed entry."""

    def __init__(
        self,
        home_coordinates: tuple[float, float] | None,
        rss_entry: FeedItem,
        features: list[type[Geometry]] = DEFAULT_FEATURES,
    ):
        """Initialise feed entry."""
        super().__init__(home_coordinates, rss_entry)
        self._features = features

    @property
    def features(self) -> list[type[Geometry]]:
        """Return features."""
        return self._features

    @property
    def attribution(self) -> str | None:
        """Return attribution."""
        return "mock attribution"


class MockFeedItem(FeedItem):
    """Mock feed item."""

    def __init__(self, source: dict | None, geometries: list[Geometry] | None):
        """Initialise feed item."""
        super().__init__(source)
        self._geometries = geometries

    @property
    def geometries(self) -> list[Geometry] | None:
        """Return geometries."""
        return self._geometries
