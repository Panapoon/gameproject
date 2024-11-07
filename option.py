"""
import pygame
เปลี่ยน volumn
เปลี่ยน note speed
เปลี่ยน key blind
วีทำ
"""
import pygame
import sys
import config
from config import *

class Options:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # โหลดพื้นหลังและแปลงขนาด
        self.optionBG = pygame.image.load("picture/optionBG.png")
        self.optionBG = pygame.transform.scale(self.optionBG, (self.WIDTH, self.HEIGHT))

        # การตั้งค่าฟอนต์
        self.font = pygame.font.Font(config.FONT1, int(120))  # แปลงเป็น int เพื่อป้องกันข้อผิดพลาด

        # ปุ่มปรับเสียง
        self.volume_left_button = config.Button("-", 40, int(self.WIDTH * 0.2), int(self.HEIGHT * 0.3), 100, 80, config.GREEN, 255)
        self.volume_right_button = config.Button("+", 40, int(self.WIDTH * 0.8), int(self.HEIGHT * 0.3), 100, 80, config.GREEN, 255)

        # ปุ่มปรับความเร็วโน้ต
        self.speed_left_button = config.Button("-", 40, int(self.WIDTH * 0.2), int(self.HEIGHT * 0.5), 100, 80, config.GREEN, 255)
        self.speed_right_button = config.Button("+", 40, int(self.WIDTH * 0.8), int(self.HEIGHT * 0.5), 100, 80, config.GREEN, 255)

        # ปุ่มปรับ Key Blind
        self.key_blind_button = config.Button("Key Blind", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.7), 300, 80, config.GREEN, 255)

        # ปุ่ม Apply
        self.apply_button = config.Button("APPLY", 40, int(self.WIDTH * 0.85), int(self.HEIGHT * 0.8), 200, 80, config.GREEN, 255)

        # ค่าเริ่มต้น
        self.volume = 1.0
        self.note_speed = 1.0
        self.key_blind = False
        self.current_resolution = config.load_settings().get("screen_size", "1920x1080")  # ค่าเริ่มต้นเป็น 1920x1080

    def show(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "title"

            # วาดพื้นหลัง
            self.screen.blit(self.optionBG, (0, 0))

            # วาดปุ่ม
            self.volume_left_button.draw(self.screen, mouse_pos)
            self.volume_right_button.draw(self.screen, mouse_pos)
            self.speed_left_button.draw(self.screen, mouse_pos)
            self.speed_right_button.draw(self.screen, mouse_pos)
            self.key_blind_button.draw(self.screen, mouse_pos)
            self.apply_button.draw(self.screen, mouse_pos)

            # ส่วนหัว
            OPTION_surface = self.font.render("OPTION", True, config.BLACK)
            OPTION_rect = OPTION_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT //7))
            self.screen.blit(OPTION_surface, OPTION_rect)

            # Volume
            volume_surface = self.font.render(f"Volume: {int(self.volume * 100)}%", True, config.BLACK)
            volume_rect = volume_surface.get_rect(center=(self.WIDTH // 2 , int(0.3 * self.HEIGHT)))
            self.screen.blit(volume_surface, volume_rect)

            # Handle volume button clicks
            if self.volume_left_button.is_clicked(mouse_pos, mouse_click):
                self.volume = max(0.0, self.volume - 0.001)
                pygame.mixer.music.set_volume(self.volume)
            if self.volume_right_button.is_clicked(mouse_pos, mouse_click):
                self.volume = min(1.0, self.volume + 0.001)
                pygame.mixer.music.set_volume(self.volume)

            # Note speed
            note_speed_surface = self.font.render(f"Note Speed: {int(self.note_speed * 100)}%", True, config.BLACK)
            note_speed_rect = note_speed_surface.get_rect(center=(self.WIDTH // 2 , int(0.5 * self.HEIGHT)))
            self.screen.blit(note_speed_surface, note_speed_rect)

            # Handle note speed button clicks
            if self.speed_left_button.is_clicked(mouse_pos, mouse_click):
                self.note_speed = max(0.1, self.note_speed - 0.001)
            if self.speed_right_button.is_clicked(mouse_pos, mouse_click):
                self.note_speed = min(2.0, self.note_speed + 0.001)

            

            # Apply button
            if self.apply_button.is_clicked(mouse_pos, mouse_click):
                self.apply_settings()
                break

            pygame.display.flip()

    def apply_settings(self):
        # บันทึกการตั้งค่าทั้งหมด
        settings = {
            "screen_size": self.current_resolution,
            "volume": self.volume,
            "note_speed": self.note_speed,
            "key_blind": self.key_blind
        }
        config.save_settings(settings)
        pygame.mixer.music.set_volume(self.volume)
