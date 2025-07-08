import pygame
import pygame_gui

from core.element import Element
from core.effect import Effect
from core.recipes import load_recipes
from core.sidebar import SideBar

pygame.init()
pygame.display.set_caption("chemymix")

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

background_color = (255, 255, 255)
clock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# === Close Button ===
close_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 110, 10), (100, 40)),
    text='Close',
    manager=ui_manager
)

# === Sidebar ===
sidebar = SideBar(SCREEN_WIDTH, SCREEN_HEIGHT)

# === Trash Area ===
trash_rect = pygame.Rect(20, SCREEN_HEIGHT - 120, 100, 100)
trash_icon = pygame.transform.scale(pygame.image.load("assets/trash.png"), (100, 100))

# === Recipes ===
RECIPES = load_recipes("recipes.txt")

# === Game Elements ===
elements = [
    Element("kotilum", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, 100, 100, "assets/gejimtium.png")
]

effects = []
running = True

while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # UI events
        ui_manager.process_events(event)

        # Close button logic
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == close_button:
                pygame.quit()
                exit()

        # Scroll wheel for sidebar
        if event.type == pygame.MOUSEWHEEL:
            sidebar.handle_scroll(event)

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            element_name = sidebar.handle_click(event.pos)
            if element_name:
                elements.append(Element(
                    element_name, 100, 100, 100, 100, f"assets/{element_name}.png"
                ))
            else:
                # Dragging elements
                for i in reversed(range(len(elements))):
                    if elements[i].handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT):
                        clicked = elements.pop(i)
                        elements.append(clicked)
                        break
        else:
            for e in elements:
                e.handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT)

        # On mouse release, check for trash drop
        if event.type == pygame.MOUSEBUTTONUP:
            elements = [e for e in elements if not trash_rect.colliderect(e.rect)]

    # === Mixing Logic ===
    mixed = False
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            a, b = elements[i], elements[j]
            if a.rect.colliderect(b.rect):
                combo = frozenset([a.name, b.name])
                if combo in RECIPES:
                    result = RECIPES[combo]
                    mx = (a.rect.centerx + b.rect.centerx) // 2
                    my = (a.rect.centery + b.rect.centery) // 2
                    elements.remove(a)
                    elements.remove(b)
                    elements.append(Element(
                        result, mx - 50, my - 50, 100, 100, f"assets/{result}.png"
                    ))
                    sidebar.discover(result)
                    effects.append(Effect(mx, my))
                    mixed = True
                    break
        if mixed:
            break

    # === Drawing ===
    for e in elements:
        e.draw(screen)

    for fx in effects:
        fx.update()
        fx.draw(screen)
    effects = [fx for fx in effects if not fx.is_done()]

    # Sidebar and Trash
    sidebar.draw(screen)
    screen.blit(trash_icon, trash_rect.topleft)
    pygame.draw.rect(screen, (200, 0, 0), trash_rect, 2)

    # UI
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
