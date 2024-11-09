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
        self.volume_left_button = config.Button("-", 40, int(self.WIDTH * 0.2), int(self.HEIGHT * 0.3), 100, 80, config.RED, 255)
        self.volume_right_button = config.Button("+", 40, int(self.WIDTH * 0.8), int(self.HEIGHT * 0.3), 100, 80, config.GREEN, 255)

        # ปุ่มปรับความเร็วโน้ต
        self.speed_left_button = config.Button("-", 40, int(self.WIDTH * 0.2), int(self.HEIGHT * 0.5), 100, 80, config.RED, 255)
        self.speed_right_button = config.Button("+", 40, int(self.WIDTH * 0.8), int(self.HEIGHT * 0.5), 100, 80, config.GREEN, 255)

        # ปุ่มปรับ Key Blind
        self.key_blind_button = config.Button("Key Blind", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.7), 300, 80, config.GREEN, 255)

        # ปุ่ม Apply
        self.apply_button = config.Button("APPLY", 40, int(self.WIDTH * 0.75), int(self.HEIGHT * 0.8), 200, 80, config.GREEN, 255)

        # ปุ่ม Back
        self.back_button1 = config.Button("BACK", 40, int(self.WIDTH * 0.25), int(self.HEIGHT * 0.8), 200, 80, config.RED, 255)
        self.back_button2 = config.Button("BACK", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.9), 200, 80, config.RED, 255)

        # ค่าเริ่มต้น
        self.volume = 1.0
        self.note_speed = 1.0
        self.key_blind = False
        self.key_bindings = {  # เก็บ key bindings ของผู้ใช้
            "D": pygame.K_d,
            "F": pygame.K_f,
            "K": pygame.K_k,
            "L": pygame.K_l
        }
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
                        return "title"  # หรือกลับไปที่หน้าหลักถ้ากด ESC

            # วาดพื้นหลัง
            self.screen.blit(self.optionBG, (0, 0))

            # วาดปุ่ม
            self.volume_left_button.draw(self.screen, mouse_pos)
            self.volume_right_button.draw(self.screen, mouse_pos)
            self.speed_left_button.draw(self.screen, mouse_pos)
            self.speed_right_button.draw(self.screen, mouse_pos)
            self.key_blind_button.draw(self.screen, mouse_pos)
            self.apply_button.draw(self.screen, mouse_pos)
            self.back_button1.draw(self.screen, mouse_pos) 

            # ส่วนหัว
            OPTION_surface = self.font.render("OPTION", True, config.BLACK)
            OPTION_rect = OPTION_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT //7))
            shadow_surface = self.font.render("OPTION", True, (0, 0, 0))  # สีดำสำหรับเงา
            shadow_rect = shadow_surface.get_rect(center=(self.WIDTH // 2 + 5, self.HEIGHT // 7 + 5))  # เงาจะอยู่ด้านล่างขวาเล็กน้อย
            self.screen.blit(shadow_surface, shadow_rect)
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

            # ตรวจสอบการคลิกปุ่ม Apply
            if self.apply_button.is_clicked(mouse_pos, mouse_click):
                self.apply_settings()  # บันทึกการตั้งค่าทั้งหมด
                break

            # ตรวจสอบการคลิกปุ่ม Back
            if self.back_button1.is_clicked(mouse_pos, mouse_click):
                return "title"  # คืนค่าไปที่หน้าหลัก

            # ตรวจสอบการคลิกปุ่ม Key Blind
            if self.key_blind_button.is_clicked(mouse_pos, mouse_click):
                self.key_blind_screen()  # เปิดหน้าต่างปรับ Key Blind

            pygame.display.flip()

    def key_blind_screen(self):
        running = True
        key_to_change = None
        selected_key = None
        spacing = 150
        printed_message = {}  # ใช้เพื่อเก็บว่าข้อความนั้นพิมพ์ไปแล้วหรือไม่

        while running:
            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if key_to_change:
                        self.key_bindings[key_to_change] = event.key  # เปลี่ยนแปลงการตั้งค่าปุ่ม
                        print(f"Key for {key_to_change} changed to {pygame.key.name(event.key)}")
                        key_to_change = None  # Reset key_to_change after changing the key

                    if event.key == pygame.K_ESCAPE:  # Back action (Escape to go back)
                        running = False

            # Display instruction text
            line1_text = self.font.render("Press a key", True, (0, 0, 0))
            line2_text = self.font.render("to change the key binding", True, (0, 0, 0))

            line1_rect = line1_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 8))
            line2_rect = line2_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 8 + 100))

            self.screen.blit(line1_text, line1_rect)
            self.screen.blit(line2_text, line2_rect)
            self.back_button2.draw(self.screen, mouse_pos)

            # Display current key bindings
            y_offset = self.HEIGHT // 3
            for action, key in self.key_bindings.items():
                key_surface = self.font.render(f"{action}: {pygame.key.name(key)}", True, (0, 0, 0))
                key_rect = key_surface.get_rect(center=(self.WIDTH // 2, y_offset))

                # Draw red border around selected key
                if selected_key == action:
                    pygame.draw.rect(self.screen, (255, 0, 0), key_rect.inflate(20, 20), 3)

                self.screen.blit(key_surface, key_rect)

                # If mouse clicked on the key, set that key for modification
                if key_rect.collidepoint(mouse_pos) and mouse_click[0]:
                    if action != selected_key:  # ถ้าผู้ใช้เลือกปุ่มใหม่
                        selected_key = action
                        printed_message[selected_key] = False  # รีเซ็ตข้อความที่พิมพ์แล้ว
                        print(f"Click to change {action} key binding.")  # พิมพ์ข้อความเมื่อผู้ใช้เลือกปุ่มใหม่
                    key_to_change = action

                y_offset += spacing

            # Prevent printing the same message multiple times
            if selected_key and not printed_message.get(selected_key, False):
                printed_message[selected_key] = True  # ตั้งให้ข้อความนี้พิมพ์แล้ว

            if self.back_button2.is_clicked(mouse_pos, mouse_click):
                return  # กลับไปที่หน้า Options

            pygame.display.flip()

        return  # เมื่อกลับมาที่หน้า Options

    def apply_settings(self):
        # บันทึกการตั้งค่าทั้งหมด
        settings = {
            "screen_size": self.current_resolution,
            "volume": self.volume,
            "note_speed": self.note_speed,
            "key_bindings": self.key_bindings  # บันทึก key bindings
        }
        config.save_settings(settings)  # ฟังก์ชันสำหรับบันทึกการตั้งค่า
        pygame.mixer.music.set_volume(self.volume)
