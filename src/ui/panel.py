from ui.element import Element


class Panel(Element):
    def __init__(self, position, size, colour, border_colour, corner_radius, border_size, enable_shadow=False):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.text_texture = None
        self.pressed = False
        self.contains = []

    def add_element(self, element):
        self.contains.append(element)

    def hide(self):
        self.disable()
        for element in self.contains:
            element.disable()

    def show(self):
        self.enable()
        for element in self.contains:
            element.enable()

    def update(self, mouse_position):
        for element in self.contains:
            element.update(mouse_position)

    def draw(self, renderer):
        if self.visible:
            renderer.draw_basics(self)
            for element in self.contains:
                element.draw(renderer)

    def freeze(self):
        for element in self.contains:
            element.freeze()

    def unfreeze(self):
        for element in self.contains:
            element.unfreeze()

    def clear(self):
        self.contains = []

