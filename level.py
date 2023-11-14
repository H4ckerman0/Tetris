import pygame
from random import choice,randint
from settings import *
from block_piece import BlockPiece
from ui import UI

pygame.init()

class Level:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.visible_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        #self.create_grid()

        self.bg_surf = pygame.image.load(game_path + r"\graphics\background.png").convert_alpha()
        self.bg_rect = self.bg_surf.get_rect(topleft = (0,0))

        self.game_paused = False

        self.game_over_sound = pygame.mixer.Sound(game_path + r"\audio\falschenentscheidung.mp3")

        self.ui = UI()

        self.changing = True
        self.change_cooldown = 500
        self.change_time = 0

        self.pause_time = 0
        self.pause_start = 0
        self.pause_end = 0

    def check_grid(self):
        rect = pygame.Rect(0,0,TILESIZE,TILESIZE)
        collisions = []
        for row in range(14,-1,-1):
            for col in range(12):
                y = row * TILESIZE
                x = col * TILESIZE
                rect.update(x,y,TILESIZE,TILESIZE)
                collisions.append(any([rect.colliderect(block.rect) for block in self.obstacle_group]))
            if len(set(collisions)) == 1 and True in collisions:
                for sprite in self.obstacle_group:
                    if sprite.rect.y == row * TILESIZE:
                        sprite.kill()
                    elif sprite.rect.y < row * TILESIZE:
                        sprite.rect.y += 42
            collisions.clear()

    def spawn_blocks(self):
        block_types = ["T","rL","lL","lZ","rZ","I","O","X"]
        if not self.visible_group.sprites():
            #self.block = Block1((choice(list(range(0,463,42))),-210),[self.visible_group],choice(block_types),self.obstacle_group)
            self.block_piece = BlockPiece(42*randint(0,9),-42,choice(block_types),self.obstacle_group)
            for sprite in self.block_piece.block_list:
                self.visible_group.add(sprite)

    def delete_blocks(self):
        for sprite in self.obstacle_group:
            if sprite.rect.top < self.display_surf.get_rect(topleft= (0,0)).top:
                self.game_paused = True
                pygame.mixer.stop()
                self.game_over_sound.play()

    def change_block_state(self):

        # if (self.block.rect.bottom == SCREEN_HEIGHT or self.block.collided) and not self.change_time:
        #     self.change_time = pygame.time.get_ticks()


        # if not self.changing:
        #     if self.block.rect.bottom == SCREEN_HEIGHT or self.block.collided:
        #         self.visible_group.remove(self.block)
        #         self.obstacle_group.add(self.block)
        #         self.block.collided = False

        #         self.changing = True
        #         self.change_time -= self.change_time

        #     else:
        #         self.changing = True
        #         self.change_time -= self.change_time
        for block in self.block_piece.block_list:
            self.visible_group.remove(block)
            self.obstacle_group.add(block)

    def cooldowns(self):
        if self.block_piece.block_state_change(self.obstacle_group) and not self.change_time:
            self.change_time = pygame.time.get_ticks() - self.pause_time
            self.changing = self.block_piece.block_state_change(self.obstacle_group)

        if self.changing and self.change_time:
            now = pygame.time.get_ticks()
            for block in self.block_piece.block_list:
                block.alpha -= 6
                block.update_alpha()

            if now - self.change_time - self.pause_time > self.change_cooldown and self.block_piece.block_state_change(self.obstacle_group):
                for block in self.block_piece.block_list:
                    block.alpha = 255
                    block.update_alpha()
                self.change_block_state()
                self.changing = False
                self.change_time -= self.change_time

            elif not self.block_piece.block_state_change(self.obstacle_group):
                self.changing = False
                self.change_time -= self.change_time
                for block in self.block_piece.block_list:
                    block.alpha = 255
                    block.update_alpha()

    def toggle_menu(self):
        self.game_paused = not self.game_paused

        if self.game_paused:
            self.pause_start = pygame.time.get_ticks()
        else:
            self.pause_end = pygame.time.get_ticks()
            self.pause_time += self.pause_end - self.pause_start

    def run(self):
        if self.game_paused:
            self.ui.display()
            
        else:
            self.delete_blocks()
            self.spawn_blocks()
            self.display_surf.blit(self.bg_surf,self.bg_rect)
            self.visible_group.draw(self.display_surf)
            self.obstacle_group.draw(self.display_surf)
            self.cooldowns()
            self.visible_group.update()
            self.block_piece.update(self.pause_time)
            self.check_grid()