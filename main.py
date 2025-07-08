import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption("chemymix")

# === Get Screen Size (Responsive) ===
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

background_color = (255, 255, 255)
clock = pygame.time.Clock()
running = True

# === UI Manager ===
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# === Close Button (top-right) ===
close_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 110, 10), (100, 40)),
    text='Close',
    manager=ui_manager
)

# === Load Recipes ===
def load_recipes(filename):
    recipes = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            left, result = line.split('=')
            ingredients = [x.strip() for x in left.split('+')]
            result = result.strip()
            recipes[frozenset(ingredients)] = result
    return recipes

RECIPES = load_recipes("recipes.txt")

# === Element Class ===
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

    def handle_event(self, event):
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
            new_x = max(0, min(SCREEN_WIDTH - self.width, mx + self.offset_x))
            new_y = max(0, min(SCREEN_HEIGHT - self.height, my + self.offset_y))
            self.rect.x = new_x
            self.rect.y = new_y
        return False

# === Effect Class ===
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

# === Init Elements & Effects ===
elements = [
    Element("kotilum", SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2, 100, 100, "assets/gejimtium.png")
]
effects = []

# === Main Game Loop ===
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle pygame_gui events
        ui_manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == close_button:
                    pygame.quit()
                    exit()

        # Handle dragging — only topmost
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in reversed(range(len(elements))):
                if elements[i].handle_event(event):
                    clicked = elements.pop(i)
                    elements.append(clicked)
                    break
        else:
            for e in elements:
                e.handle_event(event)

    # === Mixing Check ===
    mixed = False
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            a, b = elements[i], elements[j]
            if a.rect.colliderect(b.rect):
                combo = frozenset([a.name, b.name])
                if combo in RECIPES:
                    result_name = RECIPES[combo]
                    mx = (a.rect.centerx + b.rect.centerx) // 2
                    my = (a.rect.centery + b.rect.centery) // 2
                    elements.remove(a)
                    elements.remove(b)
                    elements.append(Element(
                        result_name,
                        mx - 50, my - 50, 100, 100,
                        f"assets/{result_name}.png"
                    ))
                    effects.append(Effect(mx, my))
                    mixed = True
                    break
        if mixed:
            break

    # === Draw All ===
    for e in elements:
        e.draw(screen)

    for fx in effects:
        fx.update()
        fx.draw(screen)
    effects = [e for e in effects if not e.is_done()]

    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
