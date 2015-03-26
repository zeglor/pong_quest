import pygame as pg
PLATFORM_SIZE = (80, 20)

class TwoPlatforms:
	@classmethod
	def create(cl, platform_type, *parms, **kparms):
		if cl.__name__ != 'TwoPlatforms':
			return None
		
		if platform_type == 'gravity':
			return TwoPlatformsGravity(platform_type, *parms, **kparms)
	
	def __init__(self, platform_type, dynamic_objects):
		#init top platform
		self.pl_top = Platform.create(platform_type, pos = (20, 60), keys = (pg.K_a, pg.K_d), 
			dynamic_objects = dynamic_objects, top=True)
		#init bottom platform
		self.pl_bot = Platform.create(platform_type, pos = (20, DISPLAY_SIZE[1]-60), keys = (pg.K_LEFT, pg.K_RIGHT), 
			dynamic_objects = dynamic_objects)
	
	def add(self, group, *groups):
		self.pl_top.add(group, *groups)
		self.pl_bot.add(group, *groups)

class TwoPlatformsGravity(TwoPlatforms):
	def __init__(self, platform_type, dynamic_objects):
		#init top platform
		self.pl_top = Platform.create(platform_type, pos = (20, 60), keys = (pg.K_a, pg.K_d), 
			dynamic_objects = dynamic_objects, top=True)
		#init bottom platform
		self.pl_bot = Platform.create(platform_type,pos = (20, DISPLAY_SIZE[1]-60), keys = (pg.K_LEFT, pg.K_RIGHT), 
			dynamic_objects = dynamic_objects)

class Platform(pg.sprite.Sprite):
	@classmethod
	def create(cl, platform_type, *parms, **kparms):
		if cl.__name__ != 'Platform':
			return None
		
		if platform_type == 'gravity':
			return PlatformGravity(*parms, **kparms)
	
	def __init__(self, pos, keys, dynamic_objects, top=False):
		pg.sprite.Sprite.__init__(self)
		
		self.image = self.get_image()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.speed_abs = 4
		self.speed = 0
		self.speed_y = 0
		self.keys = keys
		self.dynamic_objects = dynamic_objects
	
	def get_image(self):
		img = pg.Surface(PLATFORM_SIZE)
		img.fill(pg.Color('#111155'))
		pg.draw.rect(img, pg.Color('#333333'), img.get_rect(), 2)
		return img
	
	def update(self):
		keys = pg.key.get_pressed()
		if keys[self.keys[1]]:
			self.speed = self.speed_abs
		elif keys[self.keys[0]]:
			self.speed = -self.speed_abs
		else:
			self.speed = 0
		
		if keys[pg.K_q]:
			#activate special ability
			self.special(True)
		else:
			self.special(False)
		
		self.rect.x += self.speed
	
	def special(self, activate):
		#hook
		pass

class PlatformGravity(Platform):
	def __init__(self, pos, keys, dynamic_objects, top=False):
		super().__init__(pos, keys, dynamic_objects, top)
		self.affected_objects = {}
		self.delta_speed = 8
		if top:
			self.delta_speed = -self.delta_speed
	
	def special(self, activate):
		if activate == True:
			for o in self.dynamic_objects:
				if o.rect.center[0] >= self.rect.left and o.rect.left <= self.rect.center[0]:
					if o not in self.affected_objects.keys():
						self.affected_objects[o] = (o, o.speed_y)
						o.speed_y += self.delta_speed
				else:
					if o in self.affected_objects.keys():
						o.speed_y = self.affected_objects[o][1]
						del self.affected_objects[o]
		else:
			#restore affected objects state
			if len(self.affected_objects) > 0:
				for o, speed in self.affected_objects.values():
					o.speed_y = speed
				self.affected_objects.clear()

