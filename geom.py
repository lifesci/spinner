import math
from dataclasses import dataclass
from typing import List


def deg_to_rad(deg):
    return (deg / 360 * 2 * math.pi) % (2 * math.pi)


def rad_to_deg(rad):
    return (rad / (2 * math.pi) * 360) % 360


def pct_to_rad(pct):
    return (2 * math.pi * pct) % (2 * math.pi)


def point_to_angle(point, radius):
    acos = math.acos(point.x / radius)

    if point.y > 0:
        angle = acos
    else:
        angle = 2 * math.pi - acos

    return angle % (2 * math.pi)


def angle_to_point(angle, center, radius):
    x = center.x + math.cos(angle) * radius
    y = center.y - math.sin(angle) * radius
    return Point(x, y)


@dataclass
class Point:
    x: float
    y: float

    def rotate(self, angle, radius, center):
        offset_point = self - center

        start_angle = point_to_angle(offset_point, radius)

        angle_offset = pct_to_rad(angle)
        new_angle = start_angle + angle_offset

        x = radius * math.cos(new_angle)
        y = radius * math.sin(new_angle)
        return Point(center.x + x, center.y - y)

    def angle(self, center, radius):
        offset_point = self - center
        angle = point_to_angle(offset_point, radius)
        return angle

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, other.y - self.y)

    def __iter__(self):
        for val in (self.x, self.y):
            yield val


@dataclass
class SegmentInfo:
    label: str
    size: float


@dataclass
class Segment:
    def __init__(self, center: float, radius: float, start: Point, end: Point):
        self.center: float = center
        self.radius = radius
        self.points = self._get_points(start, end)

    def _get_points(self, p1, p2):
        # 1 point per degree
        p1_rad = p1.angle(self.center, self.radius)
        p2_rad = p2.angle(self.center, self.radius)
        if p2_rad <= p1_rad:
            p2_rad += 2 * math.pi
        p1_deg = rad_to_deg(p1_rad)
        p2_deg = rad_to_deg(p2_rad)
        if p2_deg <= p1_deg:
            p2_deg += 360
        angles = (
            [p1_rad]
            + [
                deg_to_rad(angle)
                for angle in range(math.ceil(p1_deg), math.floor(p2_deg) + 1)
            ]
            + [p2_rad]
        )
        points = [angle_to_point(angle, self.center, self.radius) for angle in angles]
        return points

    def rotate(self, angle):
        rotated_points: list[Point] = []
        for point in self.points:
            rotated_points.append(point.rotate(angle, self.radius, self.center))
        self.points = rotated_points

    def __iter__(self):
        yield tuple(self.center)
        for point in self.points:
            yield tuple(point)
