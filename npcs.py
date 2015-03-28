import pygame as pg
from params import *
from copy import copy, deepcopy
from tiles import FinishTile, JumpTile

class NPC(pg.sprite.Sprite):
	@classmethod
	def create(cl, npc_type, pos, level=None):
		if cl.__name__ != 'NPC':
			return None
		
		if npc_type == 'main':
			return NPCMain(pos, level)
		
		if npc_type == 'saw':
			return NPCSaw(pos)
	
	def __init__(self, pos):
		self.initial_pos = copy(pos)
		pg.sprite.Sprite.__init__(self)
		self.image = self.get_image()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.speed = 3
		self.speed_y = 5
		self.surrounding_tiles = set([])
		self.level_finished = False
		
	def get_image(self):
		img = pg.Surface(TILE_SIZE)
		img.fill(pg.Color('#229922'))
		return img
	
	def update(self):
		#pdb.set_trace()
		self.prev_rect = copy(self.rect)
		self.rect.x += self.speed
		self.rect.y += self.speed_y
		
		self.fix_position()
		self.clear_surrounding_tiles()
		#self.surrounding_tiles.clear()
	
	def collide_static_tile(self, tile):
		self.surrounding_tiles.add(tile)
		#self.fix_position()
	
	def fix_position(self):
		pr = self.prev_rect
		nr = self.rect
		
		for t in self.surrounding_tiles:
			tr = t.rect
			if pg.sprite.collide_rect(self, t):
				#pdb.set_trace()
				if nr.y > pr.y and nr.right > tr.left:
				#if self.speed_y > 0:
					#we're trying to move down
					if tr.top <= nr.bottom and tr.top >= pr.bottom:
						nr.bottom = tr.top
				elif nr.y < pr.y and nr.right > tr.left:
				#elif self.speed_y < 0:
					#we're trying to move up
					if tr.bottom >= nr.top and tr.bottom <= pr.top:
						nr.top = tr.bottom
					#if tr.top <= nr.bottom and tr.top >= pr.bottom:
					#	nr.bottom = tr.top
				#if following piece uncommented, jump tile works fine always, but
				#at start of new level npc sometimes falls to the middle of tiles
				#otherwise npc walks over other tiles well always BUT jump tile
				#sometimes doesnt push npc to top. WTF
				#! nope, now its okay. now just the second part happens
				#else:
					#if tr.top <= nr.bottom and tr.top >= pr.bottom:
					#	nr.bottom = tr.top
				#!!more shitty code
				if self.speed_y > 0 and isinstance(t, JumpTile) and \
					nr.bottom >= tr.top and nr.top <= tr.top and \
					(nr.left <= tr.right or nr.right >= tr.left):
						nr.bottom = tr.top
		
		for t in self.surrounding_tiles:
			tr = t.rect
			if pg.sprite.collide_rect(self, t):
				if nr.x > pr.x:
					if tr.left <= nr.right and tr.left >= pr.right:
						nr.right = tr.left
				elif nr.x < pr.x:
					if tr.right > nr.left and tr.right < pr.left:
						nr.left = tr.right
			
			if nr.bottom == tr.top and nr.right > tr.left:
				t.activate(self)
	
	def clear_surrounding_tiles(self):
		self.rect.inflate_ip(abs(self.speed), abs(self.speed_y))
		for tile in set(self.surrounding_tiles):
			if not pg.sprite.collide_rect(self, tile):
				self.surrounding_tiles.remove(tile)
		self.rect.inflate_ip(-abs(self.speed), -abs(self.speed_y))
	
	def out_of_gamefield(self):
		#reinitialize
		self.surrounding_tiles.clear()
		self.rect.topleft = self.initial_pos
		self.speed = 3
		self.speed_y = 5
	
	def die(self, *enemies):
		self.out_of_gamefield()
		
class NPCMain(NPC):
	def __init__(self, pos, level=None):
		super().__init__(pos)
		self.level = level
	
	def update(self):
		#check if we reached finish tile
		ft = [t for t in self.surrounding_tiles if isinstance(t, FinishTile)]
		if len(ft) > 0:
			if self.rect.colliderect(ft[0].rect.inflate((2,2))):
				#we finished the level!
				self.level.finish_level()
		
		#perform usual stuff
		super().update()

class NPCEnemy(NPC):
	def __init__(self, pos, size):
		self.size = size
		super().__init__(pos)
	
	def get_image(self):
		img = pg.Surface(self.size)
		img.fill(pg.Color('#AA1111'))
		return img

#enemies
class NPCSaw(NPCEnemy):
	def __init__(self, pos):
		super().__init__(pos, SAW_SIZE)
	
	def update(self):
		#we dont move
		pass
	
	def collide_static_tile(self, tile):
		pass
