import pygame

pygame.init()
pygame.display.set_caption("chemymix")

background_color = (255, 255, 255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

class Element:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (width, height))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
            mouse_x, mouse_y = event.pos
            self.offset_x = self.rect.x - mouse_x
            self.offset_y = self.rect.y - mouse_y
            return True  # Indicate that this element was grabbed
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y
        return False

# Create elements
kotilum = Element(200, 150, 100, 100, "assets/kotilum.png")
gejimtium = Element(250, 180, 100, 100, "assets/gejimtium.png")
Core_gear = Element(300, 210, 100, 100, "assets/Core_gear.png")

elements = [kotilum, gejimtium, Core_gear]

# Main loop
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle dragging — only topmost one
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in reversed(range(len(elements))):  # From top to bottom
                if elements[i].handle_event(event):
                    # Bring clicked element to front
                    clicked = elements.pop(i)
                    elements.append(clicked)
                    break
        else:
            for e in elements:
                e.handle_event(event)

    for e in elements:
        e.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
