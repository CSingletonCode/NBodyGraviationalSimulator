from .button import Button
from .control_panel import ControlPanel
from .new_body_panel import NewBodyPanel
from assets.colours import *
import pygame as pg

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
        self.control_panel.new_body_button.purpose = self.new_body

        self.new_body_panel = NewBodyPanel()
        self.elements.append(self.new_body_panel.panel)
        #self.new_body_panel.panel.hide()

        self.elements.append(self.control_panel.panel)
        self.elements.append(self.show_controls_button)

    def new_body(self):
        self.new_body_panel.panel.show()

    def get_all_elements(self):
        temp = []
        for element in self.elements:
            temp.append(element)
            if hasattr(element, "contains"):
                temp.extend(element.contains)
        return temp

    def update_elements(self, mouse_position):
        for element in self.elements:
            element.update(mouse_position)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for element in self.get_all_elements():
                if hasattr(element, "focused"):
                    if element.hovered:
                        element.focused = True
                    else:
                        element.focused = False

        if event.type == pg.KEYDOWN:
            for element in self.get_all_elements():
                if hasattr(element, "focused") and element.focused:
                    if hasattr(element, "write"):
                        element.write(event)

        for element in self.get_all_elements():
            element.handle_event(event)



    def render(self, renderer):
        for element in self.elements:
            if element.visible:
                element.draw(renderer)