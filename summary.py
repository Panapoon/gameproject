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
    def __init__(self, game, song_name, score, perfect, good, bad, miss, combo, acc):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        self.song_name = song_name
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

        # ปุ่มต่าง ๆ เช่น Restart, Select Song, Main Menu
        self.restart_button = config.Button("Restart", 20, x=400, y=600, width=120, height=40, color=(0, 120, 255))
        self.select_song_button = config.Button("Select Song", 20, x=600, y=600, width=120, height=40, color=(0, 120, 255))
        self.main_menu_button = config.Button("Main Menu", 20, x=800, y=600, width=120, height=40, color=(0, 120, 255))
    
    def calculate_rank(self):
        """ คำนวณแรงค์จากคะแนน """
        if self.acc >= 95:
            return "S"
        elif self.acc >= 90:
            return "A"
        elif self.acc >= 80:
            return "B"
        elif self.acc >= 70:
            return "C"
        else:
            return "D"

    def handle_events(self, event):
        """ จัดการเหตุการณ์คลิกปุ่ม """
        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        if self.restart_button.is_clicked(mouse_pos, mouse_click):
            # คำสั่งสำหรับการรีสตาร์ท
            pass
        elif self.select_song_button.is_clicked(mouse_pos, mouse_click):
            # คำสั่งสำหรับการเลือกเพลงใหม่
            pass
        elif self.main_menu_button.is_clicked(mouse_pos, mouse_click):
            # คำสั่งสำหรับกลับไปหน้าเมนูหลัก
            pass

    def show(self):
        self.screen.fill((0, 0, 0))

        # วาดภาพพื้นหลังตามเพลงที่เลือก
        current_index = self.songLIST.index(self.song_name)
        self.screen.blit(self.background_images[current_index], (0, 0))

        # แสดงชื่อเพลงที่มุมซ้ายบน
        song_name_text = self.font.render(self.song_name, True, (255, 255, 255))
        self.screen.blit(song_name_text, (20, 20))
        rect_surface = pygame.Surface((1920, 200), pygame.SRCALPHA)
        rect_surface.set_alpha(200)
        rect_surface.fill(config.BLACK)

        # แสดงสถิติที่ด้านซ้าย
        stats_texts = [
            f"Score: {self.score}",
            f"Perfect: {self.perfect}",
            f"Good: {self.good}",
            f"Bad: {self.bad}",
            f"Miss: {self.miss}",
            f"Combo: {self.combo}",
            f"Accuracy: {self.acc:.2f}%",
        ]
        y_offset = 100  # ตำแหน่ง Y เริ่มต้นของสถิติ
        for text in stats_texts:
            stat_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(stat_text, (20, y_offset))
            y_offset += 30  # เพิ่มระยะห่างระหว่างแต่ละสถิติ

        # คำนวณแรงค์ (เช่น S, A, B, C, D) ตามเกณฑ์ที่กำหนด
        rank = self.calculate_rank()
        rank_text = self.font.render(rank, True, (255, 255, 0))  # สีเหลืองสำหรับ Rank
        rank_rect = rank_text.get_rect(center=(self.screen.get_width() - 150, self.screen.get_height() // 2))
        self.screen.blit(rank_text, rank_rect)

        # วาดปุ่ม
        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.draw(self.screen, mouse_pos)
        self.select_song_button.draw(self.screen, mouse_pos)
        self.main_menu_button.draw(self.screen, mouse_pos)
        
        pygame.display.flip()