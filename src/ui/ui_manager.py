from .button import Button

class Manager:
    def __init__(self):
        self.elements = []

        self.create_ui()

    def create_ui(self):

        button1 = Button(
            position=(100, 100),
            size=(200, 80),
            purpose=self.button_one_pressed,
            colour=(0.2, 0.6, 1.0, 1.0),
            border_colour=(0, 0, 0, 1),
            label="Button 1",
            corner_radius=40,
            border_size=20

        )

        button2 = Button(
            position=(100, 220),
            size=(200, 80),
            purpose=self.button_two_pressed,
            colour=(1.0, 0.3, 0.3, 1.0),
            border_colour=(1, 1, 1, 1),
            label="Button 2",
            corner_radius=50,
            border_size=5
        )

        self.elements.append(button1)
        self.elements.append(button2)

    def button_one_pressed(self):
        print("Button 1 pressed")
    def button_two_pressed(self):
        print("Button 2 pressed")

    def update_elements(self, mouse_position):
        for element in self.elements:
            element.update(mouse_position)

    def handle_event(self, event):
        for element in self.elements:
            element.handle_event(event)

    def render(self, renderer):
        for element in self.elements:
            if element.visible:
                renderer.draw_element(element)