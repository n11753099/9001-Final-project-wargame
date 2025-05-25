import pygame
import os
from settings import *

# 克制关系
COUNTER_RULE = {
    "infantry": "cavalry",
    "cavalry": "archer",
    "archer": "infantry"
}

class Unit:
    archer_frames = []
    infantry_frames = []
    cavalry_image = None  # 单张图

    archer_loaded = False
    infantry_loaded = False
    cavalry_loaded = False

    @classmethod
    def load_frames(cls, unit_type, frame_width=60, frame_height=60):
        path = os.path.join(os.path.dirname(__file__), f"{unit_type}.png")
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        num_frames = sheet.get_width() // frame_width
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def __init__(self, unit_type, side, x, y, is_defending=False):
        self.unit_type = unit_type
        self.side = side  # "red" or "blue"
        self.x = x
        self.y = y
        self.is_defending = is_defending
        self.alive = True
        self.frame_index = 0
        self.frame_timer = 0         # ⏱ 帧延迟计数器
        self.frame_delay = 10        # ⌛ 切换帧的延迟值（数值越大，动画越慢）

        if unit_type == "infantry" and not Unit.infantry_loaded:
            Unit.infantry_frames = Unit.load_frames("infantry", 60, 60)
            Unit.infantry_loaded = True
        elif unit_type == "archer" and not Unit.archer_loaded:
            Unit.archer_frames = Unit.load_frames("archer", 60, 60)
            Unit.archer_loaded = True
        elif unit_type == "cavalry" and not Unit.cavalry_loaded:
            path = os.path.join(os.path.dirname(__file__), "cavalry.png")
            image = pygame.image.load(path).convert_alpha()
            Unit.cavalry_image = pygame.transform.scale(image, (60, 60))  # 统一大小
            Unit.cavalry_loaded = True

    def move(self, step):
        if not self.is_defending:
            if self.side == "red":
                self.x += step
            else:
                self.x -= step

        if self.unit_type in ["infantry", "archer"]:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                frames = Unit.infantry_frames if self.unit_type == "infantry" else Unit.archer_frames
                self.frame_index = (self.frame_index + 1) % len(frames)
                self.frame_timer = 0

    def is_countered_by(self, enemy_unit):
        return COUNTER_RULE[enemy_unit.unit_type] == self.unit_type

    def draw(self, screen):
        if self.unit_type == "infantry":
            frame = Unit.infantry_frames[self.frame_index % len(Unit.infantry_frames)]
        elif self.unit_type == "archer":
            frame = Unit.archer_frames[self.frame_index % len(Unit.archer_frames)]
        elif self.unit_type == "cavalry":
            frame = Unit.cavalry_image
        else:
            return

        if frame is None:
            return

        if self.side == "blue":
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, (self.x - frame.get_width() // 2, self.y - frame.get_height() // 2))

        if self.is_defending:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 30, 2)
