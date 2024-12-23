import pygame
import json
import os

# สี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# ฟอนต์
FONT1 = "Font/Ldfcomicsans-jj7l.ttf"
FONT2 = "Font/Ldfcomicsansbold-zgma.ttf"
FONT3 = "Font/Ldfcomicsanshairline-5PmL.ttf"
FONT4 = "Font/Ldfcomicsanslight-6dZo.ttf"

menuBG = pygame.image.load("picture/menuBG.png")
Button_default_path = "picture/default_button.png"

# ฟังก์ชั่นเปิดเพลง มึงหัดใช้ฟังก์ชั่นที่กุสร้างบ้าง ขอร้อง
def play_song(song_name):
    song_name = song_name
    song_path = f"songs/{song_name}.mp3"
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(-1)

def save_high_score(song_name, score):
    """บันทึกคะแนนสูงสุดของเพลงลงในไฟล์ .json"""
    file_path = "high_scores.json"
    
    # ตรวจสอบว่ามีไฟล์อยู่หรือไม่
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # ถ้าไม่มีเพลงในไฟล์นี้ ให้เพิ่มเพลงพร้อมค่าเริ่มต้น
    song_key = f"{song_name}"
    if song_key not in data or score > data[song_key]:
        data[song_key] = score
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

def get_high_score(song_name):
    """ดึงคะแนนสูงสุดจากไฟล์ .json ถ้ายังไม่มีให้คืนค่า 0"""
    file_path = "high_scores.json"
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get(f"{song_name}", 0)
    return 0

# ฟังก์ชันสำหรับบันทึกการตั้งค่าลงในไฟล์
def save_settings(settings):
    try:
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file, indent=4)
            print("Settings saved successfully!")
    except Exception as e:
        print(f"Error saving settings: {e}")

# ฟังก์ชันสำหรับโหลดการตั้งค่าจากไฟล์
def load_settings():
    try:
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            print("Settings loaded successfully!")
            return settings
    except FileNotFoundError:
        print("No settings file found, using default settings.")
        return {
            "volume": 1.0,
            "key_bindings": {
                "D": pygame.K_d,
                "F": pygame.K_f,
                "K": pygame.K_k,
                "L": pygame.K_l
            }
        }
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {
            "volume": 1.0,
            "key_bindings": {
                "D": pygame.K_d,
                "F": pygame.K_f,
                "K": pygame.K_k,
                "L": pygame.K_l
            }
        }

# รับชื่อเพลง
song = "songNAME.txt"
songLIST = []
with open(song, 'r', encoding='utf-8') as file:
    songLIST = [line.strip() for line in file]

class Button:
    def __init__(self, text, text_size, x, y, width, height, color, alpha=255, corner_radius=20):
        self.text = text
        self.text_size = text_size
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color
        self.alpha = alpha
        self.corner_radius = corner_radius
        self.font = pygame.font.Font(FONT1, text_size)  # ใช้ฟอนต์ที่กำหนด

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)

    def _adjust_color(self, color, amount):
        """ ปรับสีเมื่อเมาส์ชี้ """
        r, g, b = color
        return (max(0, r + amount), max(0, g + amount), max(0, b + amount))

    def wrap_text(self, text, font, max_width):
        """ แบ่งข้อความให้พอดีกับขนาดปุ่ม """
        words = text.split(" ")
        lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = f"{current_line} {word}"
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def draw_rounded_rect(self, surface, color_with_alpha, size, radius):
        """ วาดสี่เหลี่ยมมุมโค้งมนบน surface """
        rect = pygame.Rect(0, 0, size[0], size[1])
        pygame.draw.rect(surface, color_with_alpha, rect, border_radius=radius)

    def draw(self, screen, mouse_pos):
        """ วาดปุ่มบนหน้าจอ """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)

        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.rect.collidepoint(mouse_pos):
            use_color = self._adjust_color(self.color, -50)  # ทำให้สีเข้มขึ้นเมื่อเมาส์ชี้
        else:
            use_color = self.color

        self.draw_rounded_rect(button_surface, use_color + (self.alpha,), (self.rect.width, self.rect.height), self.corner_radius)
        screen.blit(button_surface, self.rect.topleft)

        # วาดข้อความบนปุ่ม
        wrapped_text = self.wrap_text(self.text, self.font, self.rect.width - 10)
        text_height = len(wrapped_text) * self.font.get_linesize()
        text_y = self.rect.top + (self.rect.height - text_height) // 2

        for line in wrapped_text:
            text_surface = self.font.render(line, True, (0, 0, 0))  # วาดข้อความสีดำ
            text_rect = text_surface.get_rect(center=(self.rect.centerx, text_y + self.font.get_linesize() // 2))
            screen.blit(text_surface, text_rect)
            text_y += self.font.get_linesize()

    def is_clicked(self, mouse_pos, mouse_click):
        """ ตรวจสอบว่าเกิดการคลิกบนปุ่ม """
        return self.rect.collidepoint(mouse_pos) and mouse_click[0] == 1