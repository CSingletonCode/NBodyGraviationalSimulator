from ui.panel import Panel
from ui.button import Button
from colours import *


class TypeDropdown:
    def __init__(self, type_box, unfreeze_nbp):
        self.panel = Panel(position=(685, 154), size=(350, 280), colour=(*NAVY, 1.0),
                           border_colour=(*CYAN, 1.0), corner_radius=0, border_size=2)
        self.types = ["Star", "Gas Giant", "Ice Giant", "Terrestrial Planet", "Dwarf Planet", "Moon", "Asteroid", "Comet"]
        self.type_box = type_box # The box the selected type will fill
        self.unfreeze_nbp = unfreeze_nbp # The function to unlock the new body panel's controls
        self.add_buttons()

    def add_buttons(self):
        """iterates through the list of types and creates a button to select each one."""
        height = 40
        count = 0
        for body_type in self.types:
            def select_type(selected=body_type):
                """Sets the label as the selected type, closes the panel and unfreezes the UI."""
                self.type_box.label = selected
                self.type_box.text_texture = None
                self.unfreeze_nbp()
                self.panel.hide()

            button = Button(position=(685, 154 + height*count), size=(350, height), purpose=select_type,
                            colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=0,
                            border_size=2, label=body_type, label_colour=(*CYAN, 1.0), enable_shadow=False)
            button.press_drop = False # Stops the button from visually pressing down.
            self.panel.add_element(button)
            count += 1