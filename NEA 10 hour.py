import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
size = 400,300
screen = pygame.display.set_mode(size,0,32)
pygame.display.set_caption('GAME')

sprite = pygame.image.load('Manic_Miner_MC.JFIF')
loop = True
while loop:
    screen.blit(sprite,(x,y))

    for event in pygame.event.get():
        if event.type == QUIT:
            loop = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 2
    if keys[pygame.K_RIGHT]:
        x += 2
    if keys[pygame.K_UP]:
        y -= 2
    if keys[pygame.K_DOWN]:
        y += 2    
        