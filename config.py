import pygame
import json
import os

# ขนาดหน้าจอ
screen_size = {
    "1024x768": (1024, 768),
    "1280x720": (1280, 720),
    "1366x768": (1366, 768),
    "1600x900": (1600, 900),
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
        return {"screen_size": "1280x720"}

# รับชื่อเพลง
song = "songNAME.txt"
songLIST = []
with open(song, 'r', encoding='utf-8') as file:
    songLIST = [line.strip() for line in file]

class Button:
    def __init__(self, text, text_size, x, y, width, height, color, alpha, image_path=None, corner_radius=20):
        self.text = text
        self.text_size = text_size
        self.base_screen_width, self.base_screen_height = 1920, 1080
        self.original_x, self.original_y = x, y
        self.original_width, self.original_height = width, height
        self.color = color
        self.alpha = alpha
        self.corner_radius = corner_radius
        self.button_image = None

        self.update_size_and_position()
        
        if image_path:
            self.load_image(image_path)
        else:
            self.button_image = None
            
    def update_size_and_position(self):
        """ ปรับขนาดและตำแหน่งของปุ่มตามขนาดหน้าจอ """
        current_screen_width, current_screen_height = pygame.display.get_surface().get_size()
        scale_x = current_screen_width / self.base_screen_width
        scale_y = current_screen_height / self.base_screen_height

        new_width = int(self.original_width * scale_x)
        new_height = int(self.original_height * scale_y)
        new_x = int(self.original_x * scale_x)
        new_y = int(self.original_y * scale_y)

        # สร้าง rect ใหม่โดยกำหนดให้จุดศูนย์กลางเป็น new_x, new_y
        self.rect = pygame.Rect(0, 0, new_width, new_height)
        self.rect.center = (new_x, new_y)

        # ปรับขนาดของภาพปุ่มตามสัดส่วนใหม่ (ถ้ามี)
        if self.button_image:
            self.button_image = pygame.transform.scale(self.button_image, (self.rect.width, self.rect.height))
    
    def load_image(self, image_path): 
        """ โหลดรูปภาพปุ่มจากไฟล์ """
        if image_path:
            self.button_image = self.try_load_image(image_path)
        if not self.button_image:
            for i in range(5):
                self.button_image = self.try_load_image(f"Button{i+1}.png")
                if self.button_image:
                    break
        if not self.button_image:
            self.button_image = self.try_load_image("Button_default.png")

    def try_load_image(self,image_name):
        """ ช่วยโหลดภาพและคืนค่าภาพหรือ None ถ้าโหลดไม่ได้ """
        image_path = os.path.join("picture", image_name)
        if os.path.exists(image_path):
            try:
                image = pygame.image.load(image_path).convert_alpha()
                return image
            except pygame.error:
                print(f"Error loading image (image_path)")
        return None

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
        # วาดสี่เหลี่ยมมุมโค้งมนโดยใช้ border_radius
        pygame.draw.rect(surface, self.color, rect, border_radius=radius)
    
    def draw(self, screen, mouse_pos):
        """ วาดปุ่มบนหน้าจอ """
        if self.button_image:
            if self.button_image.get_size() != (self.rect.width, self.rect.height):
                self.button_image = pygame.transform.scale(self.button_image, (self.rect.width, self.rect.height))
            if self.rect.collidepoint(mouse_pos):
                overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 50))
                image_surface = self.button_image.copy()
                image_surface.blit(overlay, (0,0))
            else:
                image_surface =self.button_image

            screen.blit(image_surface, self.rect.topleft)
        else:
            button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            if self.rect.collidepoint(mouse_pos):
                use_color = self._adjust_color(self.color, -50)
            else:
                use_color = self.color
            
            self.draw_rounded_rect(button_surface, use_color + (self.alpha,), (self.rect.width, self.rect.height), self.corner_radius)
            screen.blit(button_surface, self.rect.topleft)
        # วาดข้อความบนปุ่ม
        font = pygame.font.Font(FONT1, self.text_size)
        wrapped_text = self.wrap_text(self.text, font, self.rect.width - 10)

        text_height = len(wrapped_text) * font.get_linesize()
        text_y = self.rect.top + (self.rect.height - text_height) // 2

        for line in wrapped_text:
            text_surface = font.render(line, True, (0, 0, 0))  # วาดข้อความสีดำ
            text_rect = text_surface.get_rect(center=(self.rect.centerx, text_y + font.get_linesize() // 2))
            screen.blit(text_surface, text_rect)
            text_y += font.get_linesize()       
    def is_clicked(self, mouse_pos, mouse_click):
        """ ตรวจสอบว่าเกิดการคลิกบนปุ่ม """
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]


