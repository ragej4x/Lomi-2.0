import pygame as pg
import engine


pg.init()
dynamicScale = 3
width , height = 900,620
window = pg.display.set_mode((width, height))
display = pg.Surface((width//dynamicScale, height//dynamicScale))
clock = pg.time.Clock()
pg.display.set_caption("Demo")

#MODES
home = False
freeRoam = True
editMode = False
def showFps():
	font = pg.font.SysFont("Arial", 18)
	getFps = str(int(clock.get_fps()))
	fpsTxt = font.render(getFps, True, (255,255,255))
	window.blit(fpsTxt,(5,5))


def eventHandler():
	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit()

	dynamicResolution = pg.transform.scale(display, (width, height))
	#//
	window.blit(dynamicResolution, (0,0))

	#RENDER TXT INTO WINDOW
	showFps()

while True:
	#native resolution
	window.fill(0)
	#dynamic resolution
	display.fill(0)

	#KEY EVENTS
	mx,my = pg.mouse.get_pos()
	mx // 3
	my // 3
	mouseinput = pg.mouse.get_pressed()
	keyinput = pg.key.get_pressed()

	#Call all func
	engine.map.update_layer_1(display)
	#engine.map.update_layer_2(display)

	engine.lomi.player(display)
	engine.lomi.movement(keyinput)

	engine.map.update(display, keyinput)

	engine.lomi.camera(display, dynamicScale)
	engine.item.update(keyinput, display, mx , my, mouseinput)

	engine.lomi.y += engine.lomi.yVel
	engine.lomi.x += engine.lomi.xVel


	eventHandler()
	clock.tick(60)

	pg.display.flip()
