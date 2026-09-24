import pygame as pg

REFERENCE_RESOLUTION = (2560, 1440)
ACTIVE_RESOLUTION = pg.display.Info()

RADIUS_SCALE = 150_000.0
DISTANCE_SCALE = 1_500_000.0

SPEEDS = (1.0, 86_400.0, 7_500_000.0,)
SUBSTEPS = (1, 20, 250)

SIZE_CAPS = {
    "Terrestrial Planet": 0.1,
    "Gas Giant": 0.7,
    "Ice Giant": 0.4,
    "Moon": 0.01,
    "Dwarf Planet": 0.01,
    "Star": 1.0
}