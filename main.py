import pygame
import pygame_gui

from core.element import Element
from core.effect import Effect
from core.recipes import load_recipes
from core.sidebar import SideBar

# === Initialize Pygame ===
pygame.init()
pygame.display.set_caption("Chemymix")

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# === UI Elements ===
close_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 110, 10), (100, 40)),
    text='Close',
    manager=ui_manager
)

# === Sidebar ===
sidebar = SideBar(SCREEN_WIDTH, SCREEN_HEIGHT)

# === Trash Area ===
TRASH_SIZE = 100
trash_rect = pygame.Rect(20, SCREEN_HEIGHT - TRASH_SIZE - 20, TRASH_SIZE, TRASH_SIZE)
trash_icon = pygame.transform.scale(pygame.image.load("assets/trash.png"), (TRASH_SIZE, TRASH_SIZE))

# === Recipes & Elements ===
RECIPES = load_recipes("recipes.txt")
elements = [
    Element("kotilum", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, 100, 100, "assets/gejimtium.png")
]
effects = []

# === Dragging State ===
drag_preview = None  # (name, offset)
running = True

# === Main Game Loop ===
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((255, 255, 255))  # Clean white background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui_manager.process_events(event)

        # Close Button
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == close_button:
                pygame.quit()
                exit()

        # Sidebar scroll
        if event.type == pygame.MOUSEWHEEL:
            sidebar.handle_scroll(event)

        # Start drag from sidebar
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sidebar.start_drag(event.pos)
            # Also bring clicked elements to front
            for i in reversed(range(len(elements))):
                if elements[i].handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT):
                    elements.append(elements.pop(i))
                    break

        # Element dragging (outside sidebar)
        if event.type != pygame.MOUSEBUTTONDOWN:
            for e in elements:
                e.handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Drop new element
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drag_result = sidebar.get_dragged_element()
            if drag_result:
                name, offset = drag_result
                mx, my = pygame.mouse.get_pos()
                elements.append(Element(name, mx - offset[0], my - offset[1], 100, 100, f"assets/{name}.png"))
                sidebar.cancel_drag()

            # Delete elements dropped on trash
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
                    elements.append(Element(result, mx - 50, my - 50, 100, 100, f"assets/{result}.png"))
                    sidebar.discover(result)
                    effects.append(Effect(mx, my))
                    mixed = True
                    break
        if mixed:
            break

    # === Drawing Phase ===
    for e in elements:
        e.draw(screen)

    # Effects
    for fx in effects:
        fx.update()
        fx.draw(screen)
    effects = [fx for fx in effects if not fx.is_done()]

    # Sidebar
    sidebar.draw(screen)

    # Trash area (highlight if dragging over)
    mouse_pos = pygame.mouse.get_pos()
    if trash_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 100, 100), trash_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, (220, 220, 220), trash_rect, border_radius=10)
    screen.blit(trash_icon, trash_rect.topleft)
    pygame.draw.rect(screen, (200, 0, 0), trash_rect, 2, border_radius=10)

    # Drag preview (ghost image)
    drag_result = sidebar.get_dragged_element()
    if drag_result:
        name, offset = drag_result
        try:
            img = pygame.image.load(f"assets/{name}.png").convert_alpha()
            img = pygame.transform.smoothscale(img, (100, 100))
            ghost = img.copy()
            ghost.set_alpha(160)
            mx, my = pygame.mouse.get_pos()
            screen.blit(ghost, (mx - offset[0], my - offset[1]))
        except:
            pass

    # UI
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
