import pygame

pygame.init()
pygame.display.set_caption("chemymix")

background_color = (255, 255, 255)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# === MIXING RECIPES ===
RECIPES = {
    frozenset(["kotilum", "gejimtium"]): "Core_gear",

}

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
            self.rect.x = mx + self.offset_x
            self.rect.y = my + self.offset_y
        return False

# === INITIAL ELEMENTS ===
elements = [
    Element("kotilum", 200, 150, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", 400, 180, 100, 100, "assets/gejimtium.png"),
]

# === MAIN LOOP ===
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle dragging — only topmost one
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

                    # Center point
                    mx = (a.rect.centerx + b.rect.centerx) // 2
                    my = (a.rect.centery + b.rect.centery) // 2

                    # Remove old elements
                    elements.remove(a)
                    elements.remove(b)

                    # Create new result element
                    result_element = Element(
                        result_name,
                        mx - 50, my - 50, 100, 100,
                        f"assets/{result_name}.png"
                    )
                    elements.append(result_element)

                    mixed = True
                    break
        if mixed:
            break

    for e in elements:
        e.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
