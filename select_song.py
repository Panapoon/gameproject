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
    
class SelectSong:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # กำหนดสี
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        #สร้างเพลง
        self.songLIST = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5"]
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 45)

        # โหลดรูปภาพพื้นหลัง
        self.background_images = []
        for i in range(len(self.songLIST)):  # เปลี่ยนเป็นจำนวนภาพที่มีอยู่
            image_path = f"picture/BG{i}.png"
            try:
                self.background_images.append(pygame.transform.scale(pygame.image.load(image_path), (self.WIDTH, self.HEIGHT)))
            except pygame.error as e:
                print(f"Error loading image {image_path}: {e}")
        
        self.current_bg_index = 1

        self.songM_button = Button(self.songLIST[self.current_bg_index], 325, 300, 150, 150, self.WHITE, 175)

        self.is_clicking_left = False
        self.is_clicking_right = False
        self.is_clicking_mid = False

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
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        print(f"Starting {self.songLIST[self.current_bg_index-1]}")
                        pass

                    # ตรวจสอบการเลื่อนเพลงด้วยปุ่ม F และ J
                    elif event.key == pygame.K_f and self.current_bg_index > 1:
                        self.current_bg_index -= 1
                        print(f"Current song index: {self.current_bg_index}")
                    elif event.key == pygame.K_j and self.current_bg_index < len(self.songLIST) :
                        self.current_bg_index += 1
                        print(f"Current song index: {self.current_bg_index}")
                
                #ควบคุมด้วย scroll wheel
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.current_bg_index > 1:  # scroll up
                        self.current_bg_index -= 1
                        print(f"Current song index: {self.current_bg_index}")
                    elif event.button == 5 and self.current_bg_index < len(self.songLIST):  # scroll down
                        self.current_bg_index += 1
                        print(f"Current song index: {self.current_bg_index}")

            #แสดงพื้นหลัง
            self.screen.blit(self.background_images[self.current_bg_index-1], (0,0))

            #สร้างปุ่มตรงกลาง
            self.songM_button.text = self.songLIST[self.current_bg_index-1]
            self.songM_button.draw(self.screen, mouse_pos)

            #สร้างปุ่มซ้ายและขวา
            if self.current_bg_index > 1:
                songL_button = Button(self.songLIST[self.current_bg_index-2], 125, 400, 150, 150, self.WHITE, 175)
                songL_button.draw(self.screen, mouse_pos)
                if songL_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_left:
                    self.current_bg_index -= 1
                    self.is_clicking_left = True  # ตั้งค่าเป็น True เพื่อป้องกันการคลิกซ้ำ
                    print(f"Current song index: {self.current_bg_index}")
                elif not songL_button.is_clicked(mouse_pos, mouse_click):
                    self.is_clicking_left = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก

            if self.current_bg_index < len(self.songLIST):
                songR_button = Button(self.songLIST[self.current_bg_index],525, 400, 150, 150, self.WHITE, 175)
                songR_button.draw(self.screen, mouse_pos)
                if songR_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_right:
                    self.current_bg_index += 1
                    self.is_clicking_right = True  # ตั้งค่าเป็น True เพื่อป้องกันการคลิกซ้ำ
                    print(f"Current song index: {self.current_bg_index}")
                elif not songR_button.is_clicked(mouse_pos, mouse_click):
                    self.is_clicking_right = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก

            if self.songM_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_mid:
                pass
                self.is_clicking_mid = True  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก
                print(f"Starting {self.songLIST[self.current_bg_index-1]}")
            elif not self.songM_button.is_clicked(mouse_pos, mouse_click):
                self.is_clicking_mid = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก


            #แสดงข้อความ Press Enter to start
            spb_surface = self.font.render("Press Spacebar to start", True, self.WHITE)
            spb_rect = spb_surface.get_rect(center=(self.WIDTH // 2, 75))
            self.screen.blit(spb_surface, spb_rect)

            pygame.display.flip()