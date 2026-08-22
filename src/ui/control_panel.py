from functools import partial

from ui.button import Button
from ui.panel import Panel
import sys
import pygame as pg



class ControlPanel:
    def __init__(self, scb):
        self.panel = Panel(position=(1980, 10), size=(570, 225), colour=(1.0, 1.0, 1.0, 1.0),
                        border_colour=(0, 0, 0, 1.0), corner_radius=10, border_size=5)
        self.show_controls_button = scb
        self.temp_speeds = (1, 10, 100)
        self.temp_speed_index = 0
        self.add_buttons()

    def add_buttons(self):
        self.hide_controls_button = Button(position=(2390, 20), size=(150, 60), purpose=self.hide_controls, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="Hide Controls",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.hide_controls_button)

        self.quit_button = Button(position=(2390, 160), size=(150, 60), purpose=self.quit, colour=(1.0, 0.8, 0.8, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="EXIT",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.quit_button)

        self.pause_button = Button(position=(1990, 20), size=(150, 60), purpose=self.pause, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="Pause",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.pause_button)

        self.speed_button = Button(position=(2150, 20), size=(150, 60), purpose=self.change_speed, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label=f"x{self.temp_speeds[self.temp_speed_index]} Speed",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.speed_button)

        self.new_body_button = Button(position=(1990, 90), size=(150, 60), purpose=None, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="New Body",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.new_body_button)

        self.list_bodies_button = Button(position=(2150, 90), size=(150, 60), purpose=self.list_bodies, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="List Bodies",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.list_bodies_button)

        self.center_camera_button = Button(position=(1990, 160), size=(150, 60), purpose=self.center_camera, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="Centre Camera",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.center_camera_button)

        self.clear_button = Button(position=(2150, 160), size=(150, 60), purpose=self.wipe, colour=(1.0, 1.0, 1.0, 1.0),
                                      border_colour=(0, 0, 0, 1.0), corner_radius=7, border_size=2, label="Clear All",
                                      label_colour=(0, 0, 0, 1.0), enable_shadow=True)
        self.panel.add_element(self.clear_button)

    def show_controls(self):
        self.panel.show()
        self.show_controls_button.disable()

    def hide_controls(self):
        self.panel.hide()
        self.show_controls_button.enable()

    def quit(self):
        pg.quit()
        sys.exit()

    def pause(self):
        if self.pause_button.label == "Pause":
            self.pause_button.label = "Resume"
        else:
            self.pause_button.label = "Pause"
        self.pause_button.text_texture = None

    def change_speed(self):
        self.temp_speed_index = (self.temp_speed_index + 1) % 3
        self.speed_button.label = f"x{self.temp_speeds[self.temp_speed_index]} Speed"
        self.speed_button.text_texture = None

    def reset(self):
        pass

    def center_camera(self):
        pass

    def wipe(self):
        pass


    def list_bodies(self):
        pass


