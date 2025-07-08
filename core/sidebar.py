import pygame
import pygame.freetype

class SideBar:
    def __init__(self, screen_w, screen_h, width=160):
        self.width = width
        self.rect = pygame.Rect(screen_w - width, 0, width, screen_h)
        self.elements = ["kotilum", "gejimtium"]
        self.grid_size = 88
        self.padding = 16
        self.scroll_offset = 0

        self.bg_color = (250, 250, 255)
        self.border_color = (210, 210, 225)
        self.font = pygame.freetype.SysFont("Roboto", 14)

        self.dragging_element = None
        self.drag_offset = (0, 0)

    def discover(self, element_name):
        if element_name not in self.elements:
            self.elements.append(element_name)

    def draw(self, screen):
        # Sidebar background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.line(screen, self.border_color, self.rect.topleft, self.rect.bottomleft, 2)

        clip = screen.get_clip()
        screen.set_clip(self.rect)

        for i, name in enumerate(self.elements):
            y = self.padding + i*(self.grid_size + self.padding) + self.scroll_offset
            x = self.rect.x + (self.width - self.grid_size)//2

            # Drop shadow
            shadow = pygame.Surface((self.grid_size, self.grid_size), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=12)
            screen.blit(shadow, (x + 4, y + 4))

            try:
                img = pygame.image.load(f"assets/{name}.png").convert_alpha()
                img = pygame.transform.smoothscale(img, (self.grid_size, self.grid_size))
                screen.blit(img, (x, y))
            except:
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(screen, (200, 200, 230), rect, border_radius=12)
                self.font.render_to(screen, (x+self.grid_size//2-6, y+self.grid_size//2-8), "?", (100, 100, 120))

            # Draw label
            self.font.render_to(screen,
                                 (x + self.grid_size//2 - len(name)*3, y + self.grid_size + 18),
                                 name, fgcolor=(100, 100, 120))

        screen.set_clip(clip)

    def handle_scroll(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            step = 48
            if event.y > 0:
                self.scroll_offset = min(self.scroll_offset + step, 0)
            elif event.y < 0:
                max_scroll = max(0, len(self.elements)*(self.grid_size+self.padding+20) - self.rect.height)
                self.scroll_offset = max(self.scroll_offset - step, -max_scroll)

    def start_drag(self, pos):
        if not self.rect.collidepoint(pos): return
        for i, name in enumerate(self.elements):
            y = self.padding + i*(self.grid_size + self.padding) + self.scroll_offset
            x = self.rect.x + (self.width - self.grid_size)//2
            rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
            if rect.collidepoint(pos):
                self.dragging_element = name
                self.drag_offset = (pos[0]-x, pos[1]-y)
                return

    def cancel_drag(self):
        self.dragging_element = None

    def get_dragged_element(self):
        if self.dragging_element:
            return self.dragging_element, self.drag_offset
        return None
