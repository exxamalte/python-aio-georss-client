"""Tests for georss-client library."""
from typing import Optional

from aio_georss_client.feed import GeoRssFeed
from aio_georss_client.feed_entry import FeedEntry


class MockGeoRssFeed(GeoRssFeed):

    def _new_entry(self, home_coordinates, rss_entry, global_data):
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


class MockFeedEntry(FeedEntry):
    """Generic feed entry."""

    @property
    def attribution(self) -> Optional[str]:
        return None
