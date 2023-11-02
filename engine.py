import pygame as pg
import json
import csv
import math
from configparser import ConfigParser

with open('data/file.json', 'r') as data:
    file = json.load(data)
map_L0 = file['map_layer_0']
map_L1 = file['map_layer_1']
map_L2 = file['map_layer_2']

class MainClass():
	def __init__(self, x , y,):
		self.x = x
		self.y = y

		self.left = True
		self.right = False
		self.down = False
		self.up = False

		self.speed = 1

		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)


		self.fix_speed = 0.8
		#CAMERA

		self.cameraSpeed = 0.8
		self.cameraX = self.x - 125
		self.cameraY = self.y - 110

	def player(self, display):
		self.lomiRect = pg.Rect(self.x - self.cameraX , self.y - self.cameraY, 16,16)
		self.lomiObjRect = pg.Rect(self.x - self.cameraX + 3, self.y - self.cameraY + 11, 9,9)
		pg.draw.rect(display, self.red, self.lomiRect, 1)
		pg.draw.rect(display, self.blue, self.lomiObjRect, 1)
		#pg.draw.rect(display, (255,255,255), (30,30,30,30))

	def movement(self, keyinput):
		self.xVel = 0
		self.yVel = 0


		if keyinput[pg.K_w]:
			self.yVel -= self.speed
			self.up = True
			self.down = False
			self.left = False
			self.right = False

		if keyinput[pg.K_s]:
			self.yVel += self.speed
			self.down = True
			self.up = False
			self.left = False
			self.right = False

		if keyinput[pg.K_d]:
			self.xVel += self.speed
			self.right = True
			self.left = False
			self.up = False
			self.down = False

		if keyinput[pg.K_a]:
			self.xVel -= self.speed
			self.left = True
			self.right = False
			self.up = False
			self.down = False

			#FIX


		if keyinput[pg.K_a] and keyinput[pg.K_d]:
			self.right = True
			self.xVel += self.speed

		elif keyinput[pg.K_w] and keyinput[pg.K_d]:
			self.speed = self.fix_speed

		elif keyinput[pg.K_a] and keyinput[pg.K_s]:
			self.speed = self.fix_speed

		elif keyinput[pg.K_w] and keyinput[pg.K_a]:
			self.speed = self.fix_speed

		elif keyinput[pg.K_s] and keyinput[pg.K_d]:
			self.speed = self.fix_speed

		else:
			self.speed = 1


		#print(self.yVel, self.xVel)

	def camera(self, display, dynamicScale):
		center = pg.draw.rect(display, (255,255,255), (900 /6, 620/6, 1,1 ))
		distance = math.atan2(self.y - self.cameraY - 620 // 6, self.x - self.cameraX - 900 // 6)
		self.cdx = math.cos(distance)
		self.cdy = math.sin(distance)

		if not center.colliderect(self.lomiRect):
			self.cameraX += self.cdx * self.cameraSpeed
			self.cameraY += self.cdy * self.cameraSpeed

#labyoulomiko
	def updateAnimation(self, display, keyinput):


		if keyinput[pg.K_w] and self.up == True:
			anim.runUpAnim(display, pg)
		elif not keyinput[pg.K_w] and self.up == True:
			anim.idleUpAnim(display, pg)

		if keyinput[pg.K_s] and self.down == True:
			anim.runDownAnim(display, pg)

		elif not keyinput[pg.K_s] and self.down == True:
			anim.idleDownAnim(display, pg)

		if keyinput[pg.K_d] and self.right == True:
			anim.runRightAnim(display, pg)

		elif not keyinput[pg.K_d] and self.right == True:
			anim.idleRightAnim(display, pg)

		if keyinput[pg.K_a] and self.left == True:
			anim.runLeftAnim(display, pg)

		elif not keyinput[pg.K_a] and self.left == True:
			anim.idleLeftAnim(display, pg)



lomi = MainClass(100,100)


class MapClass():
	def __init__(self):
		import pygame as pg
		self.blockPos = []
		self.tileSurface = pg.Surface((16,16))


		self.world_data = []
		self.world_data_layer_2 = []
		self.world_data_layer_3 = []
		self.world_coll_data = []
		self.max_col = 50
		self.rows = 50
		self.height = 900
		self.width = 620
		self.tile_size = self.height // self.rows
		self.tile = 1


		self.tile_list = []
		self.tile_count = 135

		#LOAD IMAGE


		for row in range(self.rows):
			r = [0] * self.max_col
			self.world_data.append(r)

		for row in range(self.rows):
			r = [0] * self.max_col
			self.world_data_layer_2.append(r)

		for row in range(self.rows):
			r = [0] * self.max_col
			self.world_data_layer_3.append(r)

		for row in range(self.rows):
			r = [0] * self.max_col
			self.world_coll_data.append(r)

		#LOAD DATA
		with open(map_L1, newline='') as data:
			reader = csv.reader(data, delimiter = ",")
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					self.world_data[x][y] = int(tile)

		with open(map_L2, newline='') as data:
			reader = csv.reader(data, delimiter = ",")
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					self.world_data_layer_2[x][y] = int(tile)


		for i in range(1, self.tile_count):
			self.tile = pg.image.load(f"data/map/texture/tile- ({i}).png")
			#self.tile = pg.transform.scale(self.tile, (self.tile_size, self.tile_size))
			self.tile_list.append(self.tile)

	def update(self, display, keyinput):

		if keyinput[pg.K_l]:
			#LOAD DATA
			with open(map_L1, newline='') as data:
				reader = csv.reader(data, delimiter = ",")
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						self.world_data[x][y] = int(tile)


			with open(map_L2, newline='') as data:
				reader = csv.reader(data, delimiter = ",")
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						self.world_data_layer_2[x][y] = int(tile)

			with open(map_L3, newline='') as data:
				reader = csv.reader(data, delimiter = ",")
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						self.world_data_layer_3[x][y] = int(tile)

			with open(map_coll, newline='') as data:
				reader = csv.reader(data, delimiter = ",")
				for x, row in enumerate(reader):
					for y, tile in enumerate(row):
						self.world_coll_data[x][y] = int(tile)

		self.show_rect = True


        #tile collision
		for y, row in enumerate(self.world_data):
			for x, tile in enumerate(row):


				if tile == -1:
					if self.show_rect == True:
						self.block = pg.Rect((x * 16 - lomi.cameraX + 6 , y * 16 - lomi.cameraY, 10, 10))
						pg.draw.rect(display, (255,255,255), self.block,1)

					#COLLISION
					if self.block.colliderect(lomi.lomiObjRect.x + lomi.xVel , lomi.lomiObjRect.y, lomi.lomiObjRect.width, lomi.lomiObjRect.height):
						lomi.xVel = 0


					if self.block.colliderect(lomi.lomiObjRect.x + lomi.xVel , lomi.lomiObjRect.y, lomi.lomiObjRect.width , lomi.lomiObjRect.height):
						lomi.xVel = 0

					if self.block.colliderect(lomi.lomiObjRect.x, lomi.lomiObjRect.y + lomi.yVel, lomi.lomiObjRect.width , lomi.lomiObjRect.height):
						lomi.yVel = 0
    #blit the tiles
	def update_layer_1(self, display):
		#display.blit(self.layer_1, (0 - lomi.cameraX, 0 - lomi.cameraY))
		for y, row in enumerate(self.world_data):
			for x, tile in enumerate(row):
				if tile >= 1:
					display.blit(self.tile_list[tile], (x * 16 - lomi.cameraX , y * 16 - lomi.cameraY))
                #display.blit(self.small_items_surface, (x * self.tile_size ,y * self.tile_size))


	def update_layer_2(self, display):
		#display.blit(self.layer_1, (0 - lomi.cameraX, 0 - lomi.cameraY))
		for y, row in enumerate(self.world_data_layer_2):
			for x, tile in enumerate(row):
				if tile >= 1:
					display.blit(self.tile_list[tile], (x * 16 - lomi.cameraX , y * 16 - lomi.cameraY))
                #display.blit(self.small_items_surface, (x * self.tile_size ,y * self.tile_size))



map = MapClass()



#ITEM TAB PLACEHOLDER


class ClassPlaceHolder():
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.tab = False



        self.tile_image = []
        self.icon_image = []
        self.hover_image = []
        self.blit_tile = []
        #config
        self.config = ConfigParser()
        self.config.read("data/assets/pos.ini")


        self.hs_pos = self.config.getint("Assets Positions", "hs_pos")
        self.tr_pos = self.config.getint("Assets Positions", "tr_pos")
        self.bs_pos = self.config.getint("Assets Positions", "bs_pos")

        #self.bs_pos = self
        #self.rk_pos =


        self.button_rows = 4
        self.button_columns = 1
        self.button_width = 16
        self.button_height = 16
        self.buttons = []

        self.item_selected = 0

        for i in range(1, 5):
            image = pg.image.load(f"data/icons/icon- ({i}).png")
            image = pg.transform.scale(image, (self.button_width, self.button_height))
            self.icon_image.append(image)

        for i in range(1, 5):
            image = pg.image.load(f"data/icons/icon- ({i}).png")
            self.hover_image.append(image)

        for i in range(1, 8):
            image = pg.image.load(f"data/assets/asset- ({i}).png")
            self.tile_image.append(image)

        for row in range(self.button_rows):
            for col in range(self.button_columns):
                x = col * (self.button_width)
                y = row * (self.button_height)

                self.buttons.append({"rect": pg.Rect(x,y, self.button_width , self.button_height),
                 "posx":x, "posy":y,
                 "item":row

                 })


    def writePos(self):
        def update_pos():
            self.config.set("Assets Positions", "hs_pos", f"{mx,my}")
            self.config.set("Assets Positions", "tr_pos", f"{mx,my}")
            self.config.set("Assets Positions", "bs_pos", f"{mx,my}")

            with open("data/assets/pos.ini", "w") as config:
                self.config.write(config)

    def update(self, keyinput, display, mx , my, mouseinput):

        def placeholder():
            for button in self.buttons:

                if button["rect"].collidepoint(mx // 3 , my //3):
                    print("COLLIDEEDDD")
                    if mouseinput[0]:
                        self.item_selected = button["item"]


                pg.draw.rect(display, (255,255,255), button["rect"], 1)
                display.blit(self.icon_image[button["item"]],(button["posx"], button["posy"]))

            if mouseinput[0]:
                self.blit_tile.append([self.hover_image[self.item_selected], mx//3,my//3])

            display.blit(self.hover_image[self.item_selected], (mx //3 , my//3))


            for tile in self.blit_tile:
                display.blit(tile[0], (tile[1] - lomi.cameraX , tile[2] - lomi.cameraY ))
            #for i in range(0, self.item_selected):

        if keyinput[pg.K_e] and self.tab == False:
            self.tab = True
            print("tab true")
        #if keyinput[pg.K_e] and self.tab == True:
            #self.tab = False
            #print("tab false")


        if self.tab == True:
            placeholder()
            for button in self.buttons:
                print(mx, my, self.item_selected, button["posx"])


item = ClassPlaceHolder(0,0)
