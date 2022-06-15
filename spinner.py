import math
import pygame

from dataclasses import dataclass
from typing import List

from geom import *


class Spinner:
    def __init__(
        self, radius: float, center: Point, triangles: List[Segment], colors: List[int]
    ):
        self.triangles: list[Segment] = triangles
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
            pygame.draw.polygon(
                surface, color=self.colors[i % self.num_colors], points=tuple(triangle)
            )
            i += 1

    def rotate(self, angle):
        for triangle in self.triangles:
            triangle.rotate(angle)


class SpinnerFactory:
    def __init__(self, radius, center, segment_info, colors):
        self.center = center
        self.radius = radius
        self.segment_info = segment_info
        self.colors = colors

    def _get_next_triangle(self, used, size):
        start_angle = pct_to_rad(used)

        p1x = self.radius * math.cos(start_angle)
        p1y = -self.radius * math.sin(start_angle)
        p1_offset = Point(p1x, p1y)
        p1 = self.center + p1_offset

        end_angle = pct_to_rad(used + size)
        p2x = self.radius * math.cos(end_angle)
        p2y = -self.radius * math.sin(end_angle)
        p2_offset = Point(p2x, p2y)
        p2 = self.center + p2_offset

        return Segment(self.center, self.radius, p1, p2)

    def create_spinner(self):
        triangles = []
        used = 0
        for info in self.segment_info:
            size = info.size
            triangle = self._get_next_triangle(used, size)
            triangles.append(triangle)
            used += size
        return Spinner(self.radius, self.center, triangles, self.colors)
