from collections import defaultdict
import pygame as pg
import os
from params import *

class ResourcesContainer:
	def __init__(self):
		self.ground_tile = None
		self.bg = None
	
	def load_all(self):
		self.ground_tile = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'ground_tile.png')),
			TILE_SIZE)
		
		self.bg = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'background-sky.png')),
			DISPLAY_SIZE)
