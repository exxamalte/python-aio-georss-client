"""Tests for XML parser."""

import datetime
from pyexpat import ExpatError

import pytest

from aio_georss_client.xml_parser import XmlParser
from aio_georss_client.xml_parser.geometry import Point, Polygon
from tests.utils import load_fixture


def test_simple_1():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_simple_1.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None
    assert feed.entries is not None
    assert len(feed.entries) == 1


def test_simple_2():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_simple_2.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None
    assert feed.entries is not None
    assert len(feed.entries) == 1


def test_simple_3():
    """Test parsing XML file with invalid tags."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_simple_3.xml")
    feed = xml_parser.parse(xml)
    assert feed is None


def test_simple_4():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_simple_4.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None
    assert feed.entries is not None
    assert len(feed.entries) == 1
    # Double-check that an integer in the XML is automatically converted to string.
    assert feed.entries[0].title == "1"


def test_simple_5():
    """Test parsing XML file with invalid tags."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_simple_5.xml")
    feed = xml_parser.parse(xml)
    assert feed is None


def test_complex_1():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_complex_1.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None

    assert feed.title == "Feed Title 1"
    assert feed.subtitle == "Feed Subtitle 1"
    assert feed.description == "Feed Description 1"
    assert feed.summary == "Feed Description 1"
    assert feed.content == "Feed Description 1"
    assert feed.link == "Feed Link 1"
    assert feed.published_date == datetime.datetime(
        2018, 12, 9, 8, 30, tzinfo=datetime.timezone.utc
    )
    assert feed.pub_date == datetime.datetime(
        2018, 12, 9, 8, 30, tzinfo=datetime.timezone.utc
    )
    assert feed.updated_date == datetime.datetime(
        2018, 12, 9, 8, 45, tzinfo=datetime.timezone.utc
    )
    assert feed.last_build_date == datetime.datetime(
        2018, 12, 9, 8, 45, tzinfo=datetime.timezone.utc
    )
    assert feed.copyright == "Feed Copyright 1"
    assert feed.rights == "Feed Copyright 1"
    assert feed.generator == "Feed Generator 1"
    assert feed.language == "Feed Language 1"
    assert feed.docs == "http://docs.url/documentation.html"
    assert feed.ttl == 42
    assert feed.author == "Feed Author 1"
    assert feed.contributor == "Feed Author 1"
    assert feed.managing_editor == "Feed Author 1"
    assert feed.category == ["Feed Category 1"]
    assert feed.image is not None
    assert feed.image.title == "Image Title 1"
    assert feed.image.url == "http://image.url/image.png"
    assert feed.image.link == "http://feed.link/feed.rss"
    assert feed.image.description == "Image Description 1"
    assert feed.image.width == 123
    assert feed.image.height == 234
    assert feed.get_additional_attribute("random") == "Feed Random 1"
    assert repr(feed) == "<Feed(Feed Link 1)>"

    assert feed.entries is not None
    assert len(feed.entries) == 6

    feed_entry = feed.entries[0]
    assert feed_entry.title == "Title 1"
    assert feed_entry.description == "Description 1"
    assert feed_entry.link == "Link 1"
    assert feed_entry.published_date == datetime.datetime(
        2018, 12, 9, 7, 30, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.updated_date == datetime.datetime(
        2018, 12, 9, 7, 45, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.guid == "GUID 1"
    assert feed_entry.id == "GUID 1"
    assert feed_entry.source == "Source 1"
    assert feed_entry.category == ["Category 1"]
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Point)
    assert geometries[0].latitude == -37.4567
    assert geometries[0].longitude == 149.3456
    assert feed_entry.get_additional_attribute("random") == "Random 1"
    assert repr(feed_entry) == "<FeedItem(GUID 1)>"

    feed_entry = feed.entries[1]
    assert feed_entry.title == "Title 2"
    assert feed_entry.description == "Description 2"
    assert feed_entry.link == "Link 2"
    assert feed_entry.published_date == datetime.datetime(
        2018, 12, 9, 7, 35, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.updated_date == datetime.datetime(
        2018, 12, 9, 7, 50, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.guid == "GUID 2"
    assert feed_entry.category == ["Category 2"]
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Point)
    assert geometries[0].latitude == -37.5678
    assert geometries[0].longitude == 149.4567

    feed_entry = feed.entries[2]
    assert feed_entry.title == "Title 3"
    assert feed_entry.description == "Description 3"
    assert feed_entry.published_date == datetime.datetime(
        2018, 12, 9, 7, 40, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.updated_date == datetime.datetime(
        2018, 12, 9, 7, 55, tzinfo=datetime.timezone.utc
    )
    assert feed_entry.guid == "GUID 3"
    assert feed_entry.category == ["Category 3A", "Category 3B", "Category 3C"]
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Point)
    assert geometries[0].latitude == -37.6789
    assert geometries[0].longitude == 149.5678

    feed_entry = feed.entries[3]
    assert feed_entry.title == "Title 4"
    assert feed_entry.description == "Description 4"
    assert feed_entry.author == "Author 4"
    assert feed_entry.contributor == "Author 4"
    assert feed_entry.category == ["Category 4A", "Category 4B"]
    assert feed_entry.published_date == datetime.datetime(
        2018,
        9,
        30,
        21,
        36,
        48,
        tzinfo=datetime.timezone(datetime.timedelta(hours=10), "AEST"),
    )
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Point)
    assert geometries[0].latitude == -37.789
    assert geometries[0].longitude == 149.6789

    feed_entry = feed.entries[4]
    assert feed_entry.title == "Title 5"
    assert feed_entry.description == "Description 5"
    assert feed_entry.published_date == datetime.datetime(
        2018,
        9,
        20,
        18,
        1,
        55,
        tzinfo=datetime.timezone(datetime.timedelta(hours=2), "CEST"),
    )
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Polygon)
    assert geometries[0].centroid.latitude == -30.32
    assert geometries[0].centroid.longitude == 150.32

    feed_entry = feed.entries[5]
    assert feed_entry.title == "Title 6"
    assert feed_entry.description == "Description 6"
    assert feed_entry.published_date == datetime.datetime(
        2018,
        10,
        7,
        19,
        52,
        tzinfo=datetime.timezone(datetime.timedelta(hours=-2)),
    )
    geometries = feed_entry.geometries
    assert len(geometries) == 1
    assert isinstance(geometries[0], Polygon)
    assert geometries[0].centroid.latitude == -30.32
    assert geometries[0].centroid.longitude == 150.32


def test_complex_2():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_complex_2.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None

    assert feed.title == "Feed Title 1"
    assert feed.subtitle == "Feed Subtitle 1"
    assert feed.ttl == "INVALID"
    assert feed.author == "Author 1"
    assert feed.last_build_date == datetime.datetime(
        2018, 12, 9, 9, 0, tzinfo=datetime.timezone.utc
    )
    assert feed.updated_date == datetime.datetime(
        2018, 12, 9, 9, 0, tzinfo=datetime.timezone.utc
    )
    assert feed.copyright == "Feed Rights 1"
    assert feed.rights == "Feed Rights 1"
    assert feed.generator == "Feed Generator 1"
    assert feed.image is not None
    assert feed.image.title == "Image Title 1"
    assert feed.image.url == "http://image.url/image.png"
    assert feed.image.link == "http://feed.link/feed.rss"
    assert feed.image.description is None
    assert feed.image.width is None
    assert feed.image.height is None
    assert feed.docs is None

    assert feed.entries is not None
    assert len(feed.entries) == 1

    feed_entry = feed.entries[0]
    assert feed_entry.title == "Title 6"
    assert feed_entry.published_date is None


def test_complex_3():
    """Test parsing various actual XML files."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_complex_3.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None

    assert feed.title is None
    assert feed.subtitle is None
    assert feed.description is None
    assert feed.language is None
    assert feed.published_date is None
    assert feed.last_build_date is None
    assert feed.ttl is None
    assert feed.rights == "Feed Rights 1"
    assert feed.image is None

    assert feed.entries is not None
    assert len(feed.entries) == 2

    feed_entry = feed.entries[0]
    assert feed_entry.title is None
    assert feed_entry.published_date is None
    assert len(feed_entry.geometries) == 0

    feed_entry = feed.entries[1]
    assert feed_entry.title is None
    assert len(feed_entry.geometries) == 0


def test_geometries_2():
    """Test parsing various geometries in entries."""
    xml_parser = XmlParser()
    xml = load_fixture("xml_parser_geometries_1.xml")
    feed = xml_parser.parse(xml)
    assert feed is not None

    assert feed.title == "Feed Title 1"
    assert feed.entries is not None
    assert len(feed.entries) == 8

    feed_entry = feed.entries[0]
    assert feed_entry.title == "Title 1"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 3

    feed_entry = feed.entries[1]
    assert feed_entry.title == "Title 2"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 3

    feed_entry = feed.entries[2]
    assert feed_entry.title == "Title 3"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 2

    feed_entry = feed.entries[3]
    assert feed_entry.title == "Title 4"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 2

    feed_entry = feed.entries[4]
    assert feed_entry.title == "Title 5"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 3

    feed_entry = feed.entries[5]
    assert feed_entry.title == "Title 6"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 2

    feed_entry = feed.entries[6]
    assert feed_entry.title == "Title 7"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 2

    feed_entry = feed.entries[7]
    assert feed_entry.title == "Title 8"
    assert feed_entry.geometries is not None
    assert len(feed_entry.geometries) == 1


def test_byte_order_mark():
    """Test parsing an XML file with byte order mark."""
    xml_parser = XmlParser()
    # Create XML starting with byte order mark.
    xml = (
        "\xef\xbb\xbf<?xml version='1.0' encoding='utf-8'?>"
        "<rss version='2.0'><channel><item><title>Title 1</title>"
        "</item></channel></rss>"
    )
    # This will raise an error because the parser can't handle
    with pytest.raises(ExpatError):
        xml_parser.parse(xml)
