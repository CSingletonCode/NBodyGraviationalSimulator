from colours import *
from ui.button import Button
from ui.panel import Panel
from simulation.presets import Presets


class PresetDropdown:
    def __init__(self, new_body_panel):
        self.presets = Presets()
        self.nbp = new_body_panel
        self.panel = Panel(position=(1105, 362), size=(350, len(self.presets.preset_list)*40), colour=(*NAVY, 1.0),
                           border_colour=(*CYAN, 1.0), corner_radius=0, border_size=2)
        self.panel.hide()
        self.add_buttons()

    def add_buttons(self):
        """Adds a button to load each defined body preset."""
        for i, preset in enumerate(self.presets.preset_list):
            def fill_values(preset=preset):
                """Set each new body panel label to the necessary value, resetting the texture so they are rerendered.
                   closes the panel and unfreezes the UI."""
                self.nbp.name_box.label = preset["name"]
                self.nbp.name_box.text_texture = None
                self.nbp.type_box.label = preset["type"]
                self.nbp.type_box.text_texture = None
                self.nbp.density_box.label = str(preset["density"])
                self.nbp.density_box.text_texture = None
                self.nbp.radius_box.label = str(preset["radius"])
                self.nbp.radius_box.text_texture = None
                self.nbp.spin_box.label = str(preset["spin"])
                self.nbp.spin_box.text_texture = None

                self.nbp.pos_x.label = str(preset["position"][0])
                self.nbp.pos_x.text_texture = None
                self.nbp.pos_y.label = str(preset["position"][1])
                self.nbp.pos_y.text_texture = None
                self.nbp.pos_z.label = str(preset["position"][2])
                self.nbp.pos_z.text_texture = None

                self.nbp.component_x.label = str(preset["velocity"][0])
                self.nbp.component_x.text_texture = None
                self.nbp.component_y.label = str(preset["velocity"][1])
                self.nbp.component_y.text_texture = None
                self.nbp.component_z.label = str(preset["velocity"][2])
                self.nbp.component_z.text_texture = None

                self.nbp.tilt_x.label = str(preset["tilt"][0])
                self.nbp.tilt_x.text_texture = None
                self.nbp.tilt_y.label = str(preset["tilt"][1])
                self.nbp.tilt_y.text_texture = None
                self.nbp.tilt_z.label = str(preset["tilt"][2])
                self.nbp.tilt_z.text_texture = None

                self.nbp.colour_x.label = str(preset["colour"][0])
                self.nbp.colour_x.text_texture = None
                self.nbp.colour_y.label = str(preset["colour"][1])
                self.nbp.colour_y.text_texture = None
                self.nbp.colour_z.label = str(preset["colour"][2])
                self.nbp.colour_z.text_texture = None

                self.nbp.panel.unfreeze()
                self.panel.hide()
            button = Button(position=(1105, 362 + i*40), size=(350, 40), purpose=fill_values,
                            colour=(*NAVY, 1.0), border_colour=(*CYAN, 1.0), corner_radius=0,
                            border_size=2, label=preset["name"], label_colour=(*CYAN, 1.0), enable_shadow=False)
            button.press_drop = False
            self.panel.add_element(button)