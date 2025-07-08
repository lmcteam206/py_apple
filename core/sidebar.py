import pygame

class SideBar:
    def __init__(self, screen_w, screen_h, width=140):
        self.width = width
        self.rect = pygame.Rect(screen_w - width, 0, width, screen_h)
        self.elements = ["kotilum", "gejimtium"]
        self.grid_size = 96
        self.padding = 12
        self.scroll_offset = 0

        # Style
        self.bg_color = (245, 245, 245)
        self.border_color = (200, 200, 200)
        self.font = pygame.font.SysFont("arial", 14)

        # Drag logic
        self.dragging_element = None
        self.drag_offset = (0, 0)

    def discover(self, element_name):
        if element_name not in self.elements:
            self.elements.append(element_name)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.line(screen, self.border_color, self.rect.topleft, self.rect.bottomleft, 2)

        original_clip = screen.get_clip()
        screen.set_clip(self.rect)

        for i, name in enumerate(self.elements):
            y = self.padding + i * (self.grid_size + self.padding) + self.scroll_offset
            x = self.rect.x + (self.width - self.grid_size) // 2

            try:
                image = pygame.image.load(f"assets/{name}.png").convert_alpha()
                image = pygame.transform.smoothscale(image, (self.grid_size, self.grid_size))
                screen.blit(image, (x, y))
            except Exception:
                pygame.draw.rect(screen, (200, 200, 200), (x, y, self.grid_size, self.grid_size), border_radius=8)
                err = self.font.render("?", True, (100, 100, 100))
                screen.blit(err, (x + self.grid_size // 2 - 5, y + self.grid_size // 2 - 7))

            label = self.font.render(name, True, (50, 50, 50))
            label_rect = label.get_rect(center=(x + self.grid_size // 2, y + self.grid_size + 14))
            screen.blit(label, label_rect)

        screen.set_clip(original_clip)

    def handle_scroll(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            scroll_step = 40
            if event.y > 0:
                self.scroll_offset = min(self.scroll_offset + scroll_step, 0)
            elif event.y < 0:
                max_scroll = max(0, len(self.elements) * (self.grid_size + self.padding + 20) - self.rect.height)
                self.scroll_offset = max(self.scroll_offset - scroll_step, -max_scroll)

    def start_drag(self, pos):
        """Call this on MOUSEBUTTONDOWN."""
        if not self.rect.collidepoint(pos):
            return

        for i, name in enumerate(self.elements):
            y = self.padding + i * (self.grid_size + self.padding) + self.scroll_offset
            x = self.rect.x + (self.width - self.grid_size) // 2
            rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
            if rect.collidepoint(pos):
                self.dragging_element = name
                self.drag_offset = (pos[0] - x, pos[1] - y)
                return

    def cancel_drag(self):
        self.dragging_element = None

    def get_dragged_element(self):
        """Returns (name, offset) while dragging, else None"""
        if self.dragging_element:
            return self.dragging_element, self.drag_offset
        return None
