import pygame
from button import Button, Input, NumericInput
from spinner import Point, EvenSpinnerFactory
from helpers import get_menu_positions
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


class MenuScene(SceneBase):
    def process_events(self, events):
        for event in events:
            for button in self.buttons:
                next_scene = button.process_event(event)
                if next_scene:
                    self.switch_to_scene(next_scene)

    def update(self):
        pass

    def render(self, screen):
        for button in self.buttons:
            button.draw(screen)


class TitleScene(MenuScene):
    def __init__(self):
        MenuScene.__init__(self)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        button_info = [("CREATE", CreateScene()), ("LOAD", self)]
        positions = get_menu_positions(0, 0, screen_w, screen_h, len(button_info))
        self.buttons = []
        i = 0
        for text, next_scene in button_info:
            position = positions[i]
            button = Button(
                position["x"],
                position["y"],
                position["width"],
                position["height"],
                text,
                self,
                next_scene,
            )
            self.buttons.append(button)
            i += 1


class CreateScene(MenuScene):
    def __init__(self):
        MenuScene.__init__(self)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        button_info = [
            ("Option Name", {"next": self, "cons": Button}),
            ("Option Size", {"next": self, "cons": Button}),
            ("", {"next": self, "cons": Input}),
            ("50", {"next": self, "cons": NumericInput}),
            ("", {"next": self, "cons": Input}),
            ("50", {"next": self, "cons": NumericInput}),
        ]
        positions = get_menu_positions(
            0,
            0,
            screen_w,
            screen_h,
            len(button_info),
            num_cols=2,
            proportions=[0.75, 0.25],
        )
        self.buttons = []
        i = 0
        for text, info in button_info:
            next_scene = info["next"]
            cons = info["cons"]
            position = positions[i]
            button = cons(
                position["x"],
                position["y"],
                position["width"],
                position["height"],
                text,
                self,
                next_scene,
            )
            self.buttons.append(button)
            i += 1


class SpinnerScene(SceneBase):
    def __init__(self, spinner):
        SceneBase.__init__(self)
        # width = 200
        # height = 75
        # buff = 15
        # center = Point(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        # spinner_factory = EvenSpinnerFactory(SPINNER_RADIUS, center, SEGMENTS, COLORS)
        # spinner = spinner_factory.create_spinner()
        self.spinner = spinner

    def process_events(self, events):
        pass

    def update(self):
        self.spinner.rotate(1 / 30)

    def render(self, screen):
        self.spinner.draw(screen)
