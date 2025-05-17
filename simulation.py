import time
import threading
import random
from geometry import build_paths, center_x, center_y, lane_gap
from models import Car, TrafficLight

paths = build_paths()
cars = []
car_id_counter = 0
spawn_timer = 0

# Светофоры
lights = [
    TrafficLight('H1', (center_x - 60, 420), 'horizontal'),
    TrafficLight('H2', (center_x - 60, 480), 'horizontal'),
    TrafficLight('V1', (center_x - lane_gap - 13, center_y - 60), 'vertical'),
    TrafficLight('V2', (center_x + lane_gap - 13, center_y - 60), 'vertical'),
]

# Зоны детекторов трафика 
detection_zones = {
    'H1': (center_x - 600, center_y - lane_gap - 10, center_x - 70, center_y - lane_gap + 10),  
    'H2': (center_x - 600, center_y + lane_gap - 10, center_x - 70, center_y + lane_gap + 10), 
    'V1': (center_x - lane_gap - 10, center_y - 380, center_x - lane_gap + 10, center_y - 65),
    'V2': (center_x + lane_gap - 10, center_y - 380, center_x + lane_gap + 10, center_y - 65),
}

def count_cars_in_zone(zone):
    x1, y1, x2, y2 = zone
    return sum(x1 <= c.x <= x2 and y1 <= c.y <= y2 for c in cars if c.active)

# Фаза светофора
light_phase_timer = 0
light_phase_duration = 5
current_phase = 'horizontal'

# Фазы трафика
traffic_cycle = ['calm', 'peak_h', 'peak_v']
traffic_state_index = 0
traffic_timer = 0
traffic_duration_map = {'calm': 15, 'peak_h': 30, 'peak_v': 30}

def switch_phase():
    global current_phase
    current_phase = 'vertical' if current_phase == 'horizontal' else 'horizontal'
    for light in lights:
        light.is_green = (light.direction == current_phase)
        light.timer = 0  # сброс таймера при переключении

def is_blocked(car, light):
    if light.direction != car.path_type or light.is_green:
        return False
    if car.path_type == 'horizontal':
        aligned_y = abs(car.y - light.y) < 25
        ahead = light.x - car.x
        return aligned_y and 0 < ahead < 100
    else:
        aligned_x = abs(car.x - light.x) < 15
        ahead = light.y - car.y
        return aligned_x and 0 < ahead < 100

def get_traffic_state():
    current_mode = traffic_cycle[traffic_state_index]
    return current_mode, traffic_duration_map[current_mode] - traffic_timer

def simulation_loop():
    global spawn_timer, car_id_counter, light_phase_timer, traffic_state_index, traffic_timer

    while True:
        dt = random.uniform(0.01, 0.05)

        # 🔧 Обновляем таймеры для отображения G:/R:
        for light in lights:
            light.timer += dt

        # === Адаптивная настройка фаз ===
        if current_phase == 'horizontal':
            relevant_ids = ['H1', 'H2']
        else:
            relevant_ids = ['V1', 'V2']

        max_count = 0
        for lid in relevant_ids:
            zone = detection_zones.get(lid)
            if not zone:
                continue
            count = count_cars_in_zone(zone)
            max_count = max(max_count, count)

        if max_count >= 8:
            phase_green = 12
        elif max_count >= 5:
            phase_green = 9
        elif max_count >= 3:
            phase_green = 7
        else:
            phase_green = 5

        # Обновляем фазу
        light_phase_timer += dt
        if light_phase_timer >= phase_green:
            light_phase_timer = 0
            switch_phase()

        # Обновляем фазу трафика
        traffic_timer += dt
        current_mode = traffic_cycle[traffic_state_index]
        duration = traffic_duration_map[current_mode]

        if traffic_timer >= duration:
            traffic_timer = 0
            traffic_state_index = (traffic_state_index + 1) % len(traffic_cycle)

        traffic_state = traffic_cycle[traffic_state_index]

        # Спавн машин
        spawn_timer += dt
        spawn_threshold = 1.5
        spawn_multiplier = 1

        if traffic_state in ['peak_h', 'peak_v']:
            spawn_threshold = 0.4
            spawn_multiplier = 2

        if spawn_timer >= spawn_threshold:
            spawn_timer = 0
            for _ in range(spawn_multiplier):
                if traffic_state == 'peak_h':
                    path_index = random.choices([0, 1, 2, 3], weights=[4, 4, 1, 1])[0]
                elif traffic_state == 'peak_v':
                    path_index = random.choices([0, 1, 2, 3], weights=[1, 1, 4, 4])[0]
                else:
                    path_index = random.randint(0, 3)

                spawn_x, spawn_y = paths[path_index][0]
                path_type = 'horizontal' if path_index < 2 else 'vertical'

                too_close = any(
                    c.active and c.path == paths[path_index] and
                    (abs(c.x - spawn_x) if path_type == 'horizontal' else abs(c.y - spawn_y)) < 12
                    for c in cars
                )

                if not too_close:
                    new_car = Car(car_id_counter, paths[path_index], path_type)
                    cars.append(new_car)
                    car_id_counter += 1

        # Обработка движения машин
        for car in cars:
            if not car.active:
                continue

            min_light_dist = float('inf')
            for light in lights:
                if not is_blocked(car, light):
                    continue
                dist = light.x - car.x if car.path_type == 'horizontal' else light.y - car.y
                if 0 < dist < min_light_dist:
                    min_light_dist = dist

            if min_light_dist != float('inf'):
                if min_light_dist < 10 or car.speed < 1.0:
                    car.speed = 0.0
                    continue
                else:
                    target_speed = (min_light_dist - 10) / 10
                    car.speed += (target_speed - car.speed) * 0.4
            else:
                car.speed += (car.target_speed - car.speed) * 0.05

            same_lane = [c for c in cars if c.active and c != car and c.path == car.path]
            same_lane_sorted = sorted(same_lane, key=lambda c: c.x if car.path_type == 'horizontal' else c.y)

            min_dist = float('inf')
            for ahead in same_lane_sorted:
                dist = ahead.x - car.x if car.path_type == 'horizontal' else ahead.y - car.y
                if dist > 0:
                    min_dist = min(min_dist, dist)

            if min_dist < 80:
                if min_dist < 15:
                    car.speed = 0.0
                else:
                    target_speed = (min_dist - 15) / 10
                    car.speed += (target_speed - car.speed) * 0.3
            else:
                car.speed += (car.target_speed - car.speed) * 0.05

            car.speed = max(0.0, min(car.speed, 12.0))

            collision = any(
                abs(ahead.x - car.x) < 5 if car.path_type == 'horizontal'
                else abs(ahead.y - car.y) < 5
                for ahead in same_lane_sorted
            )

            if not collision:
                car.step()

        time.sleep(dt)

def get_active_cars():
    return [car for car in cars if car.active]

def start_simulation():
    threading.Thread(target=simulation_loop, daemon=True).start()

__all__ = ['lights', 'get_active_cars', 'start_simulation', 'get_traffic_state', 'detection_zones']
