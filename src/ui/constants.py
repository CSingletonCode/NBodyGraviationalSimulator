import pygame as pg

pg.init()
pg.key.set_repeat(400, 50)

REFERENCE_RESOLUTION = (2560, 1440)
ACTIVE_RESOLUTION = pg.display.Info()