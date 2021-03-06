from collections import defaultdict
import pygame as pg
import os
from params import *
from image_sheet import ImageSheetSimple, ImageSheetRotating

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
		
		saw = pg.transform.scale(
			pg.image.load(os.path.join('resources', 'saw.png')),
			SAW_SIZE)
		self.saw = ImageSheetRotating(saw, 12.0)
		
		self.music_loop = pg.mixer.music.load(os.path.join('resources', 'FLOAT1.wav'))
		self.sound_saw = pg.mixer.Sound(os.path.join('resources', 'saw.wav'))
		self.sound_level_complete = pg.mixer.Sound(os.path.join('resources', 'success.wav'))
		self.sound_scream_fall = pg.mixer.Sound(os.path.join('resources', 'screamfall.wav'))
