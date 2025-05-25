import pygame
import random
import os
from settings import *
from unit import Unit
from ui import Button
from castle import Castle
from background import Background
from music_manager import MusicManager  # ✅ 新增音乐模块

class Game:
    def __init__(self, screen, max_rounds=10):
        self.screen = screen
        self.round_num = 1
        self.max_rounds = max_rounds
        self.action_points = ACTIONS_PER_TURN
        self.font = pygame.font.SysFont("Arial", 24)

        self.phase = "deploy"
        self.battle_in_progress = False
        self.game_over = False
        self.game_result = ""

        self.background = Background("background.png")
        self.music = MusicManager(volume=0.5)
        self.music.play("bgm_calm.wav")  # 初始播放 calm 音乐

        self.red_castle = Castle("red", 20, HEIGHT // 2 - CASTLE_HEIGHT // 2)
        self.blue_castle = Castle("blue", WIDTH - 20 - CASTLE_WIDTH, HEIGHT // 2 - CASTLE_HEIGHT // 2)

        self.units = []
        self.pending_red_units = []
        self.pending_blue_units = []
        self.messages = []

        self.buttons = [
            Button("Infantry", 50, HEIGHT - 100, 80, 40, lambda: self.place_unit("infantry")),
            Button("Archer", 150, HEIGHT - 100, 80, 40, lambda: self.place_unit("archer")),
            Button("Cavalry", 250, HEIGHT - 100, 80, 40, lambda: self.place_unit("cavalry")),
            Button("Start Battle", 400, HEIGHT - 100, 120, 40, self.start_battle_phase),
            Button("Defend", 550, HEIGHT - 100, 100, 40, lambda: self.place_unit("infantry", is_defending=True)),
        ]

    def add_message(self, text):
        if len(self.messages) > 6:
            self.messages.pop(0)
        self.messages.append(text)

    def place_unit(self, unit_type, is_defending=False):
        if self.game_over or self.phase != "deploy":
            return
        if len(self.pending_red_units) >= 2:
            self.add_message("\U0001F6D1 Red side can only deploy 2 units.")
            return
        if self.action_points > 0:
            x = 150 if not is_defending else 220
            y_offset = (-25 if len(self.pending_red_units) == 0 else 25)
            y = HEIGHT // 2 + y_offset
            unit = Unit(unit_type, "red", x, y, is_defending=is_defending)
            self.pending_red_units.append(unit)
            self.action_points -= 1
            self.add_message(f"RED {unit_type} at y={y} {'(defend)' if is_defending else ''}")

    def ai_place_unit(self):
        if len(self.pending_blue_units) >= 2:
            return
        for _ in range(2 - len(self.pending_blue_units)):
            unit_type = random.choice(["infantry", "archer", "cavalry"])
            x = WIDTH - 150
            y_offset = (-25 if len(self.pending_blue_units) == 0 else 25)
            y = HEIGHT // 2 + y_offset
            unit = Unit(unit_type, "blue", x, y)
            self.pending_blue_units.append(unit)
            self.add_message(f"BLUE {unit_type} at y={y}")

    def start_battle_phase(self):
        if self.phase != "deploy" or self.game_over:
            return
        self.ai_place_unit()
        self.phase = "battle"
        self.battle_in_progress = True
        self.music.play("bgm_battle.wav")  # 切换战斗音乐
        self.units.extend(self.pending_red_units)
        self.units.extend(self.pending_blue_units)
        self.pending_red_units.clear()
        self.pending_blue_units.clear()

    def update(self):
        if self.phase != "battle" or self.game_over or not self.battle_in_progress:
            return

        for unit in self.units:
            unit.move(1.2)

        self.handle_battles()
        still_units = self.handle_castle_attack()

        if not still_units:
            self.battle_in_progress = False
            self.phase = "deploy"
            self.round_num += 1
            self.action_points = ACTIONS_PER_TURN
            self.music.play("bgm_calm.wav")  # 切回 calm 音乐
            if self.round_num > self.max_rounds:
                self.game_over = True
                self.game_result = "Game Over: Reached Max Rounds"
            else:
                self.add_message(f"=== Round {self.round_num} Start ===")

    def handle_battles(self):
        to_remove = set()
        for i in range(len(self.units)):
            unit1 = self.units[i]
            for j in range(i + 1, len(self.units)):
                unit2 = self.units[j]
                if unit1.side != unit2.side:
                    if abs(unit1.y - unit2.y) < 10 and abs(unit1.x - unit2.x) < 25:
                        if unit1.is_countered_by(unit2):
                            to_remove.add(i)
                        elif unit2.is_countered_by(unit1):
                            to_remove.add(j)
                        else:
                            to_remove.add(i)
                            to_remove.add(j)
        self.units = [u for idx, u in enumerate(self.units) if idx not in to_remove]

    def handle_castle_attack(self):
        updated_units = []
        for unit in self.units:
            if unit.side == "red" and unit.x >= self.blue_castle.x:
                self.blue_castle.take_damage(10)
            elif unit.side == "blue" and unit.x <= self.red_castle.x + CASTLE_WIDTH:
                defending_exists = any(u.side == "red" and u.is_defending for u in self.units)
                damage = 5 if defending_exists else 10
                self.red_castle.take_damage(damage)
            else:
                updated_units.append(unit)
        self.units = updated_units

        if self.red_castle.hp <= 0:
            self.game_over = True
            self.game_result = "Defeat! You lost."
        elif self.blue_castle.hp <= 0:
            self.game_over = True
            self.game_result = "Victory! You won."

        return len(self.units) > 0

    def draw_interface(self):
        self.background.draw(self.screen)

        pygame.draw.line(self.screen, BLACK, (CASTLE_WIDTH + 30, HEIGHT // 2),
                         (WIDTH - CASTLE_WIDTH - 30, HEIGHT // 2), 5)

        phase_label = "Deploy Phase" if self.phase == "deploy" else "Battle Phase"
        info_text = f"Round: {self.round_num}/{self.max_rounds}    AP: {self.action_points}    Phase: {phase_label}"
        self.screen.blit(self.font.render(info_text, True, BLACK), (WIDTH // 2 - 200, 30))

        self.red_castle.draw(self.screen, self.font)
        self.blue_castle.draw(self.screen, self.font)

        for unit in self.units:
            unit.draw(self.screen)
        for unit in self.pending_red_units + self.pending_blue_units:
            unit.draw(self.screen)

        for button in self.buttons:
            if self.phase == "deploy" and not self.game_over:
                button.draw(self.screen)

        message_box_x = WIDTH // 2 - 200
        message_box_y = 70
        message_box_width = 420
        message_box_height = 180
        pygame.draw.rect(self.screen, GRAY, (message_box_x, message_box_y, message_box_width, message_box_height))
        pygame.draw.rect(self.screen, BLACK, (message_box_x, message_box_y, message_box_width, message_box_height), 2)

        for idx, msg in enumerate(self.messages):
            msg_surface = self.font.render(msg, True, BLACK)
            self.screen.blit(msg_surface, (message_box_x + 10, message_box_y + 10 + idx * 25))

        if self.game_over:
            result_text = self.font.render(
                self.game_result, True,
                (0, 128, 0) if self.game_result.startswith("Victory") else (200, 0, 0)
            )
            self.screen.blit(result_text, (WIDTH // 2 - 80, HEIGHT // 2 - 60))

        pygame.display.flip()

    def handle_event(self, event):
        if self.phase == "deploy" and not self.game_over:
            for button in self.buttons:
                button.handle_event(event)
