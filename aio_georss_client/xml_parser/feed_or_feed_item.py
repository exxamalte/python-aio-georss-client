"""GeoRSS feed or feed item."""

from __future__ import annotations

import datetime

from ..consts import (
    XML_ATTR_TERM,
    XML_TAG_AUTHOR,
    XML_TAG_CATEGORY,
    XML_TAG_CONTRIBUTOR,
    XML_TAG_DC_DATE,
    XML_TAG_LAST_BUILD_DATE,
    XML_TAG_MANAGING_EDITOR,
    XML_TAG_NAME,
    XML_TAG_PUB_DATE,
    XML_TAG_PUBLISHED,
    XML_TAG_UPDATED,
)
from .feed_dict_source import FeedDictSource


class FeedOrFeedItem(FeedDictSource):
    """Represents the common base of feed and its items."""

    @property
    def category(self) -> list[str] | None:
        """Return the categories of this feed item."""
        category = self._attribute([XML_TAG_CATEGORY])
        if category:
            if isinstance(category, (str, dict)):
                # If it's a string or a dict, wrap in list.
                category = [category]
            return FeedOrFeedItem._create_categories(category)
        return None

    @staticmethod
    def _create_categories(categories: list) -> list[str]:
        """Create categories from provided list."""
        result: list[str] = []
        for item in categories:
            if XML_ATTR_TERM in item:
                # <category term="Category 1"/>
                result.append(item.get(XML_ATTR_TERM))
            else:
                result.append(item)
        return result

    @property
    def published_date(self) -> datetime.datetime | None:
        """Return the published date of this feed or feed item."""
        parsed_date = self._attribute(
            [XML_TAG_PUB_DATE, XML_TAG_PUBLISHED, XML_TAG_DC_DATE]
        )
        return parsed_date if isinstance(parsed_date, datetime.datetime) else None

    @property
    def pub_date(self) -> datetime.datetime | None:
        """Return the published date of this feed or feed item."""
        return self.published_date

    @property
    def updated_date(self) -> datetime.datetime | None:
        """Return the updated date of this feed or feed item."""
        parsed_date = self._attribute([XML_TAG_LAST_BUILD_DATE, XML_TAG_UPDATED])
        return parsed_date if isinstance(parsed_date, datetime.datetime) else None

    @property
    def last_build_date(self) -> datetime.datetime | None:
        """Return the last build date of this feed."""
        return self.updated_date

    @property
    def author(self) -> str | None:
        """Return the author of this feed."""
        # <managingEditor>jrc-ems@ec.europa.eu</managingEditor>
        managing_editor: str = self._attribute([XML_TAG_MANAGING_EDITOR])
        if managing_editor:
            return managing_editor
        # <author>
        #   <name>Istituto Nazionale di Geofisica e Vulcanologia</name>
        #   <uri>http://www.ingv.it</uri>
        # </author>
        author = self._attribute([XML_TAG_AUTHOR, XML_TAG_CONTRIBUTOR])
        if author:
            name: str = author.get(XML_TAG_NAME, None)
            return name
        return None

    @property
    def contributor(self) -> str | None:
        """Return the contributor of this feed."""
        return self.author

    @property
    def managing_editor(self) -> str | None:
        """Return the managing editor of this feed."""
        return self.author
