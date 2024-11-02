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
    
class Button:
    def __init__(self, text, x, y, width, height, color, alpha):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.alpha = alpha
        self.hover_color = self._adjust_color(color, -50)

    def _adjust_color(self, color, amount):
        r, g, b = color
        return (max(0, r + amount), max(0, g + amount), max(0, b + amount))

    def draw(self, screen, mouse_pos):
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        button_surface.fill((*current_color[:3], 200)) 
        screen.blit(button_surface, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))  
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]