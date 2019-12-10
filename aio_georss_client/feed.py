"""GeoRSS Feed."""
import asyncio
import codecs
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import aiohttp
from aiohttp import ClientSession, client_exceptions

from .consts import ATTR_ATTRIBUTION, UPDATE_OK, UPDATE_OK_NO_DATA, \
    UPDATE_ERROR, DEFAULT_REQUEST_TIMEOUT
from .xml_parser import XmlParser

_LOGGER = logging.getLogger(__name__)


class GeoRssFeed(ABC):
    """GeoRSS feed base class."""

    def __init__(self, websession: ClientSession, home_coordinates, url: str,
                 filter_radius: float = None,
                 filter_categories=None):
        """Initialise this service."""
        self._websession = websession
        self._home_coordinates = home_coordinates
        self._filter_radius = filter_radius
        self._filter_categories = filter_categories
        self._url = url
        self._last_timestamp = None

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={}, categories={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius, self._filter_categories)

    @abstractmethod
    def _new_entry(self, home_coordinates, rss_entry, global_data):
        """Generate a new entry."""
        pass

    def _client_session_timeout(self) -> int:
        """Define client session timeout in seconds. Override if necessary."""
        return DEFAULT_REQUEST_TIMEOUT

    def _additional_namespaces(self):
        """Provide additional namespaces, relevant for this feed."""
        pass

    async def update(self):
        """Update from external source and return filtered entries."""
        status, data = await self._fetch()
        if status == UPDATE_OK:
            if data:
                entries = []
                global_data = self._extract_from_feed(data)
                # Extract data from feed entries.
                for rss_entry in data.entries:
                    entries.append(self._new_entry(self._home_coordinates,
                                                   rss_entry, global_data))
                filtered_entries = self._filter_entries(entries)
                self._last_timestamp = self._extract_last_timestamp(
                    filtered_entries)
                return UPDATE_OK, filtered_entries
            else:
                # Should not happen.
                return UPDATE_OK, None
        elif status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        else:
            # Error happened while fetching the feed.
            return UPDATE_ERROR, None

    async def _fetch(self, method: str = "GET", headers=None, params=None):
        """Fetch GeoRSS data from external source."""
        try:
            timeout = aiohttp.ClientTimeout(
                total=self._client_session_timeout())
            async with self._websession.request(
                    method, self._url, headers=headers, params=params,
                    timeout=timeout
            ) as response:
                try:
                    response.raise_for_status()
                    text = await self._read_response(response)
                    parser = XmlParser(self._additional_namespaces())
                    feed_data = parser.parse(text)
                    self.parser = parser
                    self.feed_data = feed_data
                    return UPDATE_OK, feed_data
                except client_exceptions.ClientError as client_error:
                    _LOGGER.warning("Fetching data from %s failed with %s",
                                    self._url, client_error)
                    return UPDATE_ERROR, None
        except client_exceptions.ClientError as client_error:
            _LOGGER.warning("Requesting data from %s failed with "
                            "client error: %s",
                            self._url, client_error)
            return UPDATE_ERROR, None
        except asyncio.TimeoutError:
            _LOGGER.warning("Requesting data from %s failed with "
                            "timeout error", self._url)
            return UPDATE_ERROR, None

    async def _read_response(self, response):
        """Pre-process the response."""
        if response:
            _LOGGER.debug("Response encoding %s", response.get_encoding())
            raw_response = await response.read()
            print(raw_response)
            print(raw_response.startswith(codecs.BOM_UTF8))
            if raw_response.startswith(codecs.BOM_UTF8):
                return codecs.decode(raw_response, 'utf-8-sig')
            return await response.text()
        return None

    def _filter_entries(self, entries):
        """Filter the provided entries."""
        filtered_entries = entries
        _LOGGER.debug("Entries before filtering %s", filtered_entries)
        # Always remove entries without geometry
        filtered_entries = list(
            filter(lambda entry:
                   entry.geometry is not None,
                   filtered_entries))
        # Filter by distance.
        if self._filter_radius:
            filtered_entries = list(
                filter(lambda entry:
                       entry.distance_to_home <= self._filter_radius,
                       filtered_entries))
        # Filter by category.
        if self._filter_categories:
            filtered_entries = list(
                filter(lambda entry:
                       len({entry.category}.intersection(
                           self._filter_categories)) > 0,
                       filtered_entries))
        _LOGGER.debug("Entries after filtering %s", filtered_entries)
        return filtered_entries

    def _extract_from_feed(self, feed):
        """Extract global metadata from feed."""
        global_data = {}
        author = feed.author
        if author:
            global_data[ATTR_ATTRIBUTION] = author
        return global_data

    def _extract_last_timestamp(self, feed_entries):
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(
                [entry.published for entry in feed_entries if entry.published],
                reverse=True)
            if dates:
                last_timestamp = dates[0]
                _LOGGER.debug("Last timestamp: %s", last_timestamp)
                return last_timestamp
        return None

    @property
    def last_timestamp(self) -> Optional[datetime]:
        """Return the last timestamp extracted from this feed."""
        return self._last_timestamp
