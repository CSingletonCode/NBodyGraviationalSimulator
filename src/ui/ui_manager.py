import pygame as pg
from .button import Button
from .control_panel import ControlPanel
from .list_bodies_panel import ListBodiesPanel
from .new_body_panel import NewBodyPanel
from colours import *
from .panel import Panel
from .parent_dropdown import ParentDropdown
from .preset_dropdown import PresetDropdown
from .textbox import TextBox
from .type_dropdown import TypeDropdown

class Manager:
    def __init__(self, screen_size, simulation, camera):
        self.elements = []
        self.screen_size = screen_size
        self.simulation = simulation
        self.camera = camera
        self.paused = False
        self.create_ui()

    def create_ui(self):
        # The button that's revealed when the control panel is hidden
        self.show_controls_button = Button(position=(2390, 20), size=(150, 60), purpose=None, colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=7,
                                           border_size=2, label="Show Controls", label_colour=(*CYAN, 1.0), enable_shadow=False)

        # The control panel, handles the different UI features and simulation controls such as speeding up and pausing.
        self.control_panel = ControlPanel(self.show_controls_button, self.simulation)
        self.show_controls_button.purpose = self.show_controls
        self.show_controls_button.disable() # Hides the button until it's needed.
        self.control_panel.new_body_button.purpose = self.new_body # Shows a panel for adding a new body.
        self.control_panel.list_bodies_button.purpose = self.list_bodies # Shows a panel with a list of the active bodies.
        self.control_panel.toggle_radius_button.purpose = lambda *args: (self.simulation.toggle_proportional_radius(), self.camera.toggle_proportional_radius()) # Switches between proportional and capped radii.
        self.control_panel.clear_button.purpose = self.clear_bodies # Clears the list of bodies in the simulation.

        self.bodies_list = ListBodiesPanel(self.simulation, self.camera) # Panel for containing the list of bodies

        self.make_invalid()

        self.new_body_panel = NewBodyPanel(self.unfreeze_everything, self.invalid_data, self.simulation, self.retrieve_parent, self.bodies_list.refresh)
        self.preset_dropdown = PresetDropdown(self.new_body_panel)
        self.new_body_panel.type_box.purpose = self.show_types_dropdown
        self.new_body_panel.parent_box.purpose = self.show_parents_dropdown
        self.new_body_panel.preset_button.purpose = self.show_presets_dropdown
        self.new_body_panel.panel.hide()

        self.acknowledge.purpose = self.remove_invalid

        self.type_dropdown = TypeDropdown(self.new_body_panel.type_box, self.new_body_panel.panel.unfreeze) # Dropdown panel with a list of available types for bodies
        self.type_dropdown.panel.hide()

        self.parent_dropdown = ParentDropdown(self.simulation.bodies, self.new_body_panel.parent_box, self.new_body_panel.panel.unfreeze) # Dropdown panel containing all active bodies
        self.parent_dropdown.panel.hide()

        self.elements.append(self.control_panel.panel)
        self.elements.append(self.show_controls_button)
        self.elements.append(self.new_body_panel.panel)
        self.elements.append(self.type_dropdown.panel)
        self.elements.append(self.parent_dropdown.panel)
        self.elements.append(self.preset_dropdown.panel)
        self.elements.append(self.invalid_data)
        self.elements.append(self.bodies_list.panel)

    def show_controls(self):
        self.control_panel.panel.show()
        self.show_controls_button.disable()

    def make_invalid(self):
        """Creates a popup panel for displaying an error message."""
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

    def show_parents_dropdown(self):
        self.new_body_panel.panel.freeze()
        self.parent_dropdown.refresh()
        self.parent_dropdown.panel.show()

    def show_presets_dropdown(self):
        self.new_body_panel.panel.freeze()
        self.preset_dropdown.panel.show()

    def new_body(self):
        """Displays the new body panel and locks out all other UI elements."""
        self.new_body_panel.panel.show()
        self.control_panel.panel.freeze()
        self.bodies_list.panel.freeze()
        self.control_panel.quit_button.unfreeze()

    def get_all_elements(self, elements=None):
        """Flattens all elements and any child elements into a single list."""
        if elements is None:
            elements = self.elements
        temp = []
        for element in elements:
            temp.append(element)
            if hasattr(element, "contains"):
                temp.extend(self.get_all_elements(element.contains))
        return temp

    def update_elements(self, mouse_position):
        for element in self.elements:
            element.update(mouse_position)

    def handle_event(self, event):
        """Passes user events to the correct elements, splits them into 3 groups, mouse buttons, keys and everything else."""
        # Sets the focussed element if one has been clicked with a LMB press.
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for element in self.get_all_elements():
                if hasattr(element, "focused"):
                    element.focused = element.hovered

        # Sends all keyboard inputs straight to any textboxes first.
        if event.type == pg.KEYDOWN:
            for element in self.get_all_elements():
                if hasattr(element, "focused") and element.focused:
                    if hasattr(element, "write"):
                        element.write(event)

        # Sends all events to each element.
        for element in self.get_all_elements():
            element.handle_event(event)

    def render(self, renderer):
        """Renders each UI feature on the screen."""
        for element in self.elements:
            if element.visible:
                element.draw(renderer)

    def new_body_panel_state(self):
        return self.new_body_panel.panel.interactable()

    def list_bodies(self):
        """Shows or hides the list of bodies, resets the list to the first page when it opens."""
        if self.bodies_list.panel.visible:
            self.bodies_list.panel.hide()
        else:
            self.bodies_list.panel.show()
            self.bodies_list.top = 0
            self.bodies_list.show_bodies_panels()

    def unfreeze_everything(self):
        """Unlocks all controls."""
        self.control_panel.panel.unfreeze()
        self.bodies_list.panel.unfreeze()

    def get_speed_index(self):
        """Gets the user's speed selection."""
        return self.control_panel.speed_index

    def get_pause_state(self):
        return self.control_panel.paused

    def retrieve_parent(self):
        """Gets the selected parent from the parent dropdown in the new body panel."""
        return self.parent_dropdown.selected

    def clear_bodies(self):
        self.simulation.bodies.clear()
        self.bodies_list.refresh()