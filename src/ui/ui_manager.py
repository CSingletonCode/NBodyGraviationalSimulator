import sys
import pygame as pg

from .button import Button
from .control_panel import ControlPanel
from .panel import Panel
from assets.colours import *

class Manager:
    def __init__(self, screen_size):
        self.elements = []
        self.screen_size = screen_size

        self.create_ui()

    def create_ui(self):
        self.show_controls_button = Button(
            position=(2390, 20),
            size=(150, 60),
            purpose=None,
            colour=(1.0, 1.0, 1.0, 1.0),
            border_colour=(0, 0, 0, 1.0),
            corner_radius=7,
            border_size=2,
            label="Show Controls",
            label_colour=(0, 0, 0, 1.0),
            enable_shadow=True
        )

        self.control_panel = ControlPanel(self.show_controls_button)
        self.show_controls_button.purpose = self.control_panel.show_controls
        self.show_controls_button.disable()

        self.elements.append(self.control_panel.panel)
        self.elements.append(self.show_controls_button)

    def quit(self):
        pg.quit()
        sys.exit()

    def update_elements(self, mouse_position):
        for element in self.elements:
            element.update(mouse_position)

    def handle_event(self, event):
        for element in self.elements:
            element.handle_event(event)

    def render(self, renderer):
        for element in self.elements:
            if element.visible:
                element.draw(renderer)