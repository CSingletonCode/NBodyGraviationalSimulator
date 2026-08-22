from ui.button import Button
from ui.panel import Panel
from ui.textbox import TextBox


class NewBodyPanel:
    def __init__(self):
        self.panel = Panel(position=(640, 10), size=(1280, 225), colour=(1.0, 1.0, 1.0, 1.0),
                        border_colour=(0, 0, 0, 1.0), corner_radius=10, border_size=5)
        self.add_features()

    def add_features(self):
        self.name_label = TextBox(position=(650, 20), size=(100, 20), colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(1.0, 1.0, 1.0, 1.0), corner_radius=0, border_size=0,
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=False, writable=False, label="Enter Name:")
        self.panel.add_element(self.name_label)
        self.name_box = TextBox(position=(650, 42), size=(150, 60), colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2,
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True, writable=True)
        self.panel.add_element(self.name_box)
