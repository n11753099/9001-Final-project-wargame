# ui.py

import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.action = action  # 点击按钮时执行的函数
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class InputBox:
    def __init__(self, x, y, w, h, font, default_text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = default_text
        self.font = font
        self.active = False
        self.color_active = GREEN
        self.color_inactive = BLACK
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 如果点击了输入框
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20 and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, screen):
        # 渲染文字
        txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # 画边框
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return self.text.strip() or "Unnamed"
