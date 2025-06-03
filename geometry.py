# geometry.py
from typing import List, Tuple

# === Масштаб ===
scale = 2.5

# Центр перекрёстка
center_x = int(950 * scale)
center_y = int(430 * scale)
lane_gap = int(30 * scale)

def build_paths() -> List[List[Tuple[int, int]]]:
    return [
        # Горизонтальные (слева направо, верх и низ)
        [(int(x * scale), center_y - lane_gap) for x in range(950 - 700, 950 + 700, 5)],
        [(int(x * scale), center_y + lane_gap) for x in range(950 - 700, 950 + 700, 5)],
        # Вертикальные (сверху вниз, левая и правая)
        [(center_x - lane_gap, int(y * scale)) for y in range(430 - 400, 430 + 400, 5)],
        [(center_x + lane_gap, int(y * scale)) for y in range(430 - 400, 430 + 400, 5)],
    ]
