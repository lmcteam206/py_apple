import pygame

pygame.init()
pygame.display.set_caption("chemymix")

background_color = (255,255,255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.Clock()
running = True

class Element:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, height))
        
        # Dragging state
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    
element = Element(200, 150, 100, 100, "assets/kotilum.png") 

elements = [

]

while running:
    screen.fill(background_color)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        for e in element:
            e.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
    for e in elements
    element.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
