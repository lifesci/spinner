import pygame
from button import Button
from spinner import Point, EvenSpinnerFactory
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPINNER_RADIUS, SEGMENTS, COLORS

class SceneBase:
  def __init__(self):
    self.next = self

  def process_events(self, events):
    raise NotImplementedError

  def update(self):
    raise NotImplementedError

  def render(self, screen):
    raise NotImplementedError

  def switch_to_scene(self, next_scene):
    self.next = next_scene

  def terminate(self):
    self.switch_to_scene(None)

class TitleScene(SceneBase):
  def __init__(self):
    SceneBase.__init__(self)
    screen_w, screen_h = pygame.display.get_surface().get_size()
    width = 200
    height = 75
    buff = 15
    center = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    spinner_factory = EvenSpinnerFactory(SPINNER_RADIUS, center, SEGMENTS, COLORS)
    spinner = spinner_factory.create_spinner()
    button_info = {
      "QUICK START": SpinnerScene(spinner),
      "CUSTOM": None,
      "LOAD": None
    }
    step = height + buff
    self.buttons = []
    i = 0
    for text, next_scene in button_info.items():
      button = Button((screen_w - width)/2, screen_h/4 + i*step, width, height, text, next_scene)
      self.buttons.append(button)
      i += 1

  def process_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
          if button.rect.collidepoint(pos):
            print("switch")
            self.switch_to_scene(button.next_scene)
  
  def update(self):
    pass

  def render(self, screen):
    for button in self.buttons:
      button.draw(screen)

class SpinnerScene(SceneBase):
  def __init__(self, spinner):
    SceneBase.__init__(self)
    self.spinner = spinner

  def process_events(self, events):
    pass

  def update(self):
    self.spinner.rotate(1/30)

  def render(self, screen):
    self.spinner.draw(screen)
