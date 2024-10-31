"""
import pygame
import title_screen.py
import select_song.py
import gameplay.py
import summary.py
import option.py
ดู flowchart ใน picture/main.png 
ปู๊นทำ
"""
import pygame
import sys
from title_screen import *

class sec_Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Rhythm Game lnwza007')
        self.title_screen = TitleScreen(self)

        # ปุ่มกลับ
        self.back_button = Button("Back", 300, 500, 200, 50, (255, 165, 0))

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # ล้างหน้าจอ
            text_surface = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60).render("Press ENTER to start!!!", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

            # วาดปุ่มกลับ
            self.back_button.draw(self.screen, pygame.mouse.get_pos())

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return  # กลับไปยังเมนูหลัก

            pygame.display.flip()

    def option_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 0, 0))  # เปลี่ยนพื้นหลังเป็นสีแดง
            option_surface = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 74).render("Option Running", True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(option_surface, option_rect)

            # วาดปุ่มกลับ
            self.back_button.draw(self.screen, pygame.mouse.get_pos())

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return  # กลับไปยังเมนูหลัก

            pygame.display.flip()

# เริ่มต้นเกม
game_instance = sec_Game()
game_instance.title_screen.show()

'hsdf;hafhldsfhsa'