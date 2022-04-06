import pygame

class Button:
  def __init__(self, x, y, width, height, text):
    FONT = pygame.font.Font(None, 32)
    self.rect = pygame.Rect(x, y, width, height)
    self.color = (255, 255, 255)
    self.text = text
    self.text_surface = FONT.render(text, True, self.color)

  def draw(self, screen):
    screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
    pygame.draw.rect(screen, self.color, self.rect, 2)
