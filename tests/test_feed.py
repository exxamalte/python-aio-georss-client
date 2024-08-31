"""Tests for base classes."""

import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest

from aio_georss_client.consts import UPDATE_ERROR, UPDATE_OK, UPDATE_OK_NO_DATA
from aio_georss_client.xml_parser.geometry import BoundingBox, Point, Polygon
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


@pytest.mark.asyncio
async def test_update_ok(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
        assert isinstance(feed_entry.external_id, str)
        assert feed_entry.external_id == str(hash(feed_entry.coordinates))

        feed_entry = entries[4]
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"


@pytest.mark.asyncio
async def test_update_ok_feed_2(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_2.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
async def test_update_ok_feed_3(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_3.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
        assert feed_entry.coordinates == (
            pytest.approx(-34.93728111547821),
            pytest.approx(148.59710883878262),
        )
        assert round(abs(feed_entry.distance_to_home - 491.7), 1) == 0

        feed_entry = entries[1]
        assert feed_entry.external_id == "2345"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (
            pytest.approx(-34.937170989),
            pytest.approx(148.597182317),
        )
        assert round(abs(feed_entry.distance_to_home - 491.7), 1) == 0

        feed_entry = entries[2]
        assert feed_entry.external_id == "3456"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Polygon)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (
            pytest.approx(-29.962746645660683),
            pytest.approx(152.43090880416074),
        )
        assert round(abs(feed_entry.distance_to_home - 176.5), 1) == 0

        feed_entry = entries[3]
        assert feed_entry.external_id == "4567"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Point)
        assert feed_entry.coordinates == (
            pytest.approx(-33.2345),
            pytest.approx(154.789),
        )
        assert round(abs(feed_entry.distance_to_home - 172.3), 1) == 0

        feed_entry = entries[4]
        assert feed_entry.external_id == "5678"
        assert len(feed_entry.geometries) == 2
        assert isinstance(feed_entry.geometries[0], Point)
        assert isinstance(feed_entry.geometries[1], Polygon)
        assert feed_entry.coordinates == (
            pytest.approx(-31.2345),
            pytest.approx(152.789),
        )
        assert round(abs(feed_entry.distance_to_home - 172.3), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_feed_6(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_6.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
        assert feed_entry.coordinates == (
            pytest.approx(-20.9041),
            pytest.approx(168.5652),
        )
        assert round(abs(feed_entry.distance_to_home - 1493.3), 1) == 0


@pytest.mark.asyncio
async def test_update_duplicate_geometries(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_7.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
async def test_update_ok_feed_8(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_8.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
        assert feed_entry.coordinates == (
            pytest.approx(-37.2345),
            pytest.approx(149.1234),
        )
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_with_radius_filtering(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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
async def test_update_ok_with_radius_and_category_filtering(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.OK,
            body=load_fixture("generic_feed_1.xml"),
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
async def test_update_error(mock_aioresponse):
    """Test updating feed results in error."""
    mock_aioresponse.get(
        "http://test.url/badpath",
        status=HTTPStatus.NOT_FOUND,
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(websession, HOME_COORDINATES_1, "http://test.url/badpath")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_ok_then_error(mock_aioresponse):
    """Test updating feed goes fine, followed by an error."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.NOT_FOUND,
        )

        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_with_request_exception(mock_aioresponse):
    """Test updating feed raises exception."""
    mock_aioresponse.get(
        "http://test.url/badpath",
        status=HTTPStatus.NOT_FOUND,
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(websession, HOME_COORDINATES_1, "http://test.url/badpath")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert entries is None
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_bom(mock_aioresponse):
    """Test updating feed with BOM (byte order mark) is ok."""
    xml = (
        "\xef\xbb\xbf<?xml version='1.0' encoding='utf-8'?>"
        "<rss version='2.0'><channel><item><title>Title 1</title>"
        "</item></channel></rss>"
    )
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=xml.encode("iso-8859-1"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
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


@pytest.mark.asyncio
async def test_update_not_xml(mock_aioresponse):
    """Test updating feed where returned payload is not XML."""
    # During tests it turned out that occasionally the GDACS server appears to return
    # invalid payload (00 control characters) which results in an exception thrown:
    # ExpatError: not well-formed (invalid token): line 1, column 0
    not_xml = "\x00\x00\x00"
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=not_xml,
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )
        assert (
            repr(feed) == "<MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK_NO_DATA
        assert entries is None
