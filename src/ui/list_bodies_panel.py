from simulation.body import Body
from ui.button import Button
from ui.panel import Panel
from colours import *
from ui.textbox import TextBox


class ListBodiesPanel():
    def __init__(self, bodies):
        self.panel = Panel(position=(10, 360), size=(320, 720), colour=(*SILVER, 1.0),
                        border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)
        self.panel.hide()
        self.bodies = bodies
        self.top = 0
        self.bottom = 2
        self.slots = {}
        self.add_buttons()
        self.create_panel_slots()
        self.show_bodies_panels()

    def refresh(self):
        self.panel.clear()
        self.add_buttons()
        self.create_panel_slots()
        self.show_bodies_panels()

    def add_buttons(self):
        self.previous_button = Button(position=(20, 370), size=(300, 50), purpose=self.move_back, colour=(*NAVY, 1.0),
                                    border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="PREVIOUS",
                                    label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.previous_button)
        self.next_button = Button(position=(20, 1020), size=(300, 50), purpose=self.move_forward, colour=(*NAVY, 1.0),
                                    border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="NEXT",
                                    label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.next_button)

    def create_panel_slots(self):
        self.slots = []
        for i in range(3):
            body_panel = Panel(position=(20, 425+(i*200)), size=(300, 195), colour=(*SILVER, 1.0),
                               border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)

            goto_button = Button(position=(30, 565+(i*200)), size=(100, 40), purpose=None, colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label="Go To",
                              label_colour=(*CYAN, 1.0), enable_shadow=True)
            body_panel.add_element(goto_button)

            trail_button = Button(position=(210, 565+(i*200)), size=(100, 40), purpose=None, colour=(*NAVY, 1.0),
                               border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label="Trail",
                               label_colour=(*CYAN, 1.0), enable_shadow=True)
            body_panel.add_element(trail_button)

            text_boxes = []
            for j in range(6):
                blank_box = TextBox(position=(25, 435+(i*200)+(j*22)), size=(290, 20), colour=(*SILVER, 1.0),
                             border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                             label_colour=(*BLACK, 1.0), writable=False, label="")
                body_panel.add_element(blank_box)
                text_boxes.append(blank_box)

            self.panel.add_element(body_panel)

            self.slots.append ({
                "panel": body_panel,
                "text": text_boxes,
                "goto": goto_button,
                "trail": trail_button
            })

    def show_bodies_panels(self):
        for i in range(3):
            index = self.top + i
            slot = self.slots[i]

            if index < len(self.bodies):
                body = self.bodies[index]

                slot["text"][0].label = f"Name: {body.name}"
                slot["text"][0].text_texture = None
                slot["text"][1].label = f"Type: {body.body_type}"
                slot["text"][1].text_texture = None
                if body.parent is not None and not isinstance(body.parent, str):
                    slot["text"][2].label = f"Parent: {body.parent.name}"
                else:
                    slot["text"][2].label = "Parent: None"
                slot["text"][2].text_texture = None
                slot["text"][3].label = f"Radius: {body.radius}"
                slot["text"][3].text_texture = None
                slot["text"][4].label = f"Density: {body.density}"
                slot["text"][4].text_texture = None
                slot["text"][5].label = f"Rotation Period: {body.r_period}"
                slot["text"][5].text_texture = None
                slot["goto"].purpose = None
                slot["trail"].purpose = None
                slot["panel"].show()
            else:
                slot["panel"].hide()

    def move_back(self):
        self.top = max(0, self.top - 3)
        self.bottom = min(len(self.bodies) - 1, self.top + 2)
        self.show_bodies_panels()

    def move_forward(self):
        if self.top + 3 < len(self.bodies):
            self.top += 3
            self.bottom = min(len(self.bodies) - 1, self.top + 2)
            self.show_bodies_panels()
