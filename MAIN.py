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
from select_song import *
import config

class sec_Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Rhythm Game lnwza007')
        self.title_screen = TitleScreen(self)
        self.select_song = SelectSong(self)
        self.option = Options(self)

        # ปุ่มกลับ
        self.back_button = config.Button("Back", 27, 300, 500, 200, 50, (255, 165, 0), 0)
        
    def fade(self, fade_out=True, delay=500):
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill(config.BLACK)

        if fade_out:  # เฟดไปสีดำ
            for alpha in range(0, 256, 5):
                fade_surface.set_alpha(alpha)
                self.screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10)

            pygame.time.delay(delay)  # ค้างอยู่ในหน้าจอสีดำ
            
        else:  # เฟดกลับจากสีดำ
            for alpha in range(255, 0, -5):
                fade_surface.set_alpha(alpha)
                self.screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(10)

# เริ่มต้นเกม
game_instance = sec_Game()
screen = 'title'
next_screen = None 
while True:
    if screen == 'title':
        next_screen = game_instance.title_screen.show()
    elif screen == 'select_song':
        next_screen = game_instance.select_song.show()
    elif screen == 'gameplay':
        next_screen = game_instance.gameplay.show()
    elif screen == 'summary':
        next_screen = game_instance.summary.show()
    elif screen == 'option':
        next_screen = game_instance.option.show()
    else:
        pygame.quit()
        sys.exit()

    if next_screen and next_screen != screen:
        game_instance.fade(fade_out=True)  # เฟดไปสีดำ
        screen = next_screen  # เปลี่ยนหน้าจอ
        next_screen = None  # รีเซ็ตตัวแปรหน้าจอถัดไป
        game_instance.fade(fade_out=False)  # เฟดกลับจากสีดำ
