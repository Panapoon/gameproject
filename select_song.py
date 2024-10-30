"""
import pygame
รูปแบบขอตามที่ส่งให้นะ 
แสดง score ที่เคยทำได้จากเพลงนั้นๆ
ใช้ F J หรือ scroll mouse เพื่อเลื่อนเพลงและใช้ left click หรือ space bar เพื่อเริ่มเพลง
ใช้ ESC เพื่อกลับไปยังหน้า title
วีทำ
"""
import pygame
import sys
from option import *
from title_screen import *

class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = self._adjust_color(color, -50)

    def _adjust_color(self, color, amount):
        pass

    def draw(self, screen, mouse_pos):
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]
    
class SelectSong:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # กำหนดสี
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # โหลดรูปภาพพื้นหลัง
        self.background_images = []
        for i in range(1, 4):  # เปลี่ยนเป็นจำนวนภาพที่มีอยู่
            image_path = f"picture/menuBG{i}.png"
            self.background_images.append(pygame.image.load(image_path))
        self.current_bg_index = 0

        # สร้างปุ่ม
        songLIST = [1,2,3,4,5]
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)
        if self.current_bg_index == 0:
            self.songM_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
            self.songR_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
        elif self.current_bg_index == (len(songLIST) - 1):
            self.songL_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
            self.songM_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
        else:
            self.songL_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
            self.songM_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
            self.songR_button = Button(songLIST[self.current_bg_index], 300, 200, 200, 50, self.GREEN)
    
    def show(self):
        with True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    title_screen = TitleScreen(self.game)  # สมมุติว่า TitleScreen คือชื่อคลาส
                    title_screen.show() 
                    return

            self.screen.blit(self.background_images, (0,0))
            mouse_pos = pygame.mouse.get_pos()
            self.songL_button.draw(self.screen, mouse_pos)
            self.songM_button.draw(self.screen, mouse_pos)
            self.songR_button.draw(self.screen, mouse_pos)

            spb_surface = self.font.render("Rhythm Game", self.WHITE)
            spb_rect = spb_surface.get_rect(center=(self.WIDTH // 2, 100))
            self.screen.blit(spb_surface, spb_rect)

            mouse_click = pygame.mouse.get_pressed()

            if self.songM_button.is_clicked(mouse_pos, mouse_click) or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.gameplay(self.songLIST[self.current_bg_index])
            if self.songL_button.is_clicked(mouse_pos, mouse_click) or (event.type == pygame.KEYDOWN and event.key == pygame.K_f) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4):  # Scroll up
                self.current_bg_index = (self.current_bg_index - 1) % len(self.songLIST)
            if self.songR_button.is_clicked(mouse_pos, mouse_click) or (event.type == pygame.KEYDOWN and event.key == pygame.K_j) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5):  # Scroll down
                self.current_bg_index = (self.current_bg_index + 1) % len(self.songLIST)

            pygame.display.flip()
