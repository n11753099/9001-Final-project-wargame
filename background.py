# background.py

import pygame
import os
from settings import *

class Background:
    def __init__(self, image_path="background.png"):
        full_path = os.path.join(os.path.dirname(__file__), image_path)
        self.image = pygame.image.load(full_path).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
