from ui.button import Button
from ui.panel import Panel
from ui.textbox import TextBox
from assets.colours import *


class NewBodyPanel:
    def __init__(self, unfreeze_controls, invalid_data):
        self.unfreeze_controls = unfreeze_controls
        self.panel = Panel(position=(640, 10), size=(1280, 300), colour=(*SILVER, 1.0),
                        border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)
        self.standard_data_boxes = []
        self.position_boxes = None
        self.velocity_boxes = None
        self.tilt_boxes = None
        self.invalid_data = invalid_data
        self.add_features()



    def add_features(self):
        # Name
        self.name_label = TextBox(position=(681, 20), size=(100, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Enter Name:")
        self.panel.add_element(self.name_label)
        self.name_box = TextBox(position=(680, 42), size=(360, 40), colour=(*NAVY, 1.0),
                                border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                                label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.name_box)
        self.standard_data_boxes.append(self.name_box)

        # Type of Body
        self.type_label = TextBox(position=(676, 92), size=(100, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Enter Type:")
        self.panel.add_element(self.type_label)
        self.type_box = Button(position=(680, 114), size=(360, 40), purpose=None, colour=(*NAVY, 1.0),
                                border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label=None,
                                label_colour=(*CYAN, 1.0), enable_shadow=False)
        self.type_box.press_drop = False
        self.panel.add_element(self.type_box)
        self.standard_data_boxes.append(self.type_box)

        # Parent Body
        self.parent_label = TextBox(position=(683, 164), size=(100, 20), colour=(*SILVER, 1.0),
                                    border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                    label_colour=(*BLACK, 1.0), writable=False, label="Enter Parent:")
        self.panel.add_element(self.parent_label)
        self.parent_box = TextBox(position=(680, 186), size=(360, 40), colour=(*NAVY, 1.0),
                                  border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                                  label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.parent_box)
        self.standard_data_boxes.append(self.parent_box)

        # Density
        self.density_label = TextBox(position=(1065, 20), size=(150, 20), colour=(*SILVER, 1.0),
                                     border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                     label_colour=(*BLACK, 1.0), writable=False, label="Density (kg/m³):")
        self.panel.add_element(self.density_label)
        self.density_box = TextBox(position=(1075, 42), size=(360, 40), colour=(*NAVY, 1.0),
                                   border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                                   label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.density_box)
        self.standard_data_boxes.append(self.density_box)

        # Radius
        self.radius_label = TextBox(position=(1053, 92), size=(150, 20), colour=(*SILVER, 1.0),
                                    border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                    label_colour=(*BLACK, 1.0), writable=False, label="Radius (km):")
        self.panel.add_element(self.radius_label)
        self.radius_box = TextBox(position=(1075, 114), size=(360, 40), colour=(*NAVY, 1.0),
                                  border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                                  label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.radius_box)
        self.standard_data_boxes.append(self.radius_box)

        # Rotational Velocity
        self.spin_label = TextBox(position=(1079, 164), size=(150, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Rotational Velocity:")
        self.panel.add_element(self.spin_label)
        self.spin_box = TextBox(position=(1075, 186), size=(360, 40), colour=(*NAVY, 1.0),
                                border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                                label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.spin_box)
        self.standard_data_boxes.append(self.spin_box)

        # POSITION

        self.pos_label = TextBox(position=(1470, 20), size=(410, 20), colour=(*SILVER, 1.0),
                                 border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                 label_colour=(*BLACK, 1.0), writable=False, label="Position Vector (km):")
        self.panel.add_element(self.pos_label)

        self.pos_x = TextBox(position=(1470, 45), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.pos_x)

        self.pos_y = TextBox(position=(1610, 45), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.pos_y)

        self.pos_z = TextBox(position=(1750, 45), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.pos_z)
        self.position_boxes = (self.pos_x, self.pos_y, self.pos_z)

        # VELOCITY

        self.velocity_label = TextBox(position=(1470, 92), size=(410, 20), colour=(*SILVER, 1.0),
                                 border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                 label_colour=(*BLACK, 1.0), writable=False, label="Velocity Vector (km/s):")
        self.panel.add_element(self.velocity_label)

        self.component_x = TextBox(position=(1470, 117), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.component_x)

        self.component_y = TextBox(position=(1610, 117), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.component_y)

        self.component_z = TextBox(position=(1750, 117), size=(130, 35), colour=(*NAVY, 1.0),
                             border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                             label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.component_z)
        self.velocity_boxes = (self.component_x, self.component_y, self.component_z)

        # TILT

        self.tilt_label = TextBox(position=(1470, 164), size=(410, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Axial Tilt Vector (-1 to 1):")
        self.panel.add_element(self.tilt_label)

        self.tilt_x = TextBox(position=(1470, 189), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.tilt_x)

        self.tilt_y = TextBox(position=(1610, 189), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.tilt_y)

        self.tilt_z = TextBox(position=(1750, 189), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.tilt_z)
        self.tilt_boxes = (self.tilt_x, self.tilt_y, self.tilt_z)

        # Control Buttons

        self.cancel_button = Button(position=(880, 240), size=(150, 50), purpose=self.clear_and_close,
                                    colour=(*NAVY, 1.0),
                                    border_colour=(*RED, 1.0), corner_radius=7, border_size=2, label="CANCEL",
                                    label_colour=(*RED, 1.0), enable_shadow=True)
        self.panel.add_element(self.cancel_button)

        self.enter_button = Button(position=(1530, 240), size=(150, 50), purpose=self.confirm_body, colour=(*NAVY, 1.0),
                                   border_colour=(*GREEN, 1.0), corner_radius=7, border_size=2, label="ENTER BODY",
                                   label_colour=(*GREEN, 1.0), enable_shadow=True)
        self.panel.add_element(self.enter_button)


    def clear_and_close(self):
        def clear_box_group(tuples):
            for vect_box in tuples:
                vect_box.label = ""
                vect_box.text_texture = None

        for box in self.standard_data_boxes:
            box.label = ""
            box.text_texture = None

        for boxes in (self.position_boxes, self.velocity_boxes, self.tilt_boxes):
            clear_box_group(boxes)

        self.unfreeze_controls()
        self.panel.hide()

    def confirm_body(self):
        validation_failed = False

        def validate(box):
            nonlocal validation_failed
            data = box.label
            if data == "":
                validation_failed = True
                return 0.0
            try:
                return float(data)
            except ValueError or TypeError:
                validation_failed = True
                return 0.0

        density = validate(self.standard_data_boxes[3])
        radius = validate(self.standard_data_boxes[4])
        spin = validate(self.standard_data_boxes[5])

        position = tuple(validate(box) for box in self.position_boxes)
        velocity = tuple(validate(box) for box in self.velocity_boxes)
        tilt = tuple(validate(box) for box in self.tilt_boxes)

        if validation_failed:
            self.panel.freeze()
            self.invalid_data.show()
            return

        new_data = {
            "name": self.standard_data_boxes[0].label,
            "type": self.standard_data_boxes[1].label,
            "parent": self.standard_data_boxes[2].label,
            "density": density,
            "radius": radius,
            "spin": spin,
            "position": position,
            "velocity": velocity,
            "tilt": tilt,
        }
        print(new_data)
        ## MAKE NEW BODY HERE ##
        self.clear_and_close()

