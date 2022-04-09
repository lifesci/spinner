import pygame

class Button:
  def __init__(self, x, y, width, height, text, next_scene=None):
    FONT = pygame.font.Font(None, 32)
    self.rect = pygame.Rect(x, y, width, height)
    self.color = (255, 255, 255)
    self.text = text
    self.text_surface = FONT.render(text, True, self.color)
    self.next_scene = next_scene

  def draw(self, screen):
    screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
    pygame.draw.rect(screen, self.color, self.rect, 2)

class TextInput(Button):
  def __init__(self, x, y, width, height):
    super().__init__(self, x, y, width, height, text)
    self.active = False
    self.text = ""

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(pos):
        self.active = True

    if self.active and event.type == pygame.KEYDOWN:
      if event.key == pygame.K_BACKSPACE:
        self.text = self.text[:-1]
      else:
        self.text += event.unicode

  def _set_text_surface(self):
    self.text_surface = FONT.render(self.text, True, self.color)

  def draw(self, screen):
    self._set_text_surface()
    screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
    pygame.draw.rect(screen, self.color, self.rect, 2)
