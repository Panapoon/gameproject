import pygame
import json
import os

# ขนาดหน้าจอ
screen_size = {
    "800x600": (800, 600),
    "1024x768": (1024, 768),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080)
}
current_size_index = 0

# สี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ฟอนต์
FONT1 = "Font/Ldfcomicsans-jj7l.ttf"
FONT2 = "Font/Ldfcomicsansbold-zgma.ttf"
FONT3 = "Font/Ldfcomicsanshairline-5PmL.ttf"
FONT4 = "Font/Ldfcomicsanslight-6dZo.ttf"

menuBG = pygame.image.load("picture/menuBG.png")
Button_default_path = "picture/default_button.png"

# บันทึกการตั้งค่า
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

# โหลดการตั้งค่า
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"screen_size": "800x600"}

# รับชื่อเพลง
song = "songNAME.txt"
songLIST = []
with open(song, 'r', encoding='utf-8') as file:
    songLIST = [line.strip() for line in file]

class Button:
    def __init__(self, text, text_size, x, y, width, height, color, alpha, image_path=None, corner_radius=20):
        self.text = text
        self.text_size = text_size
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.alpha = alpha
        self.corner_radius = corner_radius  # ขนาดของมุมโค้งมน
        self.button_image = None

        # พยายามโหลดรูปภาพ Button1.png ถึง Button5.png
        if image_path:
            image_path = os.path.join("picture", image_path)
            if os.path.exists(image_path):
                try:
                    self.button_image = pygame.image.load(image_path).convert_alpha()
                    self.button_image = pygame.transform.scale(self.button_image, (self.rect.width, self.rect.height))
                except pygame.error as e:
                    print(f"Error loading image {image_path}: {e}")
            else:
                print(f"Image file not found: {image_path}")
        
        # หากไม่มีภาพ, ลองโหลด Button1.png ถึง Button5.png
        if not self.button_image:
            for i in range(1, 6):  # ลองหาภาพ Button1.png ถึง Button5.png
                button_image_path = os.path.join("picture", f"Button{i}.png")
                if os.path.exists(button_image_path):
                    try:
                        self.button_image = pygame.image.load(button_image_path).convert_alpha()
                        self.button_image = pygame.transform.scale(self.button_image, (self.rect.width, self.rect.height))
                        print(f"Loaded {button_image_path}")
                        break  # ออกจาก loop เมื่อเจอไฟล์ภาพ
                    except pygame.error as e:
                        print(f"Error loading image {button_image_path}: {e}")

        # หากยังไม่พบภาพ, ใช้ Button_default.png
        if not self.button_image:
            default_image_path = "picture/Button_default.png"
            if os.path.exists(default_image_path):
                self.button_image = pygame.image.load(default_image_path).convert_alpha()
                self.button_image = pygame.transform.scale(self.button_image, (self.rect.width, self.rect.height))
                print(f"Using default image: {default_image_path}")
            else:
                print(f"Error: Default image '{default_image_path}' not found.")

    def _adjust_color(self, color, amount):
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
    
    def _draw_rounded_rect(self, surface, size, radius):
        """ วาดสี่เหลี่ยมมุมโค้งมนบน surface """
        rect = pygame.Rect(0, 0, size[0], size[1])

        # วาดสี่เหลี่ยมมุมโค้งมนโดยใช้ border_radius
        pygame.draw.rect(surface, (0, 0, 0), rect, border_radius=radius)
    
    def draw(self, screen, mouse_pos):
        # วาดพื้นหลังปุ่ม
        if self.button_image:
            screen.blit(self.button_image, self.rect.topleft)
        else:
            # ถ้าไม่มีภาพ, วาดปุ่มโดยใช้มุมโค้งมน
            button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            current_color = self._adjust_color(self.color, -50) if self.rect.collidepoint(mouse_pos) else self.color
            button_surface.fill((*current_color[:3], self.alpha))  # ใช้สีสำหรับพื้นหลัง
            # วาดมุมโค้งมน
            self._draw_rounded_rect(button_surface, (self.rect.width, self.rect.height), self.corner_radius)
            screen.blit(button_surface, self.rect.topleft)

        # วาดข้อความบนปุ่ม
        font = pygame.font.Font(FONT1, self.text_size)
        wrapped_text = self.wrap_text(self.text, font, self.rect.width - 10)

        text_y = self.rect.top + (self.rect.height - (len(wrapped_text) * font.get_linesize())) // 2

        for line in wrapped_text:
            text_surface = font.render(line, True, (0, 0, 0))  # วาดข้อความสีดำ
            text_rect = text_surface.get_rect(center=(self.rect.centerx, text_y + font.get_linesize() // 2))
            screen.blit(text_surface, text_rect)
            text_y += font.get_linesize()

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]


