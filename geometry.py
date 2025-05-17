# geometry.py
from typing import List, Tuple

# Центр перекрёстка
center_x = 950
center_y = 430
lane_gap = 30

def build_paths() -> List[List[Tuple[int, int]]]:
    return [
        # Горизонтальные (слева направо, верх и низ)
        [(x, center_y - lane_gap) for x in range(center_x - 700, center_x + 700, 5)],
        [(x, center_y + lane_gap) for x in range(center_x - 700, center_x + 700, 5)],
        # Вертикальные (сверху вниз, левая и правая)
        [(center_x - lane_gap, y) for y in range(center_y - 400, center_y + 400, 5)],
        [(center_x + lane_gap, y) for y in range(center_y - 400, center_y + 400, 5)],
    ]
