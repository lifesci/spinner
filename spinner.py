# spinner

import math
import pygame

from dataclasses import dataclass
from typing import List

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
GREY = (100, 100, 100)
SPINNER_RADIUS = min(SCREEN_WIDTH, SCREEN_HEIGHT)/4
SEGMENTS = 16
COLORS = ((255, 0 , 0), (0, 0, 255))

def pct_to_rad(pct):
  return 2*math.pi*pct

@dataclass
class Point:
  x:float
  y:float

  def rotate(self, angle, radius, center):
    x_offset = self.x - center.x
    y_offset = center.y - self.y

    acos = math.acos(x_offset/radius)
    asin = math.asin(y_offset/radius)

    if y_offset > 0:
      start_angle = acos
    else:
      start_angle = 2*math.pi - acos

    angle_offset = pct_to_rad(angle)
    new_angle = start_angle + angle_offset

    x = radius*math.cos(new_angle)
    y = radius*math.sin(new_angle)
    return Point(center.x + x, center.y - y)

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __iter__(self):
    for val in (self.x, self.y):
      yield val

def add_point(*points):
  return sum(points, Point(0, 0))

@dataclass
class Triangle:
  def __init__(self, center:float, p1:Point, p2:Point):
    self.center:float = center
    self.points:tuple[Point] = (p1, p2)

  def rotate(self, angle, radius):
    points:list[Point] = []
    for point in self.points:
      points.append(point.rotate(angle, radius, self.center))
    triangle = Triangle(self.center, *points)
    return triangle

  def __iter__(self):
    yield tuple(self.center)
    for point in self.points:
      yield tuple(point)

class Spinner:
  def __init__(self, surface:pygame.Surface, radius:float, center:Point, triangles:List[Triangle], colors:List[int]):
    self.triangles: list[Triangle] = triangles
    self.radius = radius
    self.center = center
    self.colors = colors
    self.num_colors = len(colors)
    self.surface = surface

  def draw(self):
    i = 0
    for triangle in self.triangles:
      pygame.draw.polygon(self.surface, color=self.colors[i%self.num_colors], points=tuple(triangle))
      i += 1

  def rotate(self, angle):
    rotated:list[Triangle] = []
    for triangle in self.triangles:
      rotated.append(triangle.rotate(angle, self.radius))
    self.triangles = rotated

class EvenSpinnerFactory:
  def __init__(self, surface, radius, center, segments, colors):
    self.surface = surface
    self.center = center
    self.radius = radius
    self.segments = segments
    self.colors = colors

  def _get_next_triangle(self, used, size):
    start_angle = pct_to_rad(used)

    p1x = self.radius*math.cos(start_angle)
    p1y = -self.radius*math.sin(start_angle)
    p1_offset = Point(p1x, p1y)
    p1 = add_point(self.center, p1_offset)

    end_angle = pct_to_rad(used + size)
    p2x = self.radius*math.cos(end_angle)
    p2y = -self.radius*math.sin(end_angle)
    p2_offset = Point(p2x, p2y)
    p2 = add_point(self.center, p2_offset)

    return Triangle(self.center, p1, p2)

  def create_spinner(self):
    triangles = []
    used = 0
    size = 1/self.segments
    for i in range(self.segments):
      triangle = self._get_next_triangle(used, size)
      triangles.append(triangle)
      used += size
    return Spinner(self.surface, self.radius, self.center, triangles, self.colors)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

running = True
clock = pygame.time.Clock()

spinner = None

CENTER = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

while running:
  screen.fill(GREY)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif spinner:
      spinner.rotate(1/30)

    if not spinner:
      factory = EvenSpinnerFactory(screen, SPINNER_RADIUS, CENTER, SEGMENTS, COLORS)
      spinner = factory.create_spinner()

    spinner.draw()

    pygame.display.flip()

pygame.quit()
