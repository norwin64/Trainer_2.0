import csv

import pandas as pd
import pygame
import pygame as pg
import os
pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (161, 151, 142)
y_scroll =  280
scrolled = 0

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		#print(width, height)
		self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pg.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pg.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class scrollable_list():
	def __init__(self, data, x, y, width, height, font = None, font_color = BLACK, color_back=WHITE, color_scroll=GREY, color_frame=BLACK, border_width=5):
		self.data = data
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.font = font or pg.font.SysFont("maiandragd", 15)
		self.font_color = font_color
		self.color_back = color_back
		self.color_scroll = color_scroll
		self.color_frame = color_frame
		self.border_width = border_width

		self.y_text = self.y-scrolled

		# rect background
		self.rect_back = pg.Rect(x, y, width, height)

		#scroller
		self.x_scroll = self.x + 9 / 10 * self.width + 10

	def draw(self, surface):
		global y_scroll
		global count
		global scroll
		global scrolled
		pg.draw.rect(surface, self.color_back, self.rect_back)
		pg.draw.rect(surface, self.color_frame, self.rect_back, width=self.border_width)
		pg.draw.rect(surface, self.color_frame, pg.Rect(self.x+9/10*self.width, self.y, self.border_width, self.height))

		with open(f"{self.data}.csv", "r") as file:
			self.vocabs = csv.DictReader(file)
			for row in self.vocabs:
				overall =self.vocabs.line_num
				if self.y_text <= self.y+self.height-7/50*self.height:
					german_text = self.font.render(row.get("german_word")[0:25], True, self.font_color)
					english_text = self.font.render(row.get("english_word")[0:25], True, self.font_color)
					self.y_text += 24
					if self.y_text >= self.y:
						surface.blit(german_text, (self.x + 1 / 30 * self.width, self.y_text))
						surface.blit(english_text, (self.x + 15 / 30 * self.width, self.y_text))



		x = 15/overall	# factor for height of scroller
		left, middle, right = pg.mouse.get_pressed()
		scroller_rect = pygame.Rect(self.x_scroll, y_scroll, 1 / 10 * self.width - 20, self.height * x-60)

		for event in pg.event.get():
			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 4:
					scrolled -= 100
					y_scroll -= 100
				elif event.button == 5:
					scrolled += 100
					y_scroll += 100
				if y_scroll <= self.y + 30:
					y_scroll = self.y + 30
				elif y_scroll >= self.y + self.height - 30 - scroller_rect.height:
					y_scroll = self.y + self.height - 30 - scroller_rect.height
		if left:
			if scroller_rect.collidepoint(pg.mouse.get_pos()):
				scroll=True
			if scroll:
				y_scroll = pg.mouse.get_pos()[1]-scroller_rect.height/2
				scrolled += pg.mouse.get_rel()[1]/x
			if y_scroll <= self.y+30:
				y_scroll=self.y+30
			elif y_scroll>= self.y+self.height-30-scroller_rect.height:
				y_scroll=self.y+self.height-30-scroller_rect.height
		else:
			scroll=False
		scroller = pg.draw.rect(surface, self.color_scroll, scroller_rect)

		if scrolled <0:
			scrolled = 0
		if scrolled >=overall*100:
			scrolled = overall*100




