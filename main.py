import pygame

pygame.init()
pygame.display.set_caption("chemymix")

background_color = (255, 255, 255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# === Load Recipes from TXT ===
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

# === ELEMENT CLASS ===
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
            new_x = mx + self.offset_x
            new_y = my + self.offset_y

            # Keep inside screen bounds
            new_x = max(0, min(SCREEN_WIDTH - self.width, new_x))
            new_y = max(0, min(SCREEN_HEIGHT - self.height, new_y))

            self.rect.x = new_x
            self.rect.y = new_y
        return False

# === MIXING EFFECT ===
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

# === ELEMENTS AND EFFECTS ===
elements = [
    Element("kotilum", 200, 200, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", 400, 400, 100, 100, "assets/gejimtium.png")
]

effects = []

# === MAIN LOOP ===
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Dragging: only topmost element gets picked
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in reversed(range(len(elements))):
                if elements[i].handle_event(event):
                    clicked = elements.pop(i)
                    elements.append(clicked)
                    break
        else:
            for e in elements:
                e.handle_event(event)

    # === MIXING CHECK ===
    mixed = False
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            a, b = elements[i], elements[j]
            if a.rect.colliderect(b.rect):
                combo = frozenset([a.name, b.name])
                if combo in RECIPES:
                    result_name = RECIPES[combo]
                    print(f"{a.name} + {b.name} => {result_name}")

                    # Center position for new element & effect
                    mx = (a.rect.centerx + b.rect.centerx) // 2
                    my = (a.rect.centery + b.rect.centery) // 2

                    elements.remove(a)
                    elements.remove(b)

                    new_elem = Element(
                        result_name,
                        mx - 50, my - 50, 100, 100,
                        f"assets/{result_name}.png"
                    )
                    elements.append(new_elem)

                    # Add visual effect
                    effects.append(Effect(mx, my))

                    mixed = True
                    break
        if mixed:
            break

    # === DRAW ELEMENTS ===
    for e in elements:
        e.draw(screen)

    # === DRAW & UPDATE EFFECTS ===
    for fx in effects:
        fx.update()
        fx.draw(screen)
    effects = [e for e in effects if not e.is_done()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
