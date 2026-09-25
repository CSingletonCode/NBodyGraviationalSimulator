from constants import WIDTH_SCALE, HEIGHT_SCALE
from ui.button import Button
from ui.panel import Panel
from colours import *

class Parent_dropdown:
    def __init__(self, bodies, parent_box, unfreeze_nbp):
        self.bodies = bodies
        self.parent_box = parent_box
        self.unfreeze_nbp = unfreeze_nbp
        self.panel = Panel(position=(685, 226), size=(350, 40*(len(self.bodies)+1)), colour=(*NAVY, 1.0),
                           border_colour=(*CYAN, 1.0), corner_radius=0, border_size=2)
        self.selected = None
        self.add_buttons()

    def refresh(self):
        self.panel.size = (350*WIDTH_SCALE, (40*(len(self.bodies)+1))*HEIGHT_SCALE)
        self.panel.clear()
        self.add_buttons()

    def add_buttons(self):
        for i, body in enumerate(self.bodies):
            def pick_parent(parent=body):
                self.parent_box.label = parent.name
                self.selected = parent
                self.parent_box.text_texture = None
                self.unfreeze_nbp()
                self.panel.hide()
            button = Button(position=(685, 226 + i*40), size=(350, 40), purpose=pick_parent,
                            colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=0,
                            border_size=2, label=body.name, label_colour=(*CYAN, 1.0), enable_shadow=False)
            button.press_drop = False
            self.panel.add_element(button)

        def set_none():
            self.parent_box.label = "None"
            self.parent_box.text_texture = None
            self.unfreeze_nbp()
            self.panel.hide()

        button_none = Button(position=(685, 226 + len(self.bodies) * 40), size=(350, 40), purpose=set_none,
                        colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=0,
                        border_size=2, label="None", label_colour=(*CYAN, 1.0), enable_shadow=False)
        button_none.press_drop = False
        self.panel.add_element(button_none)