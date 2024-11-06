"""
import pygame
ใส่พื้นหลังสวยๆ
แสดงชื่อเกม
ปุ่ม play-ไปยัง select_song.py
ปุ่ม option-ไปยัง option.py
ปุ่ม quit-ออกจากเกม
ที่มี title_screen.py เนื่องจากกูต้องการให้มันสามารถกด esc จากหน้า select_song กลับมายังหน้า title ได้
ปู๊นทำ
"""
import pygame
import sys
import config

class TitleScreen:
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
        self.menuBG = pygame.image.load("picture/menuBG.png")
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)

        # สร้างปุ่มโดยใช้คลาส Button
        self.play_button = config.Button("Play", 72, 960, 460, 600, 120, self.GREEN, 255)
        self.options_button = config.Button("Options", 72, 960, 640, 600, 120, self.BLUE, 255)
        self.exit_button = config.Button("Exit", 72, 960, 820, 600, 120, self.RED, 255)

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menuBG, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # วาดปุ่ม
            self.play_button.draw(self.screen, mouse_pos)
            self.options_button.draw(self.screen, mouse_pos)
            self.exit_button.draw(self.screen, mouse_pos)

            title_surface = self.font.render("Rhythm Game", True, self.WHITE)
            title_rect = title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT))
            self.screen.blit(title_surface, title_rect)

            mouse_click = pygame.mouse.get_pressed()

            # ตรวจสอบการคลิกปุ่ม
            if self.play_button.is_clicked(mouse_pos, mouse_click):
                return 'select_song'
            if self.options_button.is_clicked(mouse_pos, mouse_click):
                return 'option'
            if self.exit_button.is_clicked(mouse_pos, mouse_click):
                pygame.quit()
                sys.exit()

            pygame.display.flip()