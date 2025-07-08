import pygame

class Effect:
    def __init__(self, x, y, duration=15, color=(255, 100, 100), radius=40):
        self.x = x
        self.y = y
        self.duration = duration
        self.counter = 0
        self.color = color
        self.radius = radius

    def update(self):
        self.counter += 1

    def draw(self, screen):
        if self.counter < self.duration:
            alpha = max(0, 255 - (self.counter * 15))
            surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, alpha), (self.radius, self.radius), self.radius)
            screen.blit(surface, (self.x - self.radius, self.y - self.radius))

    def is_done(self):
        return self.counter >= self.duration
