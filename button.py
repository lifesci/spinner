import pygame


class Button:
    def __init__(self, x, y, width, height, text, scene, next_scene):
        font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)
        self.text = text
        self.text_surface = font.render(text, True, self.color)
        self.scene = scene
        self.next_scene = next_scene

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def _clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            return self.rect.collidepoint(pos)
        return False

    def _clicked_away(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            return not self.rect.collidepoint(pos)
        return False

    def process_event(self, event, scene):
        if self._clicked(event):
            scene.switch_to_scene(self.next_scene)


class Input(Button):
    def __init__(self, x, y, width, height, text, scene, next_scene):
        super().__init__(x, y, width, height, text, scene, next_scene)
        self.active = False
        self.active_color = (255, 0, 0)
        self.text = ""
        self.font = pygame.font.Font(None, 32)

    def _validate_input(self, value):
        return True

    def process_event(self, event, scene):
        if self._clicked(event):
            self.active = True

        if self._clicked_away(event):
            self.active = False

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self._validate_input(self.text + event.unicode):
                self.text += event.unicode

    def _set_text_surface(self):
        self.text_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        self._set_text_surface()
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        color = self.active_color if self.active else self.color
        pygame.draw.rect(screen, color, self.rect, 2)


class NumericInput(Input):
    def _validate_input(self, value):
        try:
            return value.isdigit() and int(value) > 0 and int(value) <= 100
        except ValueError:
            return False
