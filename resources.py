from collections import defaultdict
import pygame as pg
import os
from params import *
from image_sheet import ImageSheetSimple

class ResourcesContainer:
	def __init__(self):
		self.ground_tile = None
		self.bg = None
		self.door = None
	
	def load_all(self):
		self.ground_tile = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'ground_tile.png')),
			TILE_SIZE)
		self.ground_tile = self.ground_tile.convert()
		
		self.bg = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'background-sky.png')),
			DISPLAY_SIZE)
		self.bg = self.bg.convert()
		
		self.door = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'door.png')).convert(),
			TILE_SIZE)
		self.door = self.door.convert()
		
		old_man_sheet = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'old_man.png')),
			(TILE_SIZE[0] * 3, int(TILE_SIZE[1]*1.2)))
		old_man_sheet = old_man_sheet.convert_alpha()
		
		self.old_man = ImageSheetSimple(old_man_sheet, (TILE_SIZE[0], int(TILE_SIZE[1]*1.2)), 3, 10)
