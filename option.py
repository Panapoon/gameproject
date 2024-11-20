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
from config import *  # สำหรับการใช้การตั้งค่าต่างๆ

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
        self.volume_left_button = config.Button("-", 40, int(self.WIDTH * 0.2), int(self.HEIGHT * 0.52), 100, 80, config.RED, 255)
        self.volume_right_button = config.Button("+", 40, int(self.WIDTH * 0.8), int(self.HEIGHT * 0.52), 100, 80, config.GREEN, 255)


        # ปุ่มปรับ Key Blind
        self.key_blind_button = config.Button("Key Blind", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.8), 300, 80, config.GREEN, 255)

        # ปุ่ม Apply
        self.apply_button = config.Button("APPLY", 40, int(self.WIDTH * 0.75), int(self.HEIGHT * 0.8), 200, 80, config.GREEN, 255)

        # ปุ่ม Back
        self.back_button1 = config.Button("BACK", 40, int(self.WIDTH * 0.25), int(self.HEIGHT * 0.8), 200, 80, config.RED, 255)
        self.back_button2 = config.Button("BACK", 40, int(self.WIDTH * 0.25), int(self.HEIGHT * 0.9), 200, 80, config.RED, 255)

        # ปุ่ม Reset
        self.reset_button = config.Button("RESET", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.9), 200, 80, config.YELLOW, 255)


        settings = config.load_settings()
        self.volume = settings.get("volume", 1.0)
        self.key_bindings = settings.get("key_bindings", {
            "LANE 1": pygame.K_d,
            "LANE 2": pygame.K_f,
            "LANE 3": pygame.K_k,
            "LANE 4": pygame.K_l
        })
        self.current_resolution = settings.get("screen_size", "1920x1080")  # ค่าเริ่มต้นเป็น 1920x1080

    def show(self):
        config.play_song("MENUSONG")
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
            self.key_blind_button.draw(self.screen, mouse_pos)
            self.apply_button.draw(self.screen, mouse_pos)
            self.back_button1.draw(self.screen, mouse_pos)
            self.reset_button.draw(self.screen, mouse_pos)  

            # ส่วนหัว
            OPTION_surface = self.font.render("OPTION", True, config.WHITE)
            OPTION_rect = OPTION_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 7))
            shadow_surface = self.font.render("OPTION", True, (0, 0, 0))  # สีดำสำหรับเงา
            shadow_rect = shadow_surface.get_rect(center=(self.WIDTH // 2 + 5, self.HEIGHT // 7 + 5))  # เงาจะอยู่ด้านล่างขวาเล็กน้อย
            self.screen.blit(shadow_surface, shadow_rect)
            self.screen.blit(OPTION_surface, OPTION_rect)

            # Volume
            volume_surface = self.font.render(f"Volume: {int(self.volume * 100)}%", True, config.WHITE)
            volume_rect = volume_surface.get_rect(center=(self.WIDTH // 2 , int(0.4 * self.HEIGHT)))
            shadow_volume_surface = self.font.render(f"Volume: {int(self.volume * 100)}%", True, (0, 0, 0))
            shadow_volume_rect = shadow_volume_surface.get_rect(center=(self.WIDTH // 2 + 5, int(0.4 * self.HEIGHT + 5)))
            self.screen.blit(shadow_volume_surface, shadow_volume_rect)
            self.screen.blit(volume_surface, volume_rect)


            # Handle volume button clicks
            if self.volume_left_button.is_clicked(mouse_pos, mouse_click):
                self.volume = max(0.0, self.volume - 0.001)
                pygame.mixer.music.set_volume(self.volume)
            if self.volume_right_button.is_clicked(mouse_pos, mouse_click):
                self.volume = min(1.0, self.volume + 0.001)
                pygame.mixer.music.set_volume(self.volume)
            
            # ขนาดของกราฟ slider
            slider_width = 1000
            slider_height = 40  # เพิ่มความสูงของกราฟ slider เพื่อให้มันใหญ่ขึ้น

            # สร้าง rect สำหรับกรอบ slider (เพิ่มความกว้างเป็น 600 และความสูงเป็น 20)
            slider_rect = pygame.Rect(self.WIDTH // 2 - slider_width // 2, self.HEIGHT // 2, slider_width, slider_height)
            pygame.draw.rect(self.screen, (225, 225, 225), slider_rect)  # สีเทาสำหรับกรอบ slider

            # ขนาดของ knob (ตัวเลื่อน)
            knob_size = 70 # ขนาดของ knob

            # คำนวณตำแหน่งของ knob ในกรอบ slider โดยให้มันอยู่ตรงกลางกรอบ
            # ใช้ self.volume เพื่อคำนวณตำแหน่งของ knob
            knob_x = self.WIDTH // 2 - slider_width // 2 + self.volume * slider_width  # คำนวณตำแหน่งของ knob ตาม volume
            knob_y = self.HEIGHT // 2 - knob_size // 2  # ทำให้ knob อยู่กลางในแนวตั้ง

            # สร้าง rect สำหรับ knob โดยคำนวณจากตำแหน่ง knob_x และ knob_y
            knob_rect = pygame.Rect(knob_x - knob_size // 2, knob_y+15, knob_size, knob_size)

            # วาดวงกลม (knob) ที่ตำแหน่งที่คำนวณไว้
            pygame.draw.circle(self.screen, config.BLACK, knob_rect.center, knob_size // 2)

            # ตรวจสอบการคลิกที่ slider และปรับระดับเสียง
            if mouse_click[0] and slider_rect.collidepoint(mouse_pos):
                # คำนวณตำแหน่งของ mouse ในกราฟและปรับ volume
                self.volume = (mouse_pos[0] - slider_rect.x+1) / slider_rect.width
                self.volume = max(0.0, min(self.volume, 1.0))  # ตรวจสอบให้ volume อยู่ในช่วง 0 ถึง 1
                pygame.mixer.music.set_volume(self.volume)

            # ตรวจสอบการคลิกปุ่ม Apply
            if self.apply_button.is_clicked(mouse_pos, mouse_click):
                self.apply_settings()  # บันทึกการตั้งค่าทั้งหมด

            # ตรวจสอบการคลิกปุ่ม Back
            if self.back_button1.is_clicked(mouse_pos, mouse_click):
                return "title"  # คืนค่าไปที่หน้าหลัก
            
            # ตรวจสอบการคลิกปุ่ม Key Blind
            if self.key_blind_button.is_clicked(mouse_pos, mouse_click):
                self.key_blind_screen()  # เปิดหน้าต่างปรับ Key Blind
            

            # ตรวจสอบการคลิกปุ่ม Reset
            if self.reset_button.is_clicked(mouse_pos, mouse_click):
                self.reset_settings()  # รีเซ็ตการตั้งค่า

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
                key_rect = key_surface.get_rect(center=(self.WIDTH // 2, y_offset+50))

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
            "volume": self.volume,
            "key_bindings": self.key_bindings  # บันทึก key bindings
        }

        # เรียกใช้ฟังก์ชันสำหรับบันทึกการตั้งค่า
        config.save_settings(settings)

        # ปรับระดับเสียงใน pygame
        pygame.mixer.music.set_volume(self.volume)

        # แสดงข้อความหรือฟีดแบคเมื่อการตั้งค่าถูกบันทึก
        print("Settings have been applied and saved.")

    def reset_settings(self):
        # รีเซ็ตการตั้งค่าเป็นค่าดีฟอลต์
        self.volume = 1.0
        self.key_bindings = {
            "LANE 1": pygame.K_d,
            "LANE 2": pygame.K_f,
            "LANE 3": pygame.K_k,
            "LANE 4": pygame.K_l
        }

        # อัพเดตการตั้งค่าในไฟล์
        self.apply_settings()
        print("Settings have been reset to default.")

    def fade(self):
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill(config.BLACK)

        for alpha in range(0, 256, 5):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)