# python-aio-georss-client

[![Build Status](https://img.shields.io/github/actions/workflow/status/exxamalte/python-aio-georss-client/ci.yaml)](https://github.com/exxamalte/python-aio-georss-client/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/exxamalte/python-aio-georss-client/branch/master/graph/badge.svg?token=JHET53MLPC)](https://codecov.io/gh/exxamalte/python-aio-georss-client)
[![PyPi](https://img.shields.io/pypi/v/aio-georss-client.svg)](https://pypi.python.org/pypi/aio-georss-client)
[![Version](https://img.shields.io/pypi/pyversions/aio-georss-client.svg)](https://pypi.python.org/pypi/aio-georss-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/29d6a4a8caeac24a91bd/maintainability)](https://codeclimate.com/github/exxamalte/python-aio-georss-client/maintainability)

This library provides convenient async access to [GeoRSS](http://www.georss.org/) Feeds.

## Installation
`pip install aio-georss-client`

## Known Implementations

| Library  | Source  | Topic  |
|----------|---------|--------|
| [aio_georss_gdacs](https://github.com/exxamalte/python-aio-georss-gdacs) | Global Disaster Alert and Coordination System (GDACS) | Natural Disasters |

## Usage
Each implementation extracts relevant information from the GeoJSON feed. Not 
all feeds contain the same level of information, or present their information 
in different ways.

After instantiating a particular class and supply the required parameters, you 
can call `update` to retrieve the feed data. The return value will be a tuple 
of a status code and the actual data in the form of a list of feed entries 
specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

## Geometry Features
This library supports 3 different types of geometries:
* Point
* Polygon
* Bounding Box

By default each feed entry is using all available geometries from the external
feed. If required however, you can exclude geometries by overriding 
FeedEntry#features and only return the geometries you want to support in your
specific implementation.


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
