"""
import pygame
รับ score,count_PERFECT,count_GOOD,count_BAD,count_MISS จาก gameplay.py
แสดงrankแก่ผู้เล่น A,B,C,D
กด space bar เพื่อกลับไป select_song
เปิดเพลงที่เล่นด้วยก็ดี
วีทำ
"""
"""
import pygame
รับ score,count_PERFECT,count_GOOD,count_BAD,count_MISS จาก gameplay.py
แสดงrankแก่ผู้เล่น A,B,C,D
กด space bar เพื่อกลับไป select_song
เปิดเพลงที่เล่นด้วยก็ดี
วีทำ
"""
import pygame
import sys
import config
class Summary:
    def __init__(self, game, score, perfect, good, bad, miss, combo, acc):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        self.score = score
        self.perfect = perfect
        self.good = good
        self.bad = bad
        self.miss = miss
        self.combo = combo
        self.acc = acc

        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 45)

        self.songLIST = config.songLIST

        self.background_images = []
        for i in range(len(self.songLIST)):  # เปลี่ยนเป็นจำนวนภาพที่มีอยู่
            image_path = f"picture/BACKGROUND/BG{i+1}.png"
            try:
                self.background_images.append(pygame.transform.scale(pygame.image.load(image_path), (self.WIDTH, self.HEIGHT)))
            except pygame.error as e:
                print(f"Error loading image {image_path}: {e}")

        self.current_song_index = 1
        self.current_score = 0

    def show(self):
        self.screen.blit(self.background_images[self.current_song_index-1], (0,0))

        rect_surface = pygame.Surface((1920, 200), pygame.SRCALPHA)
        rect_surface.set_alpha(200)
        rect_surface.fill(config.BLACK) 
        self.screen.blit(rect_surface, (0,0))       
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "select_song"
                    
            for i in range(0, self.score, 5):
                spb_surface = self.font.render(i, True, config.WHITE)
                spb_rect = spb_surface.get_rect(center=(self.WIDTH // 2, 75))
                self.screen.blit(spb_surface, spb_rect)

                
            pygame.display.flip()