# castle.py

import pygame
import os
from settings import *

class Castle:
    red_image = None
    blue_image = None

    def __init__(self, side, x, y, hp=INITIAL_HEALTH, name=None):
        self.side = side  # "red" or "blue"
        self.x = x
        self.y = y
        self.hp = hp
        self.name = name or (side.upper() + " Castle")  # 默认名称
        self.width = CASTLE_WIDTH
        self.height = CASTLE_HEIGHT

        # 加载图像资源
        if side == "red" and Castle.red_image is None:
            path = os.path.join(os.path.dirname(__file__), "red_castle.png")
            Castle.red_image = pygame.transform.scale(
                pygame.image.load(path).convert_alpha(),
                (self.width, self.height)
            )
        elif side == "blue" and Castle.blue_image is None:
            path = os.path.join(os.path.dirname(__file__), "blue_castle.png")
            Castle.blue_image = pygame.transform.scale(
                pygame.image.load(path).convert_alpha(),
                (self.width, self.height)
            )

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def draw(self, screen, font):
        # 选择图像
        image = Castle.red_image if self.side == "red" else Castle.blue_image
        screen.blit(image, (self.x, self.y))

        # 显示名称
        name_text = font.render(self.name, True, BLACK)
        screen.blit(name_text, (self.x + 5, self.y - 50))

        # 显示血量
        hp_text = font.render(f"HP: {self.hp}", True, BLACK)
        screen.blit(hp_text, (self.x + 10, self.y - 25))
