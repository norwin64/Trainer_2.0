import csv

import pandas as pd
import pygame
import pygame as pg
import os
pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (201, 190, 180)

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

def blit_text(surface, text, pos, font, color=BLACK, border=50):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    lines = 1
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width-border:
                x = pos[0]  # Reset the x.
                y += word_height + 4  # Start on new row.
                lines += 1
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


arrow_down = pygame.transform.scale(pygame.image.load(os.path.join("materials", "arrow_down.png")), (20, 20))
arrow_up = pygame.transform.scale(pygame.image.load(os.path.join("materials", "arrow_up.png")), (20, 20))


class ScrollBar():
	def __init__(self, data, font, Rect, font_color = BLACK, color_back=WHITE, color_scroll=GREY, color_frame=BLACK):
		self.rect = Rect
		self.data = data
		self.font = font
		self.font_color = font_color
		self.color_frame = color_frame
		self.color_back = color_back
		self.color_scroll = color_scroll
		self.y_scroll = self.rect[1] + 30
		self.x, self.y, self.width, self.height = self.rect

		self.arrow_up_button = Button(self.x+self.width-30+5, self.y+5, arrow_up, 1)
		self.arrow_down_button = Button(self.x + self.width - 30+5, self.y+self.height-30+5, arrow_down, 1)

	def draw(self, surface):

		# Draw frame
		pg.draw.rect(surface, self.color_back, self.rect)
		pg.draw.rect(surface, self.color_frame, self.rect, width=3)
		pg.draw.line(surface, self.color_frame, (self.rect[0]+self.rect[2]-30, self.rect[1]), (self.rect[0]+self.rect[2]-30, self.rect[1]+self.rect[3]), width=2)

		# Draw elements in area
		index = -5
		for element in self.data:
			if self.y+20*index+30 <= self.y+self.height and self.y+20*index >= self.y:
				surface.blit(self.font.render(element.get("german_word"), True, self.font_color), (self.x+20, self.y+20*index))
				index += 1
		
		# draw Scroll box
		height_scroll = (self.height - 60) * (index / len(self.data))
		pg.draw.rect(surface, self.color_scroll, pg.Rect(self.rect[0] + self.rect[2] - 27, self.y_scroll, 23, height_scroll))
		pg.draw.rect(surface, self.color_frame,pg.Rect(self.rect[0] + self.rect[2] - 27, self.y_scroll, 23, height_scroll), width=1)

		# Draw arrows up /down
		if self.arrow_up_button.draw(surface):
			pass
		if self.arrow_down_button.draw(surface):
			pass




