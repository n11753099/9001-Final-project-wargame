# music_manager.py

import pygame
import os

class MusicManager:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        self.current_music = None
        self.volume = volume

    def play(self, music_file):
        """播放新的背景音乐（避免重复切换）"""
        if self.current_music == music_file:
            return  # 正在播放，无需切换

        # 停止旧音乐，播放新音乐
        self.stop()
        full_path = os.path.join(os.path.dirname(__file__), music_file)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)  # 无限循环
        self.current_music = music_file

    def stop(self):
        """停止音乐播放"""
        pygame.mixer.music.stop()
        self.current_music = None

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def set_volume(self, value):
        self.volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self.volume)
