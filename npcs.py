import pygame as pg
from params import *
from copy import copy, deepcopy
from tiles import FinishTile, JumpTile
#from main import CircleCollider

class NPC(pg.sprite.Sprite):
	@classmethod
	def create(cl, npc_type, pos, level=None, resources = None):
		if cl.__name__ != 'NPC':
			return None
		
		if npc_type == 'main':
			return NPCMain(pos, level, resources)
		
		if npc_type == 'saw':
			return NPCSaw(pos, resources)
	
	def __init__(self, pos, resources = None):
		self.initial_pos = copy(pos)
		pg.sprite.Sprite.__init__(self)
		self.resources = resources
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
		self.prev_rect = copy(self.rect)
		self.rect.x += self.speed
		self.rect.y += self.speed_y
		
		self.fix_position()
		self.clear_surrounding_tiles()
	
	def collide_static_tile(self, tile):
		self.surrounding_tiles.add(tile)
	
	def fix_position(self):
		pr = self.prev_rect
		nr = self.rect
		
		for t in self.surrounding_tiles:
			tr = t.rect
			if pg.sprite.collide_rect(self, t):
				if nr.y > pr.y and nr.right > tr.left:
					#we're trying to move down
					if tr.top <= nr.bottom and tr.top >= pr.bottom:
						nr.bottom = tr.top
				elif nr.y < pr.y and nr.right > tr.left:
					#we're trying to move up
					if tr.bottom >= nr.top and tr.bottom <= pr.top:
						nr.top = tr.bottom
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
	def __init__(self, pos, level=None, resources=None):
		self.image_sheet = copy(resources.old_man)
		super().__init__(pos, resources)
		self.level = level
	
	def update(self):
		#check if we reached finish tile
		ft = [t for t in self.surrounding_tiles if isinstance(t, FinishTile)]
		if len(ft) > 0:
			if self.rect.colliderect(ft[0].rect.inflate((2,2))):
				#we finished the level!
				self.level.finish_level()
		
		#update sprite sheet
		self.image_sheet.update()
		self.image = self.image_sheet.get_image()
		
		#perform usual stuff
		super().update()
	
	def get_image(self):
		return self.image_sheet.get_image()

class NPCEnemy(NPC):
	def __init__(self, pos, size, resources=None):
		self.size = size
		super().__init__(pos)
	
	def get_image(self):
		img = pg.Surface(self.size)
		img.fill(pg.Color('#AA1111'))
		return img

#enemies
class NPCSaw(NPCEnemy):
	def __init__(self, pos, resources = None):
		self.image_sheet = copy(resources.saw)
		super().__init__(pos, SAW_SIZE, resources)
		self.collider = CircleCollider(self.rect.center, SAW_SIZE[0] / 2)
	
	def update(self):
		self.image_sheet.update()
		center = self.rect.center
		self.image = self.image_sheet.get_image()
		self.rect = self.image.get_rect()
		self.rect.center = center
	
	def get_image(self):
		return self.image_sheet.get_image()
	
	def collide_static_tile(self, tile):
		pass

class Collider:
	def __init__(self, *args, **kwargs):
		pass
	
	def collide(self, other):
		pass

class CircleCollider(Collider):
	def __init__(self, pos, radius):
		self.x = pos[0]
		self.y = pos[1]
		self.r = radius
	
	def collide(self, other):
		if isinstance(other, pg.Rect):
			circle = self
			rect = other
			
			class Dist:
				x = 0
				y = 0
			
			circleDistance = Dist()
			circleDistance.x = abs(circle.x - rect.x);
			circleDistance.y = abs(circle.y - rect.y);
			
			if (circleDistance.x > (rect.width/2 + circle.r)):
				return False
			if (circleDistance.y > (rect.height/2 + circle.r)):
				return False
			
			if (circleDistance.x <= (rect.width/2)):
				return True
			if (circleDistance.y <= (rect.height/2)):
				return True
			
			cornerDistance_sq = (circleDistance.x - rect.width/2)**2 + \
				(circleDistance.y - rect.height/2)**2;
			
			return (cornerDistance_sq <= (circle.r**2));
