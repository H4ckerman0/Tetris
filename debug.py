import pygame

pygame.init()

def debug(info,pos=(0,0)):
    display_surf = pygame.display.get_surface()
    font = pygame.font.Font(None,50)

    surf = font.render(str(info),True,"#FFFFFF")
    rect = surf.get_rect(topleft = pos)

    display_surf.blit(surf,rect)