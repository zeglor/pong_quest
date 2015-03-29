import pygame as pg

class ImageSheetSimple:
	def __init__(self, sheet, frame_size, num_frames, updates_per_frame):
		self.sheet = sheet
		self.num_frames = num_frames
		self.updates_per_frame = updates_per_frame
		
		self.counter = 0
		self.frame_indx = 0
		
		self.framel = [pg.Surface(frame_size, flags=pg.SRCALPHA) for _ in range(num_frames)]
		for indx, frame in enumerate(self.framel):
			frame.blit(
				sheet, \
				dest = (0,0), \
				area = (frame_size[0]*indx, 0, frame_size[0]*(1+indx), frame_size[1]))
	
	def update(self):
		self.counter += 1
		if self.counter >= self.updates_per_frame:
			self.counter = 0
			self.frame_indx += 1
			
			if self.frame_indx >= self.num_frames:
				self.frame_indx = 0
	
	def get_image(self):
		return self.framel[self.frame_indx]

class ImageSheetRotating:
	def __init__(self, sheet, angular_speed):
		self.sheet = sheet
		self.angular_speed = angular_speed
		self.angle = 0.0
	
	def update(self):
		self.angle += self.angular_speed
	
	def get_image(self):
		center = self.sheet.get_rect().center
		img = pg.transform.rotate(self.sheet, self.angle)
		img.get_rect().center = center
		return img
