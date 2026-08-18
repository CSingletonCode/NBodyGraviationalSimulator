from ui.button import Button
from ui.panel import Panel


class ControlPanel:
    def __init__(self, scb):
        self.panel = Panel(position=(2150, 10), size=(400, 256), colour=(1.0, 1.0, 1.0, 1.0),
                        border_colour=(0, 0, 0, 1.0), corner_radius=10, border_size=5)
        self.show_controls_button = scb
        self.add_buttons()

    def add_buttons(self):
        hide_controls_button = Button(position=(2390, 20), size=(150, 60), purpose=self.hide_controls, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="Hide Controls",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(hide_controls_button)

        quit_button = 1
        add_body_button = 1
        reset_button = 1
        speed_control_button = 1
        list_bodies_button = 1
        pause_button = 1

    def show_controls(self):
        self.panel.show()
        self.show_controls_button.disable()

    def hide_controls(self):
        self.panel.hide()
        self.show_controls_button.enable()
