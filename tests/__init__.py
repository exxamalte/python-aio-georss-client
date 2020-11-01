"""Tests for georss-client library."""
from typing import Dict, Optional, Tuple

from aio_georss_client.feed import GeoRssFeed
from aio_georss_client.feed_entry import FeedEntry
from aio_georss_client.xml_parser.feed_item import FeedItem

MOCK_HOME_COORDINATES = (0.0, 0.0)
MOCK_FEED_ITEM = FeedItem({})


class MockFeedEntry(FeedEntry):
    """Generic feed entry."""

    @property
    def attribution(self) -> Optional[str]:
        return None


class MockGeoRssFeed(GeoRssFeed[MockFeedEntry]):

    def _new_entry(self,
                   home_coordinates: Tuple[float, float],
                   rss_entry: FeedItem,
                   global_data: Dict) -> MockFeedEntry:
        """Generate a new entry."""
        return MockFeedEntry(home_coordinates, rss_entry)


class MockSimpleFeedEntry(FeedEntry):

    @property
    def attribution(self) -> Optional[str]:
        return "mock attribution"

    @property
    def title(self) -> Optional[str]:
        return "mock title"

    @property
    def external_id(self) -> Optional[str]:
        return "mock id"
