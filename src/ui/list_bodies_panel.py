from functools import partial

from ui.button import Button
from ui.panel import Panel
from ui.textbox import TextBox
from colours import *


class ListBodiesPanel:
    def __init__(self, simulation, camera):
        self.panel = Panel(position=(10, 360), size=(355, 720), colour=(*SILVER, 1.0),
                        border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)
        self.simulation = simulation
        self.camera = camera
        # The first and last indices of the bodies currently being displayed.
        self.top = 0
        self.bottom = 2

        self.slots = {}
        self.add_buttons()
        self.create_panel_slots()
        self.show_bodies_panels()
        self.panel.hide()

    def refresh(self):
        """Recreates the panel when a body is added or removed."""
        self.panel.clear()
        self.add_buttons()
        self.create_panel_slots()
        self.show_bodies_panels()

    def add_buttons(self):
        """Adds the buttons to navigate the list."""
        self.previous_button = Button(position=(20, 370), size=(335, 50), purpose=self.move_back, colour=(*NAVY, 1.0),
                                    border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="PREVIOUS",
                                    label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.previous_button)
        self.next_button = Button(position=(20, 1020), size=(335, 50), purpose=self.move_forward, colour=(*NAVY, 1.0),
                                    border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="NEXT",
                                    label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.next_button)

    def create_panel_slots(self):
        """Creates the three panels and their features so the values from the bodies to be displayed can fill them."""
        self.slots = []
        for i in range(3):
            body_panel = Panel(position=(20, 425+(i*200)), size=(335, 195), colour=(*SILVER, 1.0),
                               border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)

            # Moves the camera to the body
            goto_button = Button(position=(30, 565+(i*200)), size=(72, 40), purpose=None, colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label="Go To",
                              label_colour=(*CYAN, 1.0), enable_shadow=True)
            body_panel.add_element(goto_button)

            # Removes the body
            delete_button = Button(position=(107, 565+(i*200)), size=(72, 40), purpose=None, colour=(*NAVY, 1.0),
                               border_colour=(*RED, 1.0), corner_radius=5, border_size=2, label="Delete",
                               label_colour=(*RED, 1.0), enable_shadow=True)
            body_panel.add_element(delete_button)

            # Empties the stored orbit trail for the body.
            clear_trail_button = Button(position=(184, 565+(i*200)), size=(84, 40), purpose=None, colour=(*NAVY, 1.0),
                               border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label="Wipe Trail",
                               label_colour=(*CYAN, 1.0), enable_shadow=True)
            body_panel.add_element(clear_trail_button )

            # displays the stored path the body has travelled as a white line.
            trail_button = Button(position=(273, 565+(i*200)), size=(72, 40), purpose=None, colour=(*NAVY, 1.0),
                               border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label="Trail",
                               label_colour=(*CYAN, 1.0), enable_shadow=True)
            body_panel.add_element(trail_button)

            # Creates 5 text boxes for displaying the bodies attributes.
            text_boxes = []
            for j in range(5):
                blank_box = TextBox(position=(25, 435+(i*200)+(j*22)), size=(325, 20), colour=(*SILVER, 1.0),
                             border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                             label_colour=(*BLACK, 1.0), writable=False, label="")
                body_panel.add_element(blank_box)
                text_boxes.append(blank_box)

            self.panel.add_element(body_panel)

            # Stores references to each element.
            self.slots.append ({
                "panel": body_panel,
                "text": text_boxes,
                "goto": goto_button,
                "delete": delete_button,
                "clear trail": clear_trail_button,
                "trail": trail_button
            })

    def show_bodies_panels(self):
        """Selects the three correct elements from the list and sets their attributes to be displayed."""
        for i in range(3):
            index = self.top + i
            slot = self.slots[i]

            if index < len(self.simulation.bodies):
                body = self.simulation.bodies[index]

                def remove_body(to_remove = body):
                    self.simulation.bodies.remove(to_remove)
                    self.refresh()

                slot["text"][0].label = f"Name: {body.name}"
                slot["text"][0].text_texture = None
                slot["text"][1].label = f"Type: {body.body_type}"
                slot["text"][1].text_texture = None
                slot["text"][2].label = f"Radius: {body.radius}"
                slot["text"][2].text_texture = None
                slot["text"][3].label = f"Density: {body.density}"
                slot["text"][3].text_texture = None
                slot["text"][4].label = f"Rotation Period: {body.r_period}"
                slot["text"][4].text_texture = None
                slot["goto"].purpose = partial(self.camera.lock_on_body, body) # Calls the function to lock the cameras movement to the chosen body.
                slot["delete"].purpose = remove_body
                slot["clear trail"].purpose = body.clear_trail
                slot["trail"].purpose = body.toggle_trail
                slot["panel"].show()
            else:
                slot["panel"].hide()

    def move_back(self):
        """Decrements the indices so the list panel moves back a page."""
        self.top = max(0, self.top - 3)
        self.bottom = min(len(self.simulation.bodies) - 1, self.top + 2)
        self.show_bodies_panels()

    def move_forward(self):
        """Increments the indices so the list panel moves forwards a page."""
        if self.top + 3 < len(self.simulation.bodies):
            self.top += 3
            self.bottom = min(len(self.simulation.bodies) - 1, self.top + 2)
            self.show_bodies_panels()
