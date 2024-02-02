"""Tests for GeoRSS distance helper."""
from unittest.mock import MagicMock

import pytest

from aio_georss_client.geo_rss_distance_helper import GeoRssDistanceHelper
from aio_georss_client.xml_parser.geometry import BoundingBox, Point, Polygon


def test_extract_coordinates_from_point():
    """Test extracting coordinates from point."""
    mock_point = Point(-30.0, 151.0)
    latitude, longitude = GeoRssDistanceHelper.extract_coordinates(mock_point)
    assert latitude == -30.0
    assert longitude == 151.0


def test_extract_coordinates_from_polygon():
    """Test extracting coordinates from polygon."""
    mock_polygon = Polygon(
        [
            Point(-30.0, 151.0),
            Point(-30.0, 151.5),
            Point(-30.5, 151.5),
            Point(-30.5, 151.0),
            Point(-30.0, 151.0),
        ]
    )
    latitude, longitude = GeoRssDistanceHelper.extract_coordinates(mock_polygon)
    assert latitude == pytest.approx(-30.2, 0.1)
    assert longitude == pytest.approx(151.2, 0.1)


def test_extract_coordinates_from_unsupported_geometry():
    """Test extracting coordinates from unsupported geometry."""
    mock_unsupported_geometry = MagicMock()
    latitude, longitude = GeoRssDistanceHelper.extract_coordinates(
        mock_unsupported_geometry
    )
    assert latitude is None
    assert longitude is None


def test_distance_to_point():
    """Test calculating distance to point."""
    home_coordinates = (-31.0, 150.0)
    mock_point = Point(-30.0, 151.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_point)
    assert distance == pytest.approx(146.8, 0.1)


def test_distance_to_polygon_1():
    """Test calculating distance to polygon."""
    home_coordinates = (-31.0, 150.0)
    mock_polygon = Polygon(
        [
            Point(-30.0, 151.0),
            Point(-30.0, 151.5),
            Point(-30.5, 151.5),
            Point(-30.5, 151.0),
            Point(-30.0, 151.0),
        ]
    )
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(110.6, 0.1)


def test_distance_to_polygon_2():
    """Test calculating distance to polygon."""
    home_coordinates = (-30.2, 151.2)
    mock_polygon = Polygon(
        [
            Point(-30.0, 151.0),
            Point(-30.0, 151.5),
            Point(-30.5, 151.5),
            Point(-30.5, 151.0),
            Point(-30.0, 151.0),
        ]
    )
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(0.0, 0.1)


def test_distance_to_polygon_3():
    """Test calculating distance to polygon."""
    home_coordinates = (-29.0, 151.2)
    mock_polygon = Polygon(
        [
            Point(-30.0, 151.0),
            Point(-30.0, 151.5),
            Point(-30.5, 151.5),
            Point(-30.5, 151.0),
            Point(-30.0, 151.0),
        ]
    )
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(111.2, 0.1)


def test_distance_to_polygon_4():
    """Test calculating distance to polygon."""
    home_coordinates = (30.0, 151.3)
    mock_polygon = Polygon(
        [
            Point(30.0, 151.0),
            Point(30.0, 151.5),
            Point(30.5, 151.5),
            Point(30.5, 151.0),
            Point(30.0, 151.0),
        ]
    )
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(0.0, 0.1)


def test_distance_to_polygon_5():
    """Test calculating distance to polygon."""
    mock_polygon = Polygon(
        [
            Point(30.0, 179.0),
            Point(30.0, -179.5),
            Point(30.5, -179.5),
            Point(30.5, 179.0),
            Point(30.0, 179.0),
        ]
    )
    home_coordinates = (30.2, -177.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(240.3, 0.1)
    home_coordinates = (30.1, 178.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(96.2, 0.1)
    home_coordinates = (31.0, -179.8)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(55.6, 0.1)
    home_coordinates = (31.0, 179.8)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(55.6, 0.1)


def test_distance_to_polygon_6():
    """Test calculating distance to polygon."""
    mock_polygon = Polygon(
        [
            Point(-30.0, 179.0),
            Point(-30.0, -179.5),
            Point(-29.5, -179.5),
            Point(-29.5, 179.0),
            Point(-30.0, 179.0),
        ]
    )
    home_coordinates = (-29.8, -177.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(241.2, 0.1)
    home_coordinates = (-29.9, 178.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(96.4, 0.1)
    home_coordinates = (-29.0, -179.8)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(55.6, 0.1)
    home_coordinates = (-29.0, 179.8)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_polygon)
    assert distance == pytest.approx(55.6, 0.1)


def test_distance_to_bbox_1():
    """Test calculating distance to bounding box."""
    home_coordinates = (20.0, 20.0)
    # 1. inside
    mock_bbox = BoundingBox(Point(10.0, 10.0), Point(30.0, 30.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(0.0, 0.1)
    # 2. above-left
    mock_bbox = BoundingBox(Point(10.0, 25.0), Point(15.0, 30.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(768.1, 0.1)
    # 3. above
    mock_bbox = BoundingBox(Point(10.0, 15.0), Point(15.0, 25.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(556.0, 0.1)
    # 4. above-right
    mock_bbox = BoundingBox(Point(10.0, 10.0), Point(15.0, 15.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(768.1, 0.1)
    # 5. left
    mock_bbox = BoundingBox(Point(15.0, 25.0), Point(25.0, 30.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(522.4, 0.1)
    # 6. right
    mock_bbox = BoundingBox(Point(15.0, 10.0), Point(25.0, 15.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(522.4, 0.1)
    # 7. below-left
    mock_bbox = BoundingBox(Point(25.0, 25.0), Point(30.0, 30.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(756.8, 0.1)
    # 8. below
    mock_bbox = BoundingBox(Point(25.0, 15.0), Point(30.0, 25.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(556.0, 0.1)
    # 9. below-right
    mock_bbox = BoundingBox(Point(25.0, 10.0), Point(30.0, 15.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(756.8, 0.1)
    # special case
    home_coordinates = (-20.0, -20.0)
    mock_bbox = BoundingBox(Point(-30.0, -15.0), Point(-25.0, -10.0))
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(756.8, 0.1)


def test_distance_to_bbox_2():
    """Test calculating distance to bounding box."""
    mock_bbox = BoundingBox(Point(5.0, 175.0), Point(15.0, -175.0))
    # 1. inside
    home_coordinates = (5.0, 176.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(0.0, 0.1)
    # 2. above-left
    home_coordinates = (20.0, 170.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(768.1, 0.1)
    # 3. above-right
    home_coordinates = (20.0, -170.0)
    distance = GeoRssDistanceHelper.distance_to_geometry(home_coordinates, mock_bbox)
    assert distance == pytest.approx(768.1, 0.1)


def test_distance_to_unsupported_geometry():
    """Test calculating distance to unsupported geometry."""
    home_coordinates = (-31.0, 150.0)
    mock_unsupported_geometry = MagicMock()
    distance = GeoRssDistanceHelper.distance_to_geometry(
        home_coordinates, mock_unsupported_geometry
    )
    assert distance == float("inf")
