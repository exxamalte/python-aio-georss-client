"""Tests for base classes."""
import datetime

import aiohttp
import pytest

from aio_georss_client.consts import UPDATE_ERROR, UPDATE_OK
from aio_georss_client.xml_parser.geometry import BoundingBox, Point, Polygon
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 5

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.category == "Category 1"
        assert feed_entry.published == datetime.datetime(2018, 9, 23, 8, 30)
        assert feed_entry.updated == datetime.datetime(2018, 9, 23, 8, 35)
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0
        assert repr(feed_entry) == "<MockFeedEntry(id=1234)>"

        feed_entry = entries[1]
        assert feed_entry.title == "Title 2"
        assert feed_entry.external_id == "2345"
        assert feed_entry.attribution is None
        assert repr(feed_entry) == "<MockFeedEntry(id=2345)>"

        feed_entry = entries[2]
        assert feed_entry.title == "Title 3"
        assert feed_entry.external_id == "Title 3"

        feed_entry = entries[3]
        assert feed_entry.title is None
        assert feed_entry.external_id == hash(feed_entry.coordinates)

        feed_entry = entries[4]
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"


@pytest.mark.asyncio
async def test_update_ok_feed_2(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_2.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.category == "Category 1"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_feed_3(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_3.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 5

        feed_entry = entries[0]
        assert feed_entry.external_id == "1234"
        assert len(feed_entry.geometries) == 1
        assert isinstance(feed_entry.geometries[0], Polygon)
        assert feed_entry.coordinates == (-34.93728111547821, 148.59710883878262)
        assert round(abs(feed_entry.distance_to_home - 491.7), 1) == 0

        feed_entry = entries[1]
        assert feed_entry.external_id == "2345"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (-34.937170989, 148.597182317)
        assert round(abs(feed_entry.distance_to_home - 491.7), 1) == 0

        feed_entry = entries[2]
        assert feed_entry.external_id == "3456"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Polygon)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (-29.962746645660683, 152.43090880416074)
        assert round(abs(feed_entry.distance_to_home - 176.5), 1) == 0

        feed_entry = entries[3]
        assert feed_entry.external_id == "4567"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Point)
        assert feed_entry.coordinates == (-33.2345, 154.789)
        assert round(abs(feed_entry.distance_to_home - 172.3), 1) == 0

        feed_entry = entries[4]
        assert feed_entry.external_id == "5678"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (-31.2345, 152.789)
        assert round(abs(feed_entry.distance_to_home - 172.3), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_feed_6(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_6.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.external_id == "1234"
        assert len(feed_entry.geometries) == 1
        assert isinstance(feed_entry.geometries[0], BoundingBox)
        assert feed_entry.coordinates == (-20.9041, 168.5652)
        assert round(abs(feed_entry.distance_to_home - 1493.3), 1) == 0


@pytest.mark.asyncio
async def test_update_duplicate_geometries(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_7.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 4

        feed_entry = entries[0]
        assert feed_entry.external_id == "1234"
        assert len(feed_entry.geometries) == 1
        assert isinstance(feed_entry.geometries[0], Point)

        feed_entry = entries[1]
        assert feed_entry.external_id == "2345"
        assert len(feed_entry.geometries) == 1
        assert isinstance(feed_entry.geometries[0], Point)

        feed_entry = entries[2]
        assert feed_entry.external_id == "3456"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Polygon)

        feed_entry = entries[3]
        assert feed_entry.external_id == "4567"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], BoundingBox)


@pytest.mark.asyncio
async def test_update_ok_feed_8(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_8.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.category == "Category 1"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_with_radius_filtering(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(
            websession,
            HOME_COORDINATES_2,
            "http://test.url/testpath",
            filter_radius=90.0,
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 4
        assert round(abs(entries[0].distance_to_home - 82.0), 1) == 0
        assert round(abs(entries[1].distance_to_home - 77.0), 1) == 0
        assert round(abs(entries[2].distance_to_home - 84.6), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_with_radius_and_category_filtering(aresponses, event_loop):
    """Test updating feed is ok."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(
            websession,
            HOME_COORDINATES_2,
            "http://test.url/testpath",
            filter_radius=90.0,
            filter_categories=["Category 2"],
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1
        assert round(abs(entries[0].distance_to_home - 77.0), 1) == 0

        aresponses.add(
            "test.url",
            "/testpath",
            "get",
            aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
        )

        feed = MockGeoRssFeed(
            websession,
            HOME_COORDINATES_2,
            "http://test.url/testpath",
            filter_radius=90.0,
            filter_categories=["Category 4"],
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0


@pytest.mark.asyncio
async def test_update_error(aresponses, event_loop):
    """Test updating feed results in error."""
    aresponses.add("test.url", "/badpath", "get", aresponses.Response(status=404))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(websession, HOME_COORDINATES_1, "http://test.url/badpath")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_ok_then_error(aresponses, event_loop):
    """Test updating feed goes fine, followed by an error."""
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 5
        assert feed.last_timestamp is not None

        aresponses.add("test.url", "/testpath", "get", aresponses.Response(status=404))

        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_with_request_exception(aresponses, event_loop):
    """Test updating feed raises exception."""
    aresponses.add("test.url", "/badpath", "get", aresponses.Response(status=404))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(websession, HOME_COORDINATES_1, "http://test.url/badpath")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert entries is None
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_bom(aresponses, event_loop):
    """Test updating feed with BOM (byte order mark) is ok."""
    xml = (
        "\xef\xbb\xbf<?xml version='1.0' encoding='utf-8'?>"
        "<rss version='2.0'><channel><item><title>Title 1</title>"
        "</item></channel></rss>"
    )
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=xml, charset="iso-8859-1", status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
