import pygame
from simulation import get_active_cars, lights, start_simulation, get_traffic_state, detection_zones

pygame.init()
screen = pygame.display.set_mode((1800, 1000))
pygame.display.set_caption("Traffic Simulation")
clock = pygame.time.Clock()
start_simulation()
font = pygame.font.SysFont(None, 32)

# Центр перекрёстка
midX, midY = 950, 430
laneGap = 30
roadLength = 700
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
        pygame.draw.line(screen, ROAD_COLOR, (midX - roadLength, midY + dy), (midX + roadLength, midY + dy), 20)
    for dx in [-laneGap, laneGap]:
        pygame.draw.line(screen, ROAD_COLOR, (midX + dx, midY - roadLength), (midX + dx, midY + roadLength), 20)

    # Светофоры 
    for light in lights:
        x, y = light.x, light.y
        if light.direction == 'horizontal':
            pygame.draw.rect(screen, (0, 255, 0) if light.is_green else (255, 0, 0), (x - 6, y - 40, 12, 12))
        else:
            pygame.draw.rect(screen, (0, 255, 0) if light.is_green else (255, 0, 0), (x + 24, y - 6, 12, 12))

    # Зоны датчиков и счётчики
    cars = get_active_cars()
    for lid, zone in detection_zones.items():
        x1, y1, x2, y2 = zone
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        pygame.draw.rect(screen, (0, 0, 255), rect, 2)

        count = sum(x1 <= c.x <= x2 and y1 <= c.y <= y2 for c in cars if c.active)
        label = font.render(str(count), True, (0, 0, 0))
        screen.blit(label, (x1, y1 - 25))

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

        screen.blit(green_text, pos)
        screen.blit(red_text, (pos[0], pos[1] + 30))

    horizontal_lights = [l for l in lights if l.direction == 'horizontal']
    vertical_lights = [l for l in lights if l.direction == 'vertical']

    draw_dual_timer(horizontal_lights, (midX - 110, midY + 60))
    draw_dual_timer(vertical_lights, (midX + 80, midY - 110))

    # Таймер режима трафика (в углу)
    traffic_state, time_left = get_traffic_state()
    label_map = {
        'calm': 'Calm',
        'peak_h': 'Rush →',
        'peak_v': 'Rush ↓'
    }
    traffic_label = label_map.get(traffic_state, traffic_state)
    traffic_color = {
        'calm': (200, 200, 200),
        'peak_h': (0, 100, 255),
        'peak_v': (0, 180, 0)
    }[traffic_state]

    traffic_font = pygame.font.SysFont(None, 28)
    state_text = traffic_font.render(f"{traffic_label}", True, (0, 0, 0))
    timer_text = traffic_font.render(f"{int(time_left)}s", True, (0, 0, 0))

    state_rect = state_text.get_rect(topleft=(40, 40))
    timer_rect = timer_text.get_rect(topleft=(40, 70))

    box = state_rect.union(timer_rect).inflate(12, 12)
    pygame.draw.rect(screen, (255, 255, 255), box)
    pygame.draw.rect(screen, traffic_color, box, 3)

    screen.blit(state_text, state_rect)
    screen.blit(timer_text, timer_rect)

    # Машины
    for car in sorted(cars, key=lambda c: (c.y if c.path_type == 'vertical' else c.x)):
        x, y = int(car.x), int(car.y)
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
        pygame.draw.circle(screen, color, (x, y), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
