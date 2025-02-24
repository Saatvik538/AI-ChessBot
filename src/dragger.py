import pygame
from const import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.inital_row = 0
        self.inital_col = 0

    # blit method

    def update_blit(self, surface):
        #texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        #image
        img = pygame.image.load(texture)

        #rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)
        #blit
        surface.blit(img, self.piece.texture_rect)

    #other methods
    def update_mouse(self, position):
        self.mouseX, self.mouseY = position #(xcor, ycor)

    def save_inital(self, pos):
        self.inital_row = pos[1] // SQSIZE
        self.inital_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
    