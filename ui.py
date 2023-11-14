import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.display_centerx = self.display_surf.get_size()[0]
        self.display_centery = self.display_surf.get_size()[1]

        self.font = pygame.font.Font(game_path + r"\font\slkscr.ttf",50)

        self.text_surf = self.font.render("Game paused",False,"white")
        self.text_rect = self.text_surf.get_rect(center = (self.display_centerx // 2, self.display_centery // 2))

    def display(self):
        self.display_surf.blit(self.text_surf,self.text_rect)
