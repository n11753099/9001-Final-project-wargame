# main.py

import pygame
from ui import Button, InputBox
from game import Game
from unit import Unit

# 初始化 pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Castle Battle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# 启动界面输入框
input_rounds = InputBox(480, 200, 100, 35, font, "10")
input_red_name = InputBox(480, 260, 200, 35, font, "Red Castle")
input_blue_name = InputBox(480, 320, 200, 35, font, "Blue Castle")
start_button = Button("Start Game", 450, 380, 140, 45)

# 控制变量
game_started = False
game = None

# 主循环
running = True
while running:
    screen.fill((255, 255, 255))

    if not game_started:
        # 设置界面
        screen.blit(font.render("Enter Max Rounds:", True, (0, 0, 0)), (300, 200))
        screen.blit(font.render("Red Castle Name:", True, (0, 0, 0)), (300, 260))
        screen.blit(font.render("Blue Castle Name:", True, (0, 0, 0)), (300, 320))

        input_rounds.draw(screen)
        input_red_name.draw(screen)
        input_blue_name.draw(screen)
        start_button.draw(screen)
        pygame.display.flip()
    else:
        game.draw_interface()
        game.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            input_rounds.handle_event(event)
            input_red_name.handle_event(event)
            input_blue_name.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                try:
                    max_rounds = int(input_rounds.get_value())
                    red_name = input_red_name.get_value()
                    blue_name = input_blue_name.get_value()
                    game = Game(screen, max_rounds)
                    game.red_castle.name = red_name
                    game.blue_castle.name = blue_name
                    game_started = True
                except:
                    pass  # 输入非法时保持静默（可加提示）
        else:
            game.handle_event(event)

    clock.tick(60)

pygame.quit()
