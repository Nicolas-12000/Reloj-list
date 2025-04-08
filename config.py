SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GOLD": (255, 215, 0),
    "FLAME_ACTIVE": (90, 180, 255),  # Light blue
    "FLAME_INACTIVE": (40, 75, 102),  # Dark blue
    "TRANSPARENT": (0, 0, 0, 0)
}

FONTS = {
    "main": "Times New Roman",
    "roman": "Times New Roman",
    "gothic": "Arial"  # Fallback if gothic font not available
}

CLOCK_PARAMS = {
    "clock_center": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    "outer_radius": 300,
    "zodiac_radius": 200,
    "flames_radius": 270,
    "hour_hand_length": 150,
    "minute_hand_length": 220,
    "second_hand_length": 240
}