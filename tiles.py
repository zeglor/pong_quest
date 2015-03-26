import pygame as pg
from params import *

class Tile(pg.sprite.Sprite):
	@classmethod
	def create(cl, ttype, pos):
		if cl.__name__ != 'Tile':
			return None
		
		if ttype == 0:
			return None
		elif ttype == 1:
			return BasicTile(pos)
		elif ttype == 'O':
			return OpaqueTile(pos)
		elif ttype == 'J':
			return JumpTile(pos)
		elif ttype == 'E':
			return FinishTile(pos)
	
	def __init__(self, pos=(0, 0)):
		pg.sprite.Sprite.__init__(self)
		self.pos = pos
		
		self.image = self.get_image()
		
		self.rect = self.image.get_rect()
		self.rect.topleft = [ps*ts for ps, ts in zip(self.pos, TILE_SIZE)]
	
	def get_image(self):
		#hook
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color('#333333'))
		return None
	
	def update(self):
		pass
	
	def activate(self, npc):
		#hook. called when npc goes on this tile
		pass

class BasicTile(Tile):
	def __init__(self, pos=(0, 0)):
		super().__init__(pos)
	
	def get_image(self):
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color(BG_COLOR))
		pg.draw.rect(img, pg.Color('#333333'), img.get_rect(), 2)
		return img

class OpaqueTile(Tile):
	def __init__(self, pos=(0, 0)):
		super().__init__(pos)
	
	def get_image(self):
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color(BG_COLOR))
		pg.draw.rect(img, pg.Color('#333333'), img.get_rect(), 2)
		return img
	
	def activate(self, npc):
		self.image = pg.Surface((0, 0))
		self.rect = self.image.get_rect()

class JumpTile(Tile):
	def __init__(self, pos=(0, 0)):
		super().__init__(pos)
		self.active = False
		self.speed_abs = 6
		self.wait_updates = 1
		self.updates_active = 26
		self.cur_update = 0
		#not to break platform interaction
		#omg, shitty code :(
		self.speed_y = 0
	
	def get_image(self):
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color(BG_COLOR))
		pg.draw.rect(img, pg.Color('#333333'), img.get_rect(), 2)
		return img
	
	def activate(self, npc):
		self.active = True
	
	def update(self):
		if self.active == True:
			if self.wait_updates > 0:
				self.wait_updates -= 1
			else:
				if self.cur_update < self.updates_active / 2:
					self.rect.y -= self.speed_abs
				else:
					self.rect.y += self.speed_abs
				
				self.cur_update += 1
				if self.cur_update >= self.updates_active:
					self.cur_update = 0
					self.wait_updates = 1
					self.active = False

class FinishTile(Tile):
	def __init__(self, pos=(0, 0)):
		super().__init__(pos)
	
	def get_image(self):
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color('#551299'))
		return img
	
	def activate(self, npc):
		#when npc is on top of door, it still counts as win
		#even more shitty code :(
		npc.level.finish_level()
