"""GeoRSS Distance Helper."""
import logging
from typing import Optional

from haversine import haversine

from .xml_parser.geometry import Point, Polygon, BoundingBox, Geometry

_LOGGER = logging.getLogger(__name__)


class GeoRssDistanceHelper:
    """Helper to calculate distances between GeoRSS geometries."""

    def __init__(self):
        """Initialize the geo distance helper."""
        pass

    @staticmethod
    def extract_coordinates(geometry):
        """Extract the best coordinates from the feature for display."""
        latitude = longitude = None
        if isinstance(geometry, Point):
            # Just extract latitude and longitude directly.
            latitude, longitude = geometry.latitude, geometry.longitude
        elif isinstance(geometry, (Polygon, BoundingBox)):
            centroid = geometry.centroid
            latitude, longitude = centroid.latitude, centroid.longitude
            _LOGGER.debug("Centroid of %s is %s", geometry,
                          (latitude, longitude))
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return latitude, longitude

    @staticmethod
    def distance_to_geometry(home_coordinates, geometry: Geometry) -> float:
        """Calculate the distance between home coordinates and geometry."""
        distance = float("inf")
        if isinstance(geometry, Point):
            distance = GeoRssDistanceHelper._distance_to_point(
                home_coordinates, geometry)
        elif isinstance(geometry, Polygon):
            distance = GeoRssDistanceHelper._distance_to_polygon(
                home_coordinates, geometry)
        elif isinstance(geometry, BoundingBox):
            distance = GeoRssDistanceHelper._distance_to_bounding_box(
                home_coordinates, geometry)
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return distance

    @staticmethod
    def _distance_to_point(home_coordinates, point: Point) -> float:
        """Calculate the distance between home coordinates and the point."""
        # Swap coordinates to match: (latitude, longitude).
        return GeoRssDistanceHelper._distance_to_coordinates(
            home_coordinates, (point.latitude, point.longitude))

    @staticmethod
    def _distance_to_polygon(home_coordinates, polygon: Polygon) -> float:
        """Calculate the distance between home coordinates and the polygon."""
        distance = float("inf")
        # Check if home is inside the polygon.
        if polygon.is_inside(Point(home_coordinates[0], home_coordinates[1])):
            return 0.0
        # Calculate distance from polygon by first calculating the distance
        # to each point of the polygon.
        for point in polygon.points:
            distance = min(distance,
                           GeoRssDistanceHelper._distance_to_coordinates(
                               home_coordinates,
                               (point.latitude, point.longitude)))
        # Next calculate the distance to each edge of the polygon.
        for edge in polygon.edges:
            distance = min(distance, GeoRssDistanceHelper._distance_to_edge(
                home_coordinates, edge))
        return distance

    @staticmethod
    def _distance_to_bounding_box(home_coordinates: tuple,
                                  bbox: BoundingBox) -> float:
        """Calculate the distance between home coordinates and the bbox."""
        distance = float("inf")
        # Check if home is inside the bounding box.
        # home_coordinates is tuple of (latitude, longitude)
        if bbox.is_inside(Point(home_coordinates[0], home_coordinates[1])):
            return 0.0
        # Now distinguish 8 more cases / quadrants:
        transposed_point_longitude = home_coordinates[1]
        transposed_top_right_longitude = bbox.top_right.longitude
        if bbox.bottom_left.longitude > bbox.top_right.longitude:
            # bounding box spans across 180 degree longitude
            transposed_top_right_longitude = bbox.top_right.longitude + 360
            # only in this case, also transpose the point's longitude
            if transposed_point_longitude < 0:
                transposed_point_longitude += 360
        target_point = None
        if home_coordinates[0] > bbox.top_right.latitude:
            # 1 - above-left
            if transposed_point_longitude < bbox.bottom_left.longitude:
                # Calculate distance to top left point of bbox.
                target_point = (bbox.top_right.latitude,
                                bbox.bottom_left.longitude)
            # 2 - above-centre
            if bbox.bottom_left.longitude <= transposed_point_longitude \
                    <= transposed_top_right_longitude:
                # Calculate distance to top latitude of bbox.
                target_point = (bbox.top_right.latitude, home_coordinates[1])
            # 3 - above-right
            if transposed_point_longitude > transposed_top_right_longitude:
                # Calculate distance to top right point of bbox.
                target_point = (bbox.top_right.latitude,
                                bbox.top_right.longitude)
        if bbox.top_right.latitude >= home_coordinates[0] \
                >= bbox.bottom_left.latitude:
            # 4 - left
            if transposed_point_longitude < bbox.bottom_left.longitude:
                # Calculate distance to left longitude of bbox.
                target_point = (home_coordinates[0],
                                bbox.bottom_left.longitude)
            # 5 - right
            if transposed_point_longitude > transposed_top_right_longitude:
                # Calculate distance to right longitude of bbox.
                target_point = (home_coordinates[0], bbox.top_right.longitude)
        if home_coordinates[0] < bbox.bottom_left.latitude:
            # 6 - below-left
            if transposed_point_longitude < bbox.bottom_left.longitude:
                # Calculate distance to bottom left point of bbox.
                target_point = (bbox.bottom_left.latitude,
                                bbox.bottom_left.longitude)
            # 7 - below-centre
            if bbox.bottom_left.longitude <= transposed_point_longitude \
                    <= transposed_top_right_longitude:
                # Calculate distance to bottom latitude of bbox.
                target_point = (bbox.bottom_left.latitude, home_coordinates[1])
            # 8 - below-right
            if transposed_point_longitude > transposed_top_right_longitude:
                # Calculate distance to bottom right point of bbox.
                target_point = (bbox.bottom_left.latitude,
                                bbox.top_right.longitude)
        if target_point:
            return GeoRssDistanceHelper._distance_to_coordinates(
                home_coordinates,
                target_point)
        return distance

    @staticmethod
    def _distance_to_coordinates(home_coordinates: tuple, coordinates: tuple):
        """Calculate the distance between home coordinates and the
        coordinates."""
        # Expecting coordinates in format: (latitude, longitude).
        return haversine(coordinates, home_coordinates)

    @staticmethod
    def _distance_to_edge(home_coordinates: tuple, edge: tuple):
        """Calculate distance between home coordinates and provided edge."""
        perpendicular_point = GeoRssDistanceHelper._perpendicular_point(
            edge, Point(home_coordinates[0], home_coordinates[1]))
        # If there is a perpendicular point on the edge -> calculate distance.
        # If there isn't, then the distance to the end points of the edge will
        # need to be considered separately.
        if perpendicular_point:
            return GeoRssDistanceHelper._distance_to_point(home_coordinates,
                                                           perpendicular_point)
        return float("inf")

    @staticmethod
    def _perpendicular_point(edge, point) -> Optional[Point]:
        """Find a perpendicular point on the edge to the provided point."""
        a, b = edge
        px = point.longitude
        py = point.latitude
        ax = a.longitude
        ay = a.latitude
        bx = b.longitude
        by = b.latitude
        dx = bx - ax
        dy = by - ay
        shortest_length = ((dx * (px - ax)) + (dy * (py - ay))) \
                          / ((dx * dx) + (dy * dy))
        rx = ax + dx * shortest_length
        ry = ay + dy * shortest_length
        if bx >= rx >= ax and by >= ry >= ay:
            return Point(ry, rx)
        return None
