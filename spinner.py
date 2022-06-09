import math
import pygame

from dataclasses import dataclass
from typing import List


def pct_to_rad(pct):
    return 2 * math.pi * pct


def point_to_angle(point, radius):
    acos = math.acos(point.x / radius)

    if point.y > 0:
        angle = acos
    else:
        angle = 2 * math.pi - acos

    return angle


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

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, other.y - self.y)

    def __iter__(self):
        for val in (self.x, self.y):
            yield val


def add_point(*points):
    return sum(points, Point(0, 0))


@dataclass
class Triangle:
    def __init__(self, center: float, p1: Point, p2: Point):
        self.center: float = center
        self.points: tuple[Point] = (p1, p2)

    def rotate(self, angle, radius):
        points: list[Point] = []
        for point in self.points:
            points.append(point.rotate(angle, radius, self.center))
        triangle = Triangle(self.center, *points)
        return triangle

    def __iter__(self):
        yield tuple(self.center)
        for point in self.points:
            yield tuple(point)


class Spinner:
    def __init__(
        self, radius: float, center: Point, triangles: List[Triangle], colors: List[int]
    ):
        self.triangles: list[Triangle] = triangles
        self.radius = radius
        self.center = center
        self.colors = colors
        self.num_colors = len(colors)

        left = center.x - radius
        top = center.y - radius
        width = 2 * radius
        height = 2 * radius
        self.rect = pygame.Rect(left, top, width, height)

    def draw(self, surface):
        i = 0
        for triangle in self.triangles:
            # pygame.draw.polygon(
            #     surface, color=self.colors[i % self.num_colors], points=tuple(triangle)
            # )
            p1 = triangle.points[0]
            p2 = triangle.points[1]
            color = self.colors[i % self.num_colors]
            pygame.draw.line(
                surface,
                color=color,
                start_pos=tuple(self.center),
                end_pos=tuple(p1),
            )
            pygame.draw.line(
                surface,
                color=color,
                start_pos=tuple(self.center),
                end_pos=tuple(p2),
            )

            p1_offset = p1 - self.center
            p2_offset = p2 - self.center
            p1_angle = point_to_angle(p1_offset, self.radius)
            p2_angle = point_to_angle(p2_offset, self.radius)
            pygame.draw.arc(
                surface,
                color=color,
                rect=self.rect,
                start_angle=p1_angle,
                stop_angle=p2_angle,
            )
            i += 1

    def rotate(self, angle):
        rotated: list[Triangle] = []
        for triangle in self.triangles:
            rotated.append(triangle.rotate(angle, self.radius))
        self.triangles = rotated


class EvenSpinnerFactory:
    def __init__(self, radius, center, segments, colors):
        self.center = center
        self.radius = radius
        self.segments = segments
        self.colors = colors

    def _get_next_triangle(self, used, size):
        start_angle = pct_to_rad(used)

        p1x = self.radius * math.cos(start_angle)
        p1y = -self.radius * math.sin(start_angle)
        p1_offset = Point(p1x, p1y)
        p1 = add_point(self.center, p1_offset)

        end_angle = pct_to_rad(used + size)
        p2x = self.radius * math.cos(end_angle)
        p2y = -self.radius * math.sin(end_angle)
        p2_offset = Point(p2x, p2y)
        p2 = add_point(self.center, p2_offset)

        return Triangle(self.center, p1, p2)

    def create_spinner(self):
        triangles = []
        used = 0
        size = 1 / self.segments
        for i in range(self.segments):
            triangle = self._get_next_triangle(used, size)
            triangles.append(triangle)
            used += size
        return Spinner(self.radius, self.center, triangles, self.colors)
