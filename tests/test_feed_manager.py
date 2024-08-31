"""Test for the generic georss feed manager."""

import asyncio
import datetime
from http import HTTPStatus
from unittest import mock as async_mock

import aiohttp
import pytest

from aio_georss_client.consts import UPDATE_OK_NO_DATA
from aio_georss_client.feed_manager import FeedManagerBase
from aio_georss_client.status_update import StatusUpdate
from tests import MockGeoRssFeed
from tests.utils import load_fixture

HOME_COORDINATES_1 = (-31.0, 151.0)
HOME_COORDINATES_2 = (-37.0, 150.0)


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(entity_external_id: str) -> None:
            """Generate new entity."""
            generated_entity_external_ids.append(entity_external_id)

        async def _update_entity(entity_external_id: str) -> None:
            """Update entity."""
            updated_entity_external_ids.append(entity_external_id)

        async def _remove_entity(entity_external_id: str) -> None:
            """Remove entity."""
            removed_entity_external_ids.append(entity_external_id)

        feed_manager = FeedManagerBase(
            feed, _generate_entity, _update_entity, _remove_entity
        )
        assert (
            repr(feed_manager) == "<FeedManagerBase("
            "feed=<MockGeoRssFeed(home="
            "(-31.0, 151.0), "
            "url=http://test.url/testpath, "
            "radius=None, categories=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 5
        assert feed_manager.last_update is not None
        assert feed_manager.last_timestamp == datetime.datetime(2018, 9, 23, 9, 10)

        assert len(generated_entity_external_ids) == 5
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        feed_entry = entries.get("1234")
        assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-37.2345, 149.1234)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0
        assert repr(feed_entry) == "<MockFeedEntry(id=1234)>"

        feed_entry = entries.get("2345")
        assert feed_entry.title == "Title 2"
        assert feed_entry.external_id == "2345"

        feed_entry = entries.get("Title 3")
        assert feed_entry.title == "Title 3"
        assert feed_entry.external_id == "Title 3"

        external_id = str(hash((-37.8901, 149.7890)))
        feed_entry = entries.get(external_id)
        assert feed_entry.title is None
        assert feed_entry.external_id == external_id

        feed_entry = entries.get("5678")
        assert feed_entry.title == "Title 5"
        assert feed_entry.external_id == "5678"

        # Simulate an update with several changes.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.OK,
            body=load_fixture("generic_feed_4.xml"),
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 1
        assert len(updated_entity_external_ids) == 2
        assert len(removed_entity_external_ids) == 3

        feed_entry = entries.get("1234")
        assert feed_entry.title == "Title 1 UPDATED"

        feed_entry = entries.get("2345")
        assert feed_entry.title == "Title 2"

        feed_entry = entries.get("6789")
        assert feed_entry.title == "Title 6"

        # Simulate an update with no data.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        with async_mock.patch(
            "aio_georss_client.feed.GeoRssFeed._fetch",
            new_callable=async_mock.AsyncMock,
        ) as mock_fetch:
            mock_fetch.return_value = (UPDATE_OK_NO_DATA, None)

            await feed_manager.update()
            entries = feed_manager.feed_entries

            assert len(entries) == 3
            assert len(generated_entity_external_ids) == 0
            assert len(updated_entity_external_ids) == 0
            assert len(removed_entity_external_ids) == 0

        # Simulate an update producing an error.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 0
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 3


@pytest.mark.asyncio
async def test_feed_manager_no_timestamp(mock_aioresponse):
    """Test updating feed is ok."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_5.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id: str) -> None:
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id: str) -> None:
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id: str) -> None:
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = FeedManagerBase(
            feed, _generate_entity, _update_entity, _remove_entity
        )
        assert (
            repr(feed_manager) == "<FeedManagerBase("
            "feed=<MockGeoRssFeed(home="
            "(-31.0, 151.0), "
            "url=http://test.url/testpath, "
            "radius=None, categories=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 1
        assert feed_manager.last_timestamp is None


@pytest.mark.asyncio
async def test_feed_manager_with_status_callback(mock_aioresponse):
    """Test the feed manager."""
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_1.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockGeoRssFeed(
            websession, HOME_COORDINATES_1, "http://test.url/testpath"
        )

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []
        status_update = []

        async def _generate_entity(external_id: str) -> None:
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id: str) -> None:
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id: str) -> None:
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        async def _status(status_details: StatusUpdate) -> None:
            """Capture status update details."""
            status_update.append(status_details)

        feed_manager = FeedManagerBase(
            feed, _generate_entity, _update_entity, _remove_entity, _status
        )
        assert (
            repr(feed_manager) == "<FeedManagerBase(feed=<"
            "MockGeoRssFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, "
            "radius=None, categories=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 5
        assert feed_manager.last_update is not None
        assert feed_manager.last_timestamp == datetime.datetime(2018, 9, 23, 9, 10)

        assert len(generated_entity_external_ids) == 5
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        assert status_update[0].status == "OK"
        assert status_update[0].last_update is not None
        last_update_successful = status_update[0].last_update_successful
        assert status_update[0].last_update == last_update_successful
        assert status_update[0].last_timestamp == datetime.datetime(2018, 9, 23, 9, 10)
        assert status_update[0].total == 5
        assert status_update[0].created == 5
        assert status_update[0].updated == 0
        assert status_update[0].removed == 0
        assert (
            repr(status_update[0]) == f"<StatusUpdate("
            f"OK@{status_update[0].last_update})>"
        )

        # Simulate an update with no data.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()
        status_update.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 0
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 5

        assert status_update[0].status == "ERROR"
        assert status_update[0].last_update is not None
        assert status_update[0].last_update_successful is not None
        assert status_update[0].last_update_successful == last_update_successful
        assert status_update[0].total == 0
