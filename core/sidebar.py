import pygame
from core.element import Element

class SideBar:
    def __init__(self, screen_w, screen_h, width=120):
        self.width = width
        self.rect = pygame.Rect(screen_w - width, 0, width, screen_h)
        self.elements = ["kotilum","gejimtium"]  # Names only, no Element objects
        self.grid_size = 100
        self.padding = 10

    def discover(self, element_name):
        if element_name not in self.elements:
            self.elements.append(element_name)

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 230, 230), self.rect)
        for index, name in enumerate(self.elements):
            y = self.padding + index * (self.grid_size + self.padding)
            try:
                image = pygame.image.load(f"assets/{name}.png").convert_alpha()
                image = pygame.transform.scale(image, (self.grid_size, self.grid_size))
                screen.blit(image, (self.rect.x + 10, y))
            except:
                continue  # Missing image

    def handle_click(self, pos):
        if not self.rect.collidepoint(pos):
            return None

        for index, name in enumerate(self.elements):
            y = self.padding + index * (self.grid_size + self.padding)
            element_rect = pygame.Rect(self.rect.x + 10, y, self.grid_size, self.grid_size)
            if element_rect.collidepoint(pos):
                return name
        return None
