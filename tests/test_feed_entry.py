"""Test for the generic georss feed entry."""
import datetime
from unittest import mock

from aio_georss_client.xml_parser.geometry import Point, BoundingBox, Polygon
from . import MockFeedEntry, MockSimpleFeedEntry, MOCK_HOME_COORDINATES, MockFeedItem


def test_simple_feed_entry():
    """Test feed entry behaviour."""
    feed_entry = MockSimpleFeedEntry(None, None)
    assert repr(feed_entry) == "<MockSimpleFeedEntry(id=None)>"
    assert feed_entry.geometries is None
    assert feed_entry.coordinates is None
    assert feed_entry.title is None
    assert feed_entry.external_id is None
    assert feed_entry.attribution == "mock attribution"
    assert feed_entry.category is None
    assert feed_entry.description is None
    assert feed_entry.published is None
    assert feed_entry.updated is None
    assert (
        feed_entry._search_in_external_id(r"External ID (?P<custom_attribute>.+)$")
        is None
    )
    assert feed_entry._search_in_title(r"Title (?P<custom_attribute>.+)$") is None
    assert (
        feed_entry._search_in_description(r"Description (?P<custom_attribute>.+)$")
        is None
    )
    # Test _string2boolean
    assert not feed_entry._string2boolean("False")
    assert not feed_entry._string2boolean("no")
    assert feed_entry._string2boolean("True")
    assert feed_entry._string2boolean("yes")


def test_feed_entry_features():
    """Test feed entry filtering by feature."""
    point = Point(0.0, 0.0)
    polygon = Polygon([point, point])
    bounding_box = BoundingBox(point, point)
    feed_item = MockFeedItem(
        None, [point, polygon, point, polygon, polygon, bounding_box]
    )
    # 1. Include all
    feed_entry = MockSimpleFeedEntry(None, feed_item, [Point, Polygon, BoundingBox])
    assert len(feed_entry.geometries) == 6
    # 2. Exclude points
    feed_entry = MockSimpleFeedEntry(None, feed_item, [Polygon, BoundingBox])
    assert len(feed_entry.geometries) == 4
    # 3. Exclude polygons
    feed_entry = MockSimpleFeedEntry(None, feed_item, [Point, BoundingBox])
    assert len(feed_entry.geometries) == 3
    # 4. Exclude bounding boxes
    feed_entry = MockSimpleFeedEntry(None, feed_item, [Point, Polygon])
    assert len(feed_entry.geometries) == 5
    # 5. Exclude all
    feed_entry = MockSimpleFeedEntry(None, feed_item, [])
    assert len(feed_entry.geometries) == 0


def test_feed_entry_search_in_attributes():
    """Test feed entry behaviour."""
    rss_entry = mock.MagicMock()
    type(rss_entry).guid = mock.PropertyMock(return_value="Test 123")
    type(rss_entry).title = mock.PropertyMock(return_value="Title 123")
    type(rss_entry).description = mock.PropertyMock(return_value="Description 123")
    type(rss_entry).category = mock.PropertyMock(
        return_value=["Category 1", "Category 2"]
    )
    updated = datetime.datetime(2019, 4, 1, 8, 30, tzinfo=datetime.timezone.utc)
    type(rss_entry).updated_date = mock.PropertyMock(return_value=updated)

    feed_entry = MockFeedEntry(MOCK_HOME_COORDINATES, rss_entry)
    assert repr(feed_entry) == "<MockFeedEntry(id=Test 123)>"

    assert feed_entry._search_in_external_id(r"Test (?P<custom_attribute>.+)$") == "123"
    assert feed_entry._search_in_title(r"Title (?P<custom_attribute>.+)$") == "123"
    assert (
        feed_entry._search_in_description(r"Description (?P<custom_attribute>.+)$")
        == "123"
    )
    assert feed_entry.category == "Category 1"
    assert feed_entry.description == "Description 123"
    assert feed_entry.updated == updated
