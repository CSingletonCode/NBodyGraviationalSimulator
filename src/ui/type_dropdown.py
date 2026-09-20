from ui.panel import Panel
from ui.button import Button
from colours import *


class TypeDropdown:
    def __init__(self, type_box, unfreeze_nbp):
        self.panel = Panel(position=(685, 154), size=(350, 280), colour=(*NAVY, 1.0),
                           border_colour=(*CYAN, 1.0), corner_radius=0, border_size=2)
        self.types=["Terrestrial Planet", "Gas Giant", "Ice Giant", "Moon", "Dwarf Planet", "Asteroid", "Comet"]
        self.type_box = type_box
        self.unfreeze_nbp = unfreeze_nbp
        self.add_buttons()

    def add_buttons(self):
        height = 40
        count = 0
        for body_type in self.types:
            def select_type(selected=body_type):
                self.type_box.label = selected
                self.type_box.text_texture = None
                self.unfreeze_nbp()
                self.panel.hide()

            button = Button(position=(685, 154 + height*count), size=(350, height), purpose=select_type,
                            colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=0,
                            border_size=2, label=body_type, label_colour=(*CYAN, 1.0), enable_shadow=False)
            button.press_drop = False
            self.panel.add_element(button)
            count += 1