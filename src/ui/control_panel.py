import pygame as pg
import sys


from colours import *
from ui.button import Button
from ui.panel import Panel

class ControlPanel:
    def __init__(self, scb, simulation):
        self.panel = Panel(position=(1980, 10), size=(570, 225), colour=(*SILVER, 1.0),
                        border_colour=(*CYAN, 1.0), corner_radius=10, border_size=5)
        self.show_controls_button = scb
        self.simulation = simulation
        self.speed_arrows = (">", ">>", ">>>")
        self.speed_index = 0
        self.paused = False
        self.add_buttons()

    def add_buttons(self):
        # Button to hide the control panel and display the show controls button.
        self.hide_controls_button = Button(position=(2390, 20), size=(150, 60), purpose=self.hide_controls, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="Hide Controls",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.hide_controls_button)

        # Button to save and close the simulation.
        self.quit_button = Button(position=(2390, 160), size=(150, 60), purpose=self.quit, colour=(*NAVY, 1.0),
                                      border_colour=(*RED, 1.0), corner_radius=7, border_size=2, label="EXIT",
                                      label_colour=(*RED, 1.0), enable_shadow=True)
        self.panel.add_element(self.quit_button)

        # Button to pause the simulation but allow the UI to still be used and the camera to be moved.
        self.pause_button = Button(position=(1990, 20), size=(150, 60), purpose=self.pause, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="Pause",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.pause_button)

        # Button to select the speed multiplier for the simulation, changes the speed index.
        self.speed_button = Button(position=(2150, 20), size=(150, 60), purpose=self.change_speed, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label=f"Speed: {self.speed_arrows[self.speed_index]}",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.speed_button)

        # Button to display the panel to add a new body.
        self.new_body_button = Button(position=(1990, 90), size=(150, 60), purpose=None, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="New Body",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.new_body_button)

        # Button to display the panel to list all bodies in the simulation.
        self.list_bodies_button = Button(position=(2150, 90), size=(150, 60), purpose=None, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="List Bodies",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.list_bodies_button)

        # Button to change between proportional and capped radii.
        self.toggle_radius_button = Button(position=(1990, 160), size=(150, 60), purpose=None, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="Toggle Real Scale",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.toggle_radius_button)

        # button to wipe the simulation.
        self.clear_button = Button(position=(2150, 160), size=(150, 60), purpose=None, colour=(*NAVY, 1.0),
                                      border_colour=(*CYAN, 1.0), corner_radius=7, border_size=2, label="Clear All",
                                      label_colour=(*CYAN, 1.0), enable_shadow=True)
        self.panel.add_element(self.clear_button)

    def hide_controls(self):
        self.panel.hide()
        self.show_controls_button.enable()

    def quit(self):
        self.simulation.save_simulation()
        pg.quit()
        sys.exit()

    def pause(self):
        if self.pause_button.label == "Pause":
            self.pause_button.label = "Resume"
        else:
            self.pause_button.label = "Pause"
        self.pause_button.text_texture = None
        self.paused = not self.paused
        self.speed_index = -1
        self.change_speed()

    def change_speed(self):
        """Uses the speed index to select the correct speed arrow,
           each arrow corresponds to a speed multiplier at the same index."""
        self.speed_index = (self.speed_index + 1) % 3
        self.speed_button.label = f"Speed: {self.speed_arrows[self.speed_index]}"
        self.speed_button.text_texture = None
