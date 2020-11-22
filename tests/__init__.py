"""Tests for georss-client library."""
from typing import Dict, List, Optional, Tuple, Type

from aio_georss_client.feed import GeoRssFeed
from aio_georss_client.feed_entry import DEFAULT_FEATURES, FeedEntry
from aio_georss_client.xml_parser.feed_item import FeedItem
from aio_georss_client.xml_parser.geometry import BoundingBox, Geometry, Point

MOCK_HOME_COORDINATES = (0.0, 0.0)


class MockFeedEntry(FeedEntry):
    """Generic feed entry."""

    @property
    def attribution(self) -> Optional[str]:
        return None


class MockGeoRssFeed(GeoRssFeed[MockFeedEntry]):
    def _new_entry(
        self,
        home_coordinates: Tuple[float, float],
        rss_entry: FeedItem,
        global_data: Dict,
    ) -> MockFeedEntry:
        """Generate a new entry."""
        return MockFeedEntry(home_coordinates, rss_entry)


class MockSimpleFeedEntry(FeedEntry):
    def __init__(
        self,
        home_coordinates: Tuple[float, float],
        rss_entry: FeedItem,
        features: List[Type[Geometry]] = DEFAULT_FEATURES,
    ):
        super().__init__(home_coordinates, rss_entry)
        self._features = features

    @property
    def features(self) -> List[Type[Geometry]]:
        return self._features

    @property
    def attribution(self) -> Optional[str]:
        return "mock attribution"


class MockFeedItem(FeedItem):
    def __init__(self, source, geometries):
        super().__init__(source)
        self._geometries = geometries

    @property
    def geometries(self) -> Optional[List[Geometry]]:
        return self._geometries
