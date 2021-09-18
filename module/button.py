import pygame 

# button class
class Button():
	def __init__(self, surface, x, y, size_x, size_y):
		self.rect = pygame.Rect((x, y), (size_x, size_y))
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface
		self.x = x
		self.y = y

	def draw(self):
		action = False

		# get mouse position
		pos = pygame.mouse.get_pos()

		# check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		sc = pygame.Surface((self.rect.width, self.rect.height))
		sc.fill((196, 196, 196))
		#draw button
		self.surface.blit(sc, (self.x, self.y))

		return action

def draw_text(surface, text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	surface.blit(img, (x, y))

def draw_bg(surface, background_img):
    surface.blit(background_img, (0, 0))