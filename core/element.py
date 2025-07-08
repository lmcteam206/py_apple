import pygame

class Element:
    def __init__(self, name, x, y, w, h, image_path):
        self.name = name
        self.rect = pygame.Rect(x, y, w, h)
        original = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original, (w, h))
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.width = w
        self.height = h

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event, screen_w, screen_h):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
            mx, my = event.pos
            self.offset_x = self.rect.x - mx
            self.offset_y = self.rect.y - my
            return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            new_x = max(0, min(screen_w - self.width, mx + self.offset_x))
            new_y = max(0, min(screen_h - self.height, my + self.offset_y))
            self.rect.x = new_x
            self.rect.y = new_y
        return False
