"""Test geometries."""

from aio_georss_client.xml_parser.geometry import BoundingBox, Point, Polygon


def test_point():
    """Test point."""
    point = Point(-37.1234, 149.2345)
    assert point.latitude == -37.1234
    assert point.longitude == 149.2345
    assert repr(point) == "<Point(latitude=-37.1234, longitude=149.2345)>"


def test_point_equality():
    """Test points."""
    point1 = Point(10.0, 15.0)
    point2 = Point(10.0, 15.0)
    assert point1 == point2


def test_polygon():
    """Test polygon."""
    polygon = Polygon(
        [
            Point(-30.1, 150.1),
            Point(-30.2, 150.2),
            Point(-30.4, 150.4),
            Point(-30.8, 150.8),
            Point(-30.1, 150.1),
        ]
    )
    assert len(polygon.points) == 5
    assert polygon.centroid.latitude == -30.32
    assert polygon.centroid.longitude == 150.32
    assert (
        repr(polygon) == "<Polygon(centroid="
        "<Point(latitude=-30.32, longitude=150.32)>)>"
    )


def test_polygon_equality():
    """Test points."""
    polygon1 = Polygon(
        [
            Point(30.0, 30.0),
            Point(30.0, 35.0),
            Point(35.0, 35.0),
            Point(35.0, 30.0),
            Point(30.0, 30.0),
        ]
    )
    polygon2 = Polygon(
        [
            Point(30.0, 30.0),
            Point(30.0, 35.0),
            Point(35.0, 35.0),
            Point(35.0, 30.0),
            Point(30.0, 30.0),
        ]
    )
    assert polygon1 == polygon2


def test_point_in_polygon_1():
    """Test if point is in polygon."""
    polygon = Polygon(
        [Point(30.0, 30.0), Point(30.0, 35.0), Point(35.0, 35.0), Point(30.0, 30.0)]
    )
    # 1. Outside
    point = Point(20.0, 20.0)
    assert not polygon.is_inside(point)
    # 2. Inside
    point = Point(31.0, 32.0)
    assert polygon.is_inside(point)
    # 3. Inside
    point = Point(30.0, 32.0)
    assert polygon.is_inside(point)
    # 4. Inside
    point = Point(30.0, 35.0)
    assert polygon.is_inside(point)
    # 5. Outside
    point = Point(34.0, 31.0)
    assert not polygon.is_inside(point)


def test_point_in_polygon_2():
    """Test if point is in polygon."""
    polygon = Polygon(
        [
            Point(30.0, -30.0),
            Point(30.0, -25.0),
            Point(35.0, -25.0),
            Point(30.0, -30.0),
        ]
    )
    # 1. Outside
    point = Point(20.0, -40.0)
    assert not polygon.is_inside(point)
    # 2. Inside
    point = Point(31.0, -28.0)
    assert polygon.is_inside(point)
    # 3. Inside
    point = Point(30.0, -28.0)
    assert polygon.is_inside(point)
    # 4. Inside
    point = Point(30.0, -25.0)
    assert polygon.is_inside(point)
    # 5. Outside
    point = Point(34.0, -29.0)
    assert not polygon.is_inside(point)
    # 6. Invalid point
    assert not polygon.is_inside(None)


def test_bounding_box_1():
    """Test bounding box."""
    bbox = BoundingBox(Point(-30.0, 148.0), Point(-28.0, 150.0))
    assert (
        repr(bbox) == "<BoundingBox(bottom_left="
        "<Point(latitude=-30.0, longitude=148.0)>, "
        "top_right="
        "<Point(latitude=-28.0, longitude=150.0)>)>"
    )
    assert bbox.centroid.latitude == -29.0
    assert bbox.centroid.longitude == 149.0
    assert bbox.is_inside(Point(-29.5, 148.1))
    assert not bbox.is_inside(Point(-29.5, 147.9))


def test_bounding_box_2():
    """Test bounding box."""
    bbox = BoundingBox(Point(-5.0, 175.0), Point(5.0, -175.0))
    assert (
        repr(bbox) == "<BoundingBox(bottom_left="
        "<Point(latitude=-5.0, longitude=175.0)>, "
        "top_right="
        "<Point(latitude=5.0, longitude=-175.0)>)>"
    )
    assert bbox.centroid.latitude == 0.0
    assert bbox.centroid.longitude == 180.0
    assert bbox.is_inside(Point(-2.5, 179.0))
    assert not bbox.is_inside(Point(2.5, 170.0))


def test_bounding_box_3():
    """Test bounding box."""
    bbox = BoundingBox(Point(-5.0, 175.0), Point(5.0, -175.0))
    assert (
        repr(bbox) == "<BoundingBox(bottom_left="
        "<Point(latitude=-5.0, longitude=175.0)>, "
        "top_right="
        "<Point(latitude=5.0, longitude=-175.0)>)>"
    )
    assert bbox.centroid.latitude == 0.0
    assert bbox.centroid.longitude == 180.0
    assert bbox.is_inside(Point(-2.5, -179.0))
    assert not bbox.is_inside(Point(2.5, -170.0))
    # Special case to increase test coverage.
    assert not bbox.is_inside(None)


def test_bounding_box_equality():
    """Test points."""
    bbox1 = BoundingBox(Point(10.0, 10.0), Point(20.0, 20.0))
    bbox2 = BoundingBox(Point(10.0, 10.0), Point(20.0, 20.0))
    assert bbox1 == bbox2
