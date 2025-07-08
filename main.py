import pygame
import pygame_gui

from core.element import Element
from core.effect import Effect
from core.recipes import load_recipes
from core.sidebar import SideBar

# === Initialization ===
pygame.init()
pygame.mixer.init()  # Sound engine
pygame.display.set_caption("Chemymix")

info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# === Load sounds ===
sound_spawn = pygame.mixer.Sound("assets/spawn.wav")
sound_mix = pygame.mixer.Sound("assets/mix.wav")
sound_delete = pygame.mixer.Sound("assets/trash.wav")

# === UI Buttons ===
close_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((SCREEN_WIDTH - 110, 10), (100, 40)),
    text='Close',
    manager=ui_manager,
    object_id="#close_button"
)

# === Sidebar & Trash ===
sidebar = SideBar(SCREEN_WIDTH, SCREEN_HEIGHT)
TRASH_SIZE = 100
trash_rect = pygame.Rect(20, SCREEN_HEIGHT - TRASH_SIZE - 20, TRASH_SIZE, TRASH_SIZE)
trash_icon = pygame.transform.smoothscale(pygame.image.load("assets/trash.png").convert_alpha(),
                                          (TRASH_SIZE, TRASH_SIZE))

# === Recipes & Game State ===
RECIPES = load_recipes("recipes.txt")
elements = [
    Element("kotilum", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 100, 100, "assets/kotilum.png"),
    Element("gejimtium", SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, 100, 100, "assets/gejimtium.png")
]
effects = []
running = True

# === Main Loop ===
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((242, 242, 247))  # Clean modern gray background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui_manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == close_button:
                pygame.quit()
                exit()

        if event.type == pygame.MOUSEWHEEL:
            sidebar.handle_scroll(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sidebar.start_drag(event.pos)
            for i in reversed(range(len(elements))):
                if elements[i].handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT):
                    elements.append(elements.pop(i))
                    break

        if event.type != pygame.MOUSEBUTTONDOWN:
            for e in elements:
                e.handle_event(event, SCREEN_WIDTH, SCREEN_HEIGHT)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            drag = sidebar.get_dragged_element()
            if drag:
                name, offset = drag
                mx, my = pygame.mouse.get_pos()
                elements.append(Element(name, mx - offset[0], my - offset[1], 100, 100, f"assets/{name}.png"))
                sidebar.cancel_drag()
                sound_spawn.play()

            # Trash check
            before = len(elements)
            elements = [e for e in elements if not trash_rect.colliderect(e.rect)]
            if len(elements) < before:
                sound_delete.play()

    # === Mixing Elements ===
    mixed = False
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            a, b = elements[i], elements[j]
            if a.rect.colliderect(b.rect):
                combo = frozenset([a.name, b.name])
                if combo in RECIPES:
                    result = RECIPES[combo]
                    mx, my = (a.rect.centerx + b.rect.centerx)//2, (a.rect.centery + b.rect.centery)//2
                    elements.remove(a); elements.remove(b)
                    elements.append(Element(result, mx-50, my-50, 100, 100, f"assets/{result}.png"))
                    sidebar.discover(result)
                    effects.append(Effect(mx, my))
                    sound_mix.play()
                    mixed = True
                    break
        if mixed:
            break

    # === Draw Phase ===
    for e in elements:
        e.draw(screen)

    for fx in effects:
        fx.update()
        fx.draw(screen)
    effects = [fx for fx in effects if not fx.is_done()]

    sidebar.draw(screen)

    # === Trash UI with hover highlight ===
    hover = trash_rect.collidepoint(pygame.mouse.get_pos())
    color = (255, 105, 105) if hover else (224, 224, 229)
    pygame.draw.rect(screen, color, trash_rect, border_radius=14)
    screen.blit(trash_icon, trash_rect.topleft)
    pygame.draw.rect(screen, (188, 0, 0), trash_rect, 2, border_radius=14)

    # === Ghost Drag ===
    drag = sidebar.get_dragged_element()
    if drag:
        name, offset = drag
        try:
            img = pygame.image.load(f"assets/{name}.png").convert_alpha()
            img = pygame.transform.smoothscale(img, (100, 100))
            ghost = img.copy(); ghost.set_alpha(140)
            mx, my = pygame.mouse.get_pos()
            screen.blit(ghost, (mx - offset[0], my - offset[1]))
        except: pass

    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
