import random
scale = 2.5

class TrafficLight:
    def __init__(self, tl_id, location, direction, green=5, red=5):
        self.id = tl_id
        self.x, self.y = location
        self.direction = direction
        self.green_duration = green
        self.red_duration = red
        self.timer = 0
        self.is_green = True

    def step(self, dt):
        self.timer += dt
        if self.is_green and self.timer >= self.green_duration:
            self.is_green = False
            self.timer = 0
        elif not self.is_green and self.timer >= self.red_duration:
            self.is_green = True
            self.timer = 0

class Car:
    def __init__(self, car_id, path, path_type):
        self.id = car_id
        self.path = path
        self.path_type = path_type
        self.pos_index = 0
        self.x, self.y = self.path[0]
        self.target_speed = random.uniform(12.0 * scale, 16.0 * scale)  # ↑ скорость
        self.speed = self.target_speed
        self.active = True
        self.blocked_by_light = False

    def step(self):
        if not self.active or self.pos_index >= len(self.path) - 1:
            self.active = False
            return

        next_index = min(self.pos_index + 1, len(self.path) - 1)
        next_x, next_y = self.path[next_index]

        dx = next_x - self.x
        dy = next_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            self.pos_index = next_index
            self.x, self.y = next_x, next_y
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

        if self.pos_index >= len(self.path) - 1:
            self.active = False
import random

# Масштаб (должен совпадать с simulation.py и geometry.py)
scale = 2.5

class TrafficLight:
    def __init__(self, tl_id, location, direction, green=5, red=5):
        self.id = tl_id
        self.x, self.y = location
        self.direction = direction
        self.green_duration = green
        self.red_duration = red
        self.timer = 0
        self.is_green = True

    def step(self, dt):
        self.timer += dt
        if self.is_green and self.timer >= self.green_duration:
            self.is_green = False
            self.timer = 0
        elif not self.is_green and self.timer >= self.red_duration:
            self.is_green = True
            self.timer = 0

class Car:
    def __init__(self, car_id, path, path_type):
        self.id = car_id
        self.path = path
        self.path_type = path_type
        self.pos_index = 0
        self.x, self.y = self.path[0]
        self.target_speed = random.uniform(12.0 * scale, 16.0 * scale)  # ↑ скорость
        self.speed = self.target_speed
        self.active = True
        self.blocked_by_light = False

    def step(self):
        if not self.active or self.pos_index >= len(self.path) - 1:
            self.active = False
            return

        next_index = min(self.pos_index + 1, len(self.path) - 1)
        next_x, next_y = self.path[next_index]

        dx = next_x - self.x
        dy = next_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < self.speed:
            self.pos_index = next_index
            self.x, self.y = next_x, next_y
        else:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

        if self.pos_index >= len(self.path) - 1:
            self.active = False
