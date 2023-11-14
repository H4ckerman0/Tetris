import pygame
from debug import debug
from settings import *

pygame.init()

class Block1(pygame.sprite.Sprite):
    def __init__(self,pos,groups,type,obstacle_group):
        super().__init__(groups)
        self.image = pygame.image.load(block_data[type])
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.display_surf = pygame.display.get_surface()
        self.display_rect = self.display_surf.get_rect()
        self.display_rect_resized = self.display_rect.inflate(0,210)
        self.display_rect_resized.bottom = self.display_rect.bottom

        self.direction = pygame.math.Vector2((0,0))
        self.speed =  42
        self.spin_offset = pygame.math.Vector2((0,0))

        self.alpha = 255

        self.obstacle_group = obstacle_group

        self.moving = None
        self.move_cooldown = 150
        self.move_time = 0

        self.falling = None
        self.fall_cooldown = 1000
        self.fall_time = 0

        self.spinning = None
        self.spin_cooldown = 500
        self.spin_time = 0

        if type in ["T-piece","rZ-piece"]:
            self.spin_offset = pygame.math.Vector2((-21,-21))
        elif type == "rL-piece":
            self.spin_offset = pygame.math.Vector2((-21,21))
        elif type == "lL-piece":
            self.spin_offset = pygame.math.Vector2((21,-21))
        elif type in ["lZ-piece","I-piece"]:
            self.spin_offset = pygame.math.Vector2((21,21))

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if self.direction.y == 0:
                if keys[pygame.K_LEFT]:
                    self.direction.x = -1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks()
                elif keys[pygame.K_RIGHT]:
                    self.direction.x = 1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks()

            if self.direction.x == 0:
                if keys[pygame.K_DOWN]:
                    self.direction.y = 1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks()

        if not self.spinning:
            if keys[pygame.K_UP]:
                self.spinning = True
                self.spin_time = pygame.time.get_ticks()
                self.spin()

    def update_alpha(self):
        self.image.set_alpha(self.alpha)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if not self.falling:
            self.direction.y = 1
            self.rect.y += self.direction.y * self.speed

            self.falling = True
            self.fall_time = pygame.time.get_ticks()

            self.collision("vertical")
            self.direction.y = 0

        self.rect.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.direction.x = 0

        self.rect.y += self.direction.y * self.speed
        self.collision("vertical")
        self.direction.y = 0

    def spin(self):
        self.image = pygame.transform.rotate(self.image,-90)

        pos = self.rect.center + self.spin_offset
        self.spin_offset.rotate_ip(90)

        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.collision("rotate")

    def collision(self,direction=None):
        self.rect.clamp_ip(self.display_rect_resized)

        if pygame.sprite.spritecollide(self,self.obstacle_group,False):
            while pygame.sprite.spritecollide(self,self.obstacle_group,False,pygame.sprite.collide_mask):
                if direction == "vertical":
                    if self.direction.y > 0: self.rect.y -= 42
                    elif self.direction.y < 0: self.rect.y += 42

                elif direction == "horizontal":
                    if self.direction.x < 0: self.rect.x += 42
                    elif self.direction.x > 0: self.rect.x -= 42
                
                if int(self.direction.x) == 0 and int(self.direction.y) == 0 or direction == "rotate":
                    self.rect.y -= 42

    def change_state(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            return True

        for sprite in self.obstacle_group.sprites():
            touching = self.rect.bottom == sprite.rect.top and self.rect.left < sprite.rect.right and self.rect.right > sprite.rect.left

            if touching or pygame.sprite.spritecollide(self,self.obstacle_group,False):
                offsetx = self.rect.left - sprite.rect.left
                offsety = (self.rect.top + 1) - sprite.rect.top

                if sprite.mask.overlap(self.mask,(offsetx,offsety)):
                    return True

        return False

    def cooldowns(self):
        if self.moving:
            now = pygame.time.get_ticks()
            if now - self.move_time >= self.move_cooldown:
                self.moving = False

        if self.falling:
            now = pygame.time.get_ticks()
            if now - self.fall_time >= self.fall_cooldown:
                self.falling = False

        if self.spinning:
            now = pygame.time.get_ticks()
            if now - self.spin_time >= self.spin_cooldown:
                self.spinning = False

    def update(self):
        self.update_alpha()
        self.input()
        self.move()
        self.cooldowns()
        self.collision()