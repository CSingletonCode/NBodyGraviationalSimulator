import numpy as np
from ui.button import Button
from ui.panel import Panel
from ui.textbox import TextBox
from colours import *

class NewBodyPanel:
    def __init__(self, unfreeze_features, invalid_data, simulation, retrieve_parent, refresh_list):
        self.unfreeze_features = unfreeze_features
        self.panel = Panel(position=(640, 10), size=(1280, 372), colour=(*SILVER, 1.0),
                        border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)
        self.standard_data_boxes = []
        self.position_boxes = None
        self.velocity_boxes = None
        self.tilt_boxes = None
        self.retrieve_parent = retrieve_parent
        self.invalid_data = invalid_data
        self.simulation = simulation
        self.refresh_list = refresh_list
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
        self.parent_box = Button(position=(680, 186), size=(360, 40), purpose=None, colour=(*NAVY, 1.0),
                                  border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2, label=None,
                                  label_colour=(*CYAN, 1.0), enable_shadow=False)
        self.parent_box.press_drop = False
        self.panel.add_element(self.parent_box)

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

        # Angular Velocity
        self.spin_label = TextBox(position=(1071, 164), size=(150, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Rotation Period (hrs)")
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

        # Colour

        self.colour_label = TextBox(position=(1470, 236), size=(410, 20), colour=(*SILVER, 1.0),
                                  border_colour=(*SILVER, 1.0), corner_radius=0, border_size=0,
                                  label_colour=(*BLACK, 1.0), writable=False, label="Colour (0 - 1):")
        self.panel.add_element(self.colour_label)

        self.colour_x = TextBox(position=(1470, 261), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.colour_x)

        self.colour_y = TextBox(position=(1610, 261), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.colour_y)

        self.colour_z = TextBox(position=(1750, 261), size=(130, 35), colour=(*NAVY, 1.0),
                              border_colour=(*CYAN, 1.0), corner_radius=5, border_size=2,
                              label_colour=(*CYAN, 1.0), writable=True)
        self.panel.add_element(self.colour_z)
        self.colour_boxes = (self.colour_x, self.colour_y, self.colour_z)

        # Load a preset

        self.preset_button = Button(position=(1205, 312), size=(150, 50), purpose=None, colour=(*NAVY, 1.0),
                                    border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="SELECT PRESET",
                                    label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.preset_button)

        # Control Buttons

        self.cancel_button = Button(position=(880, 312), size=(150, 50), purpose=self.clear_and_close, colour=(*NAVY, 1.0),
                                    border_colour=(*RED, 1.0), corner_radius=7, border_size=2, label="CANCEL",
                                    label_colour=(*RED, 1.0), enable_shadow=True)
        self.panel.add_element(self.cancel_button)

        self.enter_button = Button(position=(1530, 312), size=(150, 50), purpose=self.confirm_body, colour=(*NAVY, 1.0),
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

        self.parent_box.label = ""
        self.parent_box.text_texture = None

        for boxes in (self.position_boxes, self.velocity_boxes, self.tilt_boxes, self.colour_boxes):
            clear_box_group(boxes)

        self.unfreeze_features()
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

        density = validate(self.standard_data_boxes[2])
        radius = validate(self.standard_data_boxes[3])
        spin = validate(self.standard_data_boxes[4])

        position = tuple(validate(box) for box in self.position_boxes)
        velocity = tuple(validate(box) for box in self.velocity_boxes)
        tilt = tuple(validate(box) for box in self.tilt_boxes)
        colour = tuple(validate(box) for box in self.colour_boxes)

        if validation_failed:
            self.panel.freeze()
            self.invalid_data.show()
            return

        parent_object = self.retrieve_parent()
        if parent_object is None:
            parent_name = "None"
        elif isinstance(parent_object, str):
            parent_name = parent_object
        else:
            parent_name = parent_object.name

        new_data = {
            "name": self.standard_data_boxes[0].label,
            "type": self.standard_data_boxes[1].label,
            "parent": parent_name,
            "density": density,
            "radius": radius,
            "mass": self.calculate_mass(density, radius),
            "r_period": spin,
            "spin": self.calculate_angular_velocity(spin),
            "position": self.calculate_world_position(parent_object, position),
            "velocity": self.calculate_world_velocity(parent_object, velocity),
            "tilt": tilt,
            "colour": colour
        }
        self.simulation.make_body(new_data)
        self.refresh_list()
        self.clear_and_close()

    def calculate_world_position(self, parent, local_position):
        pos = np.array(local_position, dtype=np.float64)
        if parent is not None and not isinstance(parent, str):
            parent_pos = np.array(parent.position, dtype=np.float64)
            pos += parent_pos
        return pos

    def calculate_world_velocity(self, parent, local_velocity):
        vel = np.array(local_velocity, dtype=np.float64)
        if parent is not None and not isinstance(parent, str):
            parent_vel = np.array(parent.velocity, dtype=np.float64)
            vel += parent_vel
        return vel

    def calculate_angular_velocity(self, rotation_period):
        v = ( 2.0 * np.pi ) / (3600.0 * rotation_period)
        return v

    def calculate_mass(self, density, radius):
        volume = (4.0 / 3.0) * np.pi * ((radius * 1000.0) ** 3)
        mass = volume * density
        return mass
