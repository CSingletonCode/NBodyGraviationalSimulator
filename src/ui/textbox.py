from ui.element import Element


class TextBox(Element):
    def __init__(self, position, size, colour, border_colour, label, label_colour, corner_radius, border_size, enable_shadow, writable):
        super().__init__(position, size, colour, border_colour, corner_radius, border_size, enable_shadow)
        self.label = label
        self.label_colour = label_colour
        self.writable = writable

    #def write(self, ):