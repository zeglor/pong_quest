import pygame as pg
from levels import Level
from params import *

def main():
	pg.init()
	
	clock = pg.time.Clock()
	screen = pg.display.set_mode(DISPLAY_SIZE)
	screen_rect = pg.display.get_surface().get_rect()
	
	level = Level()
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
		for npc, enemies in pg.sprite.groupcollide(level.GmainNpc, level.Genemies, False, False).items():
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
		bg.fill(pg.Color(BG_COLOR))
		screen.blit(bg, dest = (0,0))
		level.Gdrawables.draw(screen)
		pg.display.update()
	
if __name__ == '__main__':
	main()
