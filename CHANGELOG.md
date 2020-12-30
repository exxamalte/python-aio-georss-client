# Changes

## 0.7 (31/12/2020)
* Add non-standard namespace used by [EMSC feed](https://www.emsc-csem.org/service/rss/rss.php).

## 0.6 (02/11/2020)
* Added geometry features filter to exclude geometries from being taken into
  account for calculating distances.
* General code improvements.

## 0.5 (20/01/2020)
* Clear last timestamp when update fails.

## 0.4 (06/01/2020)
* Support multiple geometries per feed entry.
* Filter out duplicate geometries.
* Support GDACS bounding box.
* Improved distance calculation for polygons.
* Added conversion util for implementing libraries.
* Improved code quality. 

## 0.3 (11/12/2019)
* Fixes GDACS XML namespace.

## 0.2 (11/12/2019)
* Fixes bug that prevented external source from being read correctly.

## 0.1 (11/12/2019)
* Initial release as base for GeoRSS feeds.
* Calculating distance to home coordinates.
* Support for filtering by distance and category.
* Filter out entries without any geo location data.
* Simple Feed Manager.
