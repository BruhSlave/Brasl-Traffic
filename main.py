import pygame
from simulation import get_active_cars, lights, start_simulation, get_traffic_state, detection_zones

scale = 2.5

pygame.init()
screen = pygame.display.set_mode((1800, 1000))
pygame.display.set_caption("Traffic Simulation")
clock = pygame.time.Clock()
start_simulation()
font = pygame.font.SysFont(None, 42)

midX, midY = int(950 * scale), int(430 * scale)
laneGap = int(30 * scale)
roadLength = int(700 * scale)
road_width = 50  # Толщина полотна дорог
ROAD_COLOR = (136, 136, 136)
BG_COLOR = (220, 220, 220)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    # Дороги
    for dy in [-laneGap, laneGap]:
        pygame.draw.line(screen, ROAD_COLOR,
                         (int((midX - roadLength) / scale), int((midY + dy) / scale)),
                         (int((midX + roadLength) / scale), int((midY + dy) / scale)),
                         road_width)
    for dx in [-laneGap, laneGap]:
        pygame.draw.line(screen, ROAD_COLOR,
                         (int((midX + dx) / scale), int((midY - roadLength) / scale)),
                         (int((midX + dx) / scale), int((midY + roadLength) / scale)),
                         road_width)

    # Светофоры
    for light in lights:
        x, y = light.x, light.y
        if light.direction == 'horizontal':
            pygame.draw.rect(screen, (0, 255, 0) if light.is_green else (255, 0, 0),
                             pygame.Rect(int((x - 18) / scale), int((y - 120) / scale), int(36 / scale), int(36 / scale)))
        else:
            pygame.draw.rect(screen, (0, 255, 0) if light.is_green else (255, 0, 0),
                             pygame.Rect(int((x + 72) / scale), int((y - 18) / scale), int(36 / scale), int(36 / scale)))

    # Зоны детекторов
    cars = get_active_cars()
    for lid, zone in detection_zones.items():
        x1, y1, x2, y2 = zone
        rect = pygame.Rect(int(x1 / scale), int(y1 / scale), int((x2 - x1) / scale), int((y2 - y1) / scale))
        pygame.draw.rect(screen, (0, 0, 255), rect, 2)

        count = sum(x1 <= c.x <= x2 and y1 <= c.y <= y2 for c in cars if c.active)

        offset_y = 65 if lid != 'H2' else -140
        label = font.render(str(count), True, (0, 0, 0))
        screen.blit(label, (int(x1 / scale), int((y1 - offset_y) / scale)))

    # Таймеры светофоров
    def draw_dual_timer(light_group, pos):
        light = light_group[0]
        if light.is_green:
            green_left = int(light.green_duration - light.timer)
            red_left = light.red_duration
        else:
            green_left = light.green_duration
            red_left = int(light.red_duration - light.timer)

        green_text = font.render(f"G: {green_left}", True, (0, 128, 0))
        red_text = font.render(f"R: {red_left}", True, (180, 0, 0))

        screen.blit(green_text, (int(pos[0] / scale), int(pos[1] / scale)))
        screen.blit(red_text, (int(pos[0] / scale), int((pos[1] + 90) / scale)))

    horizontal_lights = [l for l in lights if l.direction == 'horizontal']
    vertical_lights = [l for l in lights if l.direction == 'vertical']

    draw_dual_timer(horizontal_lights, (midX - 330, midY + 180))
    draw_dual_timer(vertical_lights, (midX + 240, midY - 330))

    # Таймер трафика
    traffic_state, time_left = get_traffic_state()
    label_map = {'calm': 'Calm', 'peak_h': 'Rush →', 'peak_v': 'Rush ↓'}
    traffic_label = label_map.get(traffic_state, traffic_state)
    traffic_color = {'calm': (200, 200, 200), 'peak_h': (0, 100, 255), 'peak_v': (0, 180, 0)}[traffic_state]

    state_text = font.render(f"{traffic_label}", True, (0, 0, 0))
    timer_text = font.render(f"{int(time_left)}s", True, (0, 0, 0))

    state_rect = state_text.get_rect(topleft=(40, 40))
    timer_rect = timer_text.get_rect(topleft=(40, 70))

    box = state_rect.union(timer_rect).inflate(24, 24)
    pygame.draw.rect(screen, (255, 255, 255), box)
    pygame.draw.rect(screen, traffic_color, box, 3)

    screen.blit(state_text, state_rect)
    screen.blit(timer_text, timer_rect)

    # Машины
    for car in sorted(cars, key=lambda c: (c.y if c.path_type == 'vertical' else c.x)):
        x, y = int(car.x / scale), int(car.y / scale)
        ratio = car.speed / car.target_speed if car.target_speed > 0 else 0
        ratio = max(0.0, min(ratio, 1.0))

        if car.path_type == 'horizontal':
            r = int(255 * (1 - ratio))
            g = 0
            b = int(128 * ratio)
        else:
            r = int(255 * (1 - ratio))
            g = int(100 * ratio)
            b = 0

        color = (r, g, b)
        pygame.draw.circle(screen, color, (x, y), 12)

    legend_font = pygame.font.SysFont(None, 24)
    legend_x, legend_y = 500, 120
    line_spacing = 40

    # Красный сигнал
    pygame.draw.rect(screen, (255, 0, 0), (legend_x, legend_y, 20, 20))
    screen.blit(legend_font.render("Красный сигнал светофора", True, (0, 0, 0)), (legend_x + 30, legend_y + 2))

    # Зелёный сигнал
    pygame.draw.rect(screen, (0, 255, 0), (legend_x, legend_y + line_spacing, 20, 20))
    screen.blit(legend_font.render("Зелёный сигнал светофора", True, (0, 0, 0)), (legend_x + 30, legend_y + line_spacing + 2))

    # Зона детектора
    pygame.draw.rect(screen, (0, 0, 255), (legend_x, legend_y + 2 * line_spacing, 20, 20), 2)
    screen.blit(legend_font.render("Зона детектора трафика", True, (0, 0, 0)), (legend_x + 30, legend_y + 2 * line_spacing + 2))

    # Машина
    pygame.draw.circle(screen, (150, 150, 255), (legend_x + 10, legend_y + 3 * line_spacing + 10), 10)
    screen.blit(legend_font.render("Машина", True, (0, 0, 0)), (legend_x + 30, legend_y + 3 * line_spacing))

    # G: таймер
    g_text = legend_font.render("G: — Время до конца зелёного", True, (0, 128, 0))
    screen.blit(g_text, (legend_x, legend_y + 4 * line_spacing))

    # R: таймер
    r_text = legend_font.render("R: — Время до конца красного", True, (180, 0, 0))
    screen.blit(r_text, (legend_x, legend_y + 5 * line_spacing))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
