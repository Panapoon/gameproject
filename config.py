import pygame
import json

#ขนาดหน้าจอ
screen_size = {
    "800x600": (800, 600),
    "1024x768": (1024, 768),
    "1280x720": (1280, 720),
    "1920x1080": (1920, 1080)
}
current_size_index = 0

#สี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#ฟ้อนเล็บ
FONT1 = "Font/Ldfcomicsans-jj7l.ttf"
FONT2 = "Font/Ldfcomicsansbold-zgma.ttf"
FONT3 = "Font/Ldfcomicsanshairline-5PmL.ttf"
FONT4 = "Font/Ldfcomicsanslight-6dZo.ttf"

menuBG = pygame.image.load("picture/menuBG.png")

#บันทึกการตั้งค่า
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

#โหลดการตั้งค่า
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"screen_size": "800x600"} 
    
#รับชื่อเพลง
song = "songNAME.txt"
songLIST = []
with open(song, 'r') as file:
    songLIST = [line.strip() for line in file] 
    
#คลาสปุ่ม
class Button:
    def __init__(self, text, text_size, x, y, width, height, color, alpha):
        self.text = text
        self.text_size = text_size
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.alpha = alpha
        self.hover_color = self._adjust_color(color, -50)

    def _adjust_color(self, color, amount):
        r, g, b = color
        return (max(0, r + amount), max(0, g + amount), max(0, b + amount))

    def wrap_text(self, text, font, max_width):
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
    
    def draw(self, screen, mouse_pos):
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        button_surface.fill((*current_color[:3], self.alpha)) 
        screen.blit(button_surface, self.rect.topleft)

        font = pygame.font.Font(None, self.text_size)
        wrapped_text = self.wrap_text(self.text, font, self.rect.width - 10)

        text_y = self.rect.top + (self.rect.height - (len(wrapped_text) * font.get_linesize())) // 2

        for line in wrapped_text:
            text_surface = font.render(line, True, (0, 0, 0))  
            text_rect = text_surface.get_rect(center=(self.rect.centerx, text_y + font.get_linesize() // 2))
            screen.blit(text_surface, text_rect)
            text_y += font.get_linesize()
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]