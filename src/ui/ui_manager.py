from .button import Button
from .control_panel import ControlPanel
from .new_body_panel import NewBodyPanel
from assets.colours import *
import pygame as pg

from .panel import Panel
from .textbox import TextBox
from .type_dropdown import TypeDropdown

class Manager:
    def __init__(self, screen_size, simulation):
        self.elements = []
        self.screen_size = screen_size
        self.simulation = simulation
        self.create_ui()

    def create_ui(self):
        self.show_controls_button = Button(
            position=(2390, 20),
            size=(150, 60),
            purpose=None,
            colour=(*NAVY, 1.0),
            border_colour=(*CYAN, 1.0),
            corner_radius=7,
            border_size=2,
            label="Show Controls",
            label_colour=(*CYAN, 1.0),
            enable_shadow=False
        )

        self.control_panel = ControlPanel(self.show_controls_button)
        self.show_controls_button.purpose = self.control_panel.show_controls
        self.show_controls_button.disable()
        self.control_panel.new_body_button.purpose = self.new_body

        self.make_invalid()

        self.new_body_panel = NewBodyPanel(self.control_panel.panel.unfreeze, self.invalid_data, self.simulation)
        self.new_body_panel.type_box.purpose = self.show_types_dropdown
        self.new_body_panel.panel.hide()

        self.acknowledge.purpose = self.remove_invalid

        self.type_dropdown = TypeDropdown(self.new_body_panel.type_box, self.new_body_panel.panel.unfreeze)
        self.type_dropdown.panel.hide()

        self.elements.append(self.control_panel.panel)
        self.elements.append(self.show_controls_button)
        self.elements.append(self.new_body_panel.panel)
        self.elements.append(self.type_dropdown.panel)
        self.elements.append(self.invalid_data)

    def make_invalid(self):
        self.invalid_data = Panel(position=(980, 100), size=(600, 300), colour=(*SILVER, 1.0),
                        border_colour=(*RED, 1.0), corner_radius=10, border_size=5)
        self.error_title = TextBox(
            position=(1155, 150), size=(250, 50), colour=(*SILVER, 1.0), border_colour=(*SILVER, 1.0),
            corner_radius=5, border_size=2,label_colour=(*BLACK, 1.0), writable=False, label="INVALID DATA ENTRY",
        )
        self.invalid_data.add_element(self.error_title)
        self.error_message = TextBox(
            position=(1030, 220), size=(500, 40), colour=(*SILVER, 1.0), border_colour=(*SILVER, 1.0),
            corner_radius=5, border_size=2, label_colour=(*BLACK, 1.0), writable=False,
            label="All mathematical values must be numbers.",
        )
        self.invalid_data.add_element(self.error_message)
        self.acknowledge = Button(position=(1205, 330), size=(150, 50), purpose=None, colour=(*NAVY, 1.0),
            border_colour=(*RED, 1.0), corner_radius=7, border_size=2,
            label="OK", label_colour=(*RED, 1.0), enable_shadow=True)
        self.invalid_data.add_element(self.acknowledge)
        self.invalid_data.hide()

    def remove_invalid(self):
        self.invalid_data.hide()
        self.new_body_panel.panel.unfreeze()

    def show_types_dropdown(self):
        self.new_body_panel.panel.freeze()
        self.type_dropdown.panel.show()

    def new_body(self):
        self.new_body_panel.panel.show()
        self.control_panel.panel.freeze()
        self.control_panel.quit_button.unfreeze()

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

    def new_body_panel_state(self):
        return self.new_body_panel.panel.interactable()
