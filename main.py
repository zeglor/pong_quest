import pygame as pg
from levels import Level
from resources import ResourcesContainer
from params import *
from npcs import Collider


def collided(sprite1, sprite2):
	is_collided = False
	collider1 = None
	collider2 = None
	try:
		collider1 = sprite1.collider
	except AttributeError:
		collider1 = sprite1.rect
	try:
		collider2 = sprite2.collider
	except AttributeError:
		collider2 = sprite2.rect
	
	if isinstance(collider1, Collider):
		return collider1.collide(collider2)
	elif isinstance(collider2, Collider):
		return collider2.collide(collider1)
	else:
		return pg.sprite.collide_rect(sprite1, sprite2)

def main():
	pg.init()
	screen = pg.display.set_mode(DISPLAY_SIZE)
	screen_rect = pg.display.get_surface().get_rect()
	resources = ResourcesContainer()
	resources.load_all()
	
	#start main theme
	pg.mixer.music.play(loops=-1)
	
	clock = pg.time.Clock()
	
	level = Level(resources)
	level.start()
	
	#==========main game loop========
	running = True
	while running:
		clock.tick(60)
		
		#events
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False
			elif e.type == pg.KEYDOWN and e.unicode == 'r':
				level.start()
		
		#collide
		#rigid with ground
		for r in level.Grigid:
			r.rect.inflate_ip((2 * abs(r.speed), 2 * abs(r.speed_y)))
		for r, gl in pg.sprite.groupcollide(level.Grigid, level.Gground, False, False).items():
			for g in gl:
				r.collide_static_tile(g)
		
		for r in level.Grigid:
			r.rect.inflate_ip((-2 * abs(r.speed), -2 * abs(r.speed_y)))
		
		#update stuff
		level.Gdynamic.update()
		
		#check if we collide any enemy
		for npc, enemies in pg.sprite.groupcollide(level.GmainNpc, level.Genemies, False, False, collided).items():
			npc.die(enemies)
		
		#check if any item gone outside the border
		for o in level.Gdynamic:
			if not screen_rect.colliderect(o.rect):
				o.out_of_gamefield()
		
		#rigid with ground
		for r, gl in pg.sprite.groupcollide(level.Grigid, level.Gground, False, False).items():
			for g in gl:
				r.collide_static_tile(g)
		
		#draw stuff
		bg = pg.Surface(DISPLAY_SIZE)
		if resources.bg is not None:
			bg.blit(resources.bg, (0, 0))
		else:
			bg.fill(pg.Color(BG_COLOR))
		
		font = pg.font.SysFont('verdana', size = 14)
		fps_text = font.render('FPS: {}'.format(int(clock.get_fps())), True, pg.Color('#111111'))
		bg.blit(fps_text, (10, 10))
		
		
		screen.blit(bg, dest = (0,0))
		level.Gdrawables.draw(screen)
		pg.display.update()
	
if __name__ == '__main__':
	main()
