import pygame

from dataclasses import dataclass
from typing import List

from scene import TitleScene, SpinnerScene
from spinner import Point, EvenSpinnerFactory
from constants import *

pygame.init()

# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT = 500
# GREY = (100, 100, 100)
# SPINNER_RADIUS = min(SCREEN_WIDTH, SCREEN_HEIGHT)/4
# SEGMENTS = 16
# COLORS = ((255, 0 , 0), (0, 0, 255))

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

clock = pygame.time.Clock()

CENTER = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

def run_game(active_scene):
  spinner = None
  while active_scene:
    screen.fill(GREY)

    filtered_events = []
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        active_scene.terminate()
      else:
        filtered_events.append(event)

      # if not spinner:
      #   factory = EvenSpinnerFactory(SPINNER_RADIUS, CENTER, SEGMENTS, COLORS)
      #   spinner = factory.create_spinner()
      #   active_scene = SpinnerScene(spinner)

      active_scene.process_events(filtered_events)
    active_scene.update()
    active_scene.render(screen)

    active_scene = active_scene.next

    pygame.display.flip()
    clock.tick(60)

  pygame.quit()

title = TitleScene()

run_game(title)
