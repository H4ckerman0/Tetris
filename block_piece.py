import pygame
from block import Block
from settings import *

class BlockPiece():
    def __init__(self,x,y,type,obstacle_group):

        # Tetromino
        self.shapes = {
            "lL": [Block(x+42,y+42,"blue",(0,0)),Block(x+42,y,"blue",(42,42)),Block(x+42,y+84,"blue",(-42,-42)),Block(x,y+84,"blue",(0,-84))],
            "I": [Block(x,y+84,"cyan",(0,-42)),Block(x,y,"cyan",(84,42)),Block(x,y+42,"cyan",(42,0)),Block(x,y+126,"cyan",(-42,-84))],
            "rZ": [Block(x+42,y,"green",(0,0)),Block(x+84,y,"green",(-42,42)),Block(x,y+42,"green",(0,-84)),Block(x+42,y+42,"green",(-42,-42))],
            "rL": [Block(x,y+42,"orange",(0,0)),Block(x,y,"orange",(42,42)),Block(x,y+84,"orange",(-42,-42)),Block(x+42,y+84,"orange",(-84,0))],
            "T": [Block(x+42,y,"purple",(0,0)),Block(x,y,"purple",(42,-42)),Block(x+84,y,"purple",(-42,42)),Block(x+42,y+42,"purple",(-42,-42))],
            "lZ": [Block(x+42,y,"red",(0,0)),Block(x,y,"red",(42,-42)),Block(x+42,y+42,"red",(-42,-42)),Block(x+84,y+42,"red",(-84,0))],
            "O": [Block(x,y,"yellow",(0,0)),Block(x+42,y,"yellow",(0,0)),Block(x,y+42,"yellow",(0,0)),Block(x+42,y+42,"yellow",(0,0))],
            "X": [Block(x+42 ,y,"pink",(0,0)),Block(x,y+42,"pink",(0,0)),Block(x+42,y+42,"pink",(0,0)),Block(x+84,y+42,"pink",(0,0)),Block(x+42,y+84,"pink",(0,0))],
            ".": [Block(x ,y,"pink",(0,0))]
        }

        self.block_list = self.shapes[type]

        #Groups
        self.obstacle_group = obstacle_group

        # Movement
        self.direction = pygame.math.Vector2((0,0))
        self.speed = 42


        #Cooldowns
        self.moving = False
        self.move_time = 0
        self.move_cooldown = 150

        self.falling = None
        self.fall_time = 0
        self.fall_cooldown = 375

        self.spinning = None
        self.spin_time = 0
        self.spin_cooldown = 150

        self.pause_time = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if self.direction.y == 0:
                if keys[pygame.K_LEFT]:
                    self.direction.x = -1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks() - self.pause_time
                elif keys[pygame.K_RIGHT]:
                    self.direction.x = 1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks() - self.pause_time

            if self.direction.x == 0:
                if keys[pygame.K_DOWN]:
                    self.direction.y = 1
                    self.moving = True
                    self.move_time = pygame.time.get_ticks() - self.pause_time

        if not self.spinning:
            if keys[pygame.K_UP]:
                self.spinning = True
                self.spin_time = pygame.time.get_ticks() - self.pause_time
                self.spin()

    def is_collided(self,rect_list,rect_coll=False):
        return any(map(Block.is_collided,self.block_list,rect_list,[self.obstacle_group]*len(self.block_list),[rect_coll]*len(self.block_list)))

    def block_state_change(self,obstacle_group):
        touching = []
        for block in self.block_list:
            touching.append(any([block.rect.bottom == block2.rect.top and block.rect.x == block2.rect.x for block2 in obstacle_group]))

        return any([block.rect.bottom == SCREEN_HEIGHT for block in self.block_list]) or any(touching)

    def move(self):
        if not self.falling:
            self.direction.y = 1

            self.falling = True
            self.fall_time = pygame.time.get_ticks() - self.pause_time

        new_pos = [block.rect.topleft + self.direction * self.speed for block in self.block_list]

        if not self.is_collided(new_pos):
            for block in self.block_list:
                block.rect.topleft += self.direction * self.speed
        self.direction *= 0

    def spin(self):
        new_pos = [block.rect.topleft + block.offset for block in self.block_list]
        if not self.is_collided(new_pos):
            for block in self.block_list:
                block.spin()
        else:
            for i in range(1,3):
                if not self.is_collided([pos - (0,42*i) for pos in new_pos]):
                    for block in self.block_list:
                        block.spin()
                        block.rect.y -= 42 * i
                    break
                
    def collision(self):
        obst_coll_right = []
        obst_coll_left = []
        obst_coll_down = []

        for block1 in self.block_list:
            block1.coll_direction()

            # for block2 in self.obstacle_group:
            #     obst_coll_right.append(block1.rect.right > block2.rect.left and )

        if any([block.coll_right for block in self.block_list]):

            for block in self.block_list:
                block.rect.x += -42

        elif any([block.coll_left for block in self.block_list]):
            for block in self.block_list:
                block.rect.x += 42

        elif any([block.coll_bottom for block in self.block_list]):
            for block in self.block_list:
                block.rect.y -= 42

    def cooldowns(self):
        if self.moving:
            now = pygame.time.get_ticks()
            if now - self.move_time - self.pause_time >= self.move_cooldown:
                self.moving = False

        if self.falling:
            now = pygame.time.get_ticks()
            if now - self.fall_time - self.pause_time >= self.fall_cooldown:
                self.falling = False

        if self.spinning:
            now = pygame.time.get_ticks()
            if now - self.spin_time - self.pause_time >= self.spin_cooldown:
                self.spinning = False

    def update(self,pause_time):
        self.pause_time = pause_time
        self.input()
        self.move()
        self.collision()
        self.cooldowns()