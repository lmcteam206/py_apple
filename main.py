import pygame

pygame.init()
pygame.display.set_caption("chemymix")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.Clock()
running = True

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
