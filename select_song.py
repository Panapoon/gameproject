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
import config

class SelectSong:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # สร้างเพลง
        self.songLIST = config.songLIST
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 45)

        # โหลดรูปภาพพื้นหลัง
        self.background_images = []
        for i in range(len(self.songLIST)):  # เปลี่ยนเป็นจำนวนภาพที่มีอยู่
            image_path = f"picture/BACKGROUND/BG{i+1}.png"
            try:
                # ตรวจสอบการโหลดภาพ
                self.background_images.append(pygame.transform.scale(pygame.image.load(image_path), (self.WIDTH, self.HEIGHT)))
            except pygame.error as e:
                print(f"Error loading image {image_path}: {e}")

        self.current_song_index = 1
        self.is_playing = False

        # ปุ่มเลือกเพลง
        self.songM_button = config.Button(self.songLIST[self.current_song_index], 40, 960, 700, 300, 300, config.WHITE, 200)

        # การคลิก
        self.is_clicking_left = False
        self.is_clicking_right = False
        self.is_clicking_mid = False

    def play_song(self):
        # หยุดเพลงปัจจุบันถ้ามีการเล่นอยู่
        if self.is_playing:
            pygame.mixer.music.stop()

        config.play_song(f"SONG{self.current_song_index}")
        self.is_playing = True
        print(f"Playing {self.songLIST[self.current_song_index - 1]}")

    def show(self):
        self.play_song()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "title", None
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        print(f"Starting {self.songLIST[self.current_song_index-1]}")
                        return  'gameplay' , self.current_song_index
                    
                    # ตรวจสอบการเลื่อนเพลงด้วยปุ่ม F และ J
                    elif event.key == pygame.K_f and self.current_song_index > 1:
                        self.current_song_index -= 1
                        self.play_song()
                    elif event.key == pygame.K_j and self.current_song_index < len(self.songLIST) :
                        self.current_song_index += 1
                        self.play_song()

                #ควบคุมด้วย scroll wheel
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and self.current_song_index > 1:  # scroll up
                        self.current_song_index -= 1
                        self.play_song()
                    elif event.button == 5 and self.current_song_index < len(self.songLIST):  # scroll down
                        self.current_song_index += 1
                        self.play_song()                        

            # แสดงพื้นหลัง
            self.screen.blit(self.background_images[self.current_song_index-1], (0,0))            

            #สร้างปุ่มตรงกลาง
            self.songM_button.text = self.songLIST[self.current_song_index-1]
            self.songM_button.draw(self.screen, mouse_pos)

            high_score_text = config.get_high_score(self.songLIST[self.current_song_index-1])
            high_score_text = self.font.render(f"{high_score_text:05}", True, (255, 255, 255))
            self.screen.blit(high_score_text, (900, 900))

            #สร้างปุ่มซ้ายและขวา
            if self.current_song_index > 1:
                songL_button = config.Button(self.songLIST[self.current_song_index-2], 40, 550, 850, 300, 300, config.WHITE, 200)
                songL_button.draw(self.screen, mouse_pos)
                if songL_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_left:
                    self.current_song_index -= 1
                    self.is_clicking_left = True  # ตั้งค่าเป็น True เพื่อป้องกันการคลิกซ้ำ
                    self.play_song()
                elif not songL_button.is_clicked(mouse_pos, mouse_click):
                    self.is_clicking_left = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก

            if self.current_song_index < len(self.songLIST):
                songR_button = config.Button(self.songLIST[self.current_song_index], 40, 1370, 850, 300, 300, config.WHITE, 200)
                songR_button.draw(self.screen, mouse_pos)
                if songR_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_right:
                    self.current_song_index += 1
                    self.is_clicking_right = True  # ตั้งค่าเป็น True เพื่อป้องกันการคลิกซ้ำ
                    self.play_song()
                elif not songR_button.is_clicked(mouse_pos, mouse_click):
                    self.is_clicking_right = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก

            if self.songM_button.is_clicked(mouse_pos, mouse_click) and not self.is_clicking_mid:
                return  'gameplay' , self.current_song_index
                self.is_clicking_mid = True  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก
            elif not self.songM_button.is_clicked(mouse_pos, mouse_click):
                self.is_clicking_mid = False  # ตั้งค่าเป็น False เมื่อไม่ได้คลิก

                # แสดงข้อความ Press Spacebar to start
                spb_surface = self.font.render("Press Spacebar to start", True, config.WHITE)
                spb_rect = spb_surface.get_rect(center=(self.WIDTH // 2, 75))
                self.screen.blit(spb_surface, spb_rect)

                pygame.display.flip()