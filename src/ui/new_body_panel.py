from ui.panel import Panel


class NewBodyPanel:
    def __init__(self):
        self.panel = Panel(position=(640, 10), size=(1280, 225), colour=(1.0, 1.0, 1.0, 1.0),
                        border_colour=(0, 0, 0, 1.0), corner_radius=10, border_size=5)