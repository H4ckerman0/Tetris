import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,color,offset):
        super().__init__()
        self.image = pygame.image.load(block_data[color])
        self.rect = self.image.get_rect(topleft = (x,y))

        self.alpha = 255

        self.offset = pygame.math.Vector2((offset))

        self.display = pygame.display.get_surface()

    def is_collided(self,pos,obstacle,rect_coll=False):
        new_rect = self.rect.copy()
        new_rect.topleft = pos

        if any([new_rect.colliderect(obst.rect) for obst in obstacle]):
            return True

        if not rect_coll:
            if pos[0] > SCREEN_WIDTH - TILESIZE or pos[0] < 0 or pos[1] >= SCREEN_HEIGHT:
                return True

            return False

    def spin(self):
        self.rect.center += self.offset
        self.offset.rotate_ip(90)
        
        return self.rect

    def coll_direction(self):
        self.coll_right = self.rect.right > SCREEN_WIDTH
        self.coll_left = self.rect.left < 0
        self.coll_bottom = self.rect.bottom > SCREEN_HEIGHT

    def update_alpha(self):
        self.image.set_alpha(self.alpha)

    def update(self):
        self.coll_direction()