import pygame
from button import Button, Input, NumericInput
from spinner import Point, SpinnerFactory
from helpers import get_menu_positions
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CENTER,
    SPINNER_RADIUS,
    SEGMENTS,
    COLORS,
)
from geom import SegmentInfo


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
                button.process_event(event, self)

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
        self.buttons = []
        screen_w, screen_h = pygame.display.get_surface().get_size()
        button_info = [
            ("Option Name", {"next": self, "cons": Button}),
            ("Option Size", {"next": self, "cons": Button}),
            ("", {"next": self, "cons": Input}),
            ("50", {"next": self, "cons": NumericInput}),
            ("", {"next": self, "cons": Input}),
            ("50", {"next": self, "cons": NumericInput}),
            ("Create", {"next": self, "cons": Button}),
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

        self.create_button = self.buttons[-1]

    def process_events(self, events):
        MenuScene.process_events(self, events)
        spinner_scene = self._build_spinner_scene()
        self.create_button.next_scene = spinner_scene

    def _build_spinner_scene(self):
        segment_info = []
        i = 0
        try:
            for inp in self.buttons[2:-1]:
                if i % 2 == 0:
                    label = inp.text
                else:
                    size = int(inp.text) / 100
                    segment_info.append(SegmentInfo(label, size))
                i += 1
            total_size = sum(info.size for info in segment_info)
            if total_size == 1:
                spinner_factory = SpinnerFactory(
                    SPINNER_RADIUS, CENTER, segment_info, COLORS
                )
                spinner = spinner_factory.create_spinner()
                scene = SpinnerScene(spinner)
                return scene
            else:
                return self
        except ValueError:
            return self


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
        self.spinner.rotate(1 / 360)

    def render(self, screen):
        self.spinner.draw(screen)
