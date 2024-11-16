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
    def __init__(self, game, song_index, score, perfect, good, bad, miss, combo, acc):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        self.song_index = song_index
        self.score = score
        self.perfect = perfect
        self.good = good
        self.bad = bad
        self.miss = miss
        self.combo = combo
        self.acc = acc

        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)
        self.font_rank = pygame.font.Font("Font/RosmatikaRegular-BWA45.ttf", 540)

        self.songLIST = config.songLIST

        # ปุ่มต่าง ๆ เช่น Restart, Select Song, Main Menu
        self.restart_button = config.Button("RESTART", 40, x=380, y=1000, width=400, height=80, color=(0, 120, 255))
        self.select_song_button = config.Button("SELECT SONG", 40, x=960, y=1000, width=400, height=80, color=(0, 120, 255))
        self.main_menu_button = config.Button("MAIN MENU", 40, x=1540, y=1000, width=400, height=80, color=(0, 120, 255))

        self.music_played = False

    def play_summary_music(self):
        """ เล่นเพลงที่เลือกเมื่อเข้าสู่หน้าสรุป """
        if not self.music_played:  # ตรวจสอบว่าเพลงยังไม่ได้เริ่ม
            pygame.mixer.init()
            pygame.mixer.music.load(f'songs/SONG{self.song_index}.mp3')
            pygame.mixer.music.play(-1)
            self.music_played = True  # ตั้งค่าให้เพลงเริ่มแล้ว

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
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.restart_button.is_clicked(mouse_pos, mouse_click):
            pass
        elif self.select_song_button.is_clicked(mouse_pos, mouse_click):
            pass
        elif self.main_menu_button.is_clicked(mouse_pos, mouse_click):
            pass

    def show(self):
        h = 0
        alpha = 0
        while True:
            self.play_summary_music()
            for event in pygame.event.get():
                self.handle_events(event)

            self.screen.fill((0, 0, 0))

            # วาดภาพพื้นหลังตามเพลงที่เลือก
            background_image = pygame.image.load(f'picture/BACKGROUND/BG{self.song_index}.png')
            background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background_image, (0, 0))

            overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            
            while h <= 150:
                h += 5
                self.screen.fill((0, 0, 0)) 
                self.screen.blit(background_image, (0, 0))
                self.screen.blit(overlay, (0, 0))

                head_overlay = pygame.Surface((self.WIDTH, h))
                head_overlay.set_alpha(128)
                head_overlay.fill((0, 0, 0))
                self.screen.blit(head_overlay, (0, 0))

                tail_overlay = pygame.Surface((self.WIDTH, h))
                tail_overlay.set_alpha(128)
                tail_overlay.fill((0, 0, 0))
                self.screen.blit(tail_overlay, (0, 1080 - h))

                pygame.display.flip()

            song_name_text = self.font.render(config.songLIST[self.song_index-1], True, (255, 255, 255))
            self.screen.blit(song_name_text, (200, 40))

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

            # วาดปุ่ม
            mouse_pos = pygame.mouse.get_pos()
            self.restart_button.draw(self.screen, mouse_pos)
            self.select_song_button.draw(self.screen, mouse_pos)
            self.main_menu_button.draw(self.screen, mouse_pos)

            
            # เฟดข้อความที่แสดง
            stats_texts_faded = []

            rank = self.calculate_rank()
            shadow_rank_text = self.font_rank.render(rank, True, (255, 128, 0))  # สีเหลืองสำหรับ Rank

            rank_text = self.font_rank.render(rank, True, (255, 255, 0))  # สีเหลืองสำหรับ Rank

            while alpha <= 255:
                alpha += 1

                stats_texts_faded.clear()
                for text in stats_texts:
                    faded_text = self.font.render(text, True, (255, 255, 255))
                    faded_text.set_alpha(alpha)
                    stats_texts_faded.append(faded_text)

                # คำนวณแรงค์ (เช่น S, A, B, C, D) ตามเกณฑ์ที่กำหนด
                shadow_rank_text.set_alpha(alpha)
                shadow_rank_rect = shadow_rank_text.get_rect(center=(self.screen.get_width() - 292, self.screen.get_height() // 2+12))
                self.screen.blit(shadow_rank_text, shadow_rank_rect)

                rank_text.set_alpha(alpha)
                rank_rect = rank_text.get_rect(center=(self.screen.get_width() - 300, self.screen.get_height() // 2))
                self.screen.blit(rank_text, rank_rect)

                    # วาดข้อความที่เฟด
                for i, text in enumerate(stats_texts_faded):
                    self.screen.blit(text, (200, 225 + i * 90))
                
                pygame.display.flip()
                pygame.time.delay(5)

        
        """def show(self):
            h = 0
            alpha = 0
            start_ticks = pygame.time.get_ticks()  # เริ่มจับเวลา
            fade_duration = 2000  # ระยะเวลาในการทำ fade 2 วินาที
            overlay_duration = 3000  # ระยะเวลาในการขยาย overlay 3 วินาที

            while True:
                self.play_summary_music()
                for event in pygame.event.get():
                    self.handle_events(event)

                # วาดภาพพื้นหลัง
                background_image = pygame.image.load(f'picture/BACKGROUND/BG{self.song_index}.png')
                background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
                self.screen.blit(background_image, (0, 0))

                overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                elapsed_time = pygame.time.get_ticks() - start_ticks  # เวลาที่ผ่านไป

                # ขยาย overlay (head_overlay, tail_overlay)
                if elapsed_time <= overlay_duration:
                    h = int((elapsed_time / overlay_duration) * 150)  # ขยายตามเวลา
                head_overlay = pygame.Surface((self.WIDTH, h))
                head_overlay.set_alpha(128)
                head_overlay.fill((0, 0, 0))
                self.screen.blit(head_overlay, (0, 0))

                tail_overlay = pygame.Surface((self.WIDTH, h))
                tail_overlay.set_alpha(128)
                tail_overlay.fill((0, 0, 0))
                self.screen.blit(tail_overlay, (0, self.HEIGHT - h))

                if elapsed_time >= overlay_duration:
                    # เฟดข้อความหลังจาก overlay ขยายเสร็จ
                    if alpha < 128:
                        alpha = int((elapsed_time - overlay_duration) / fade_duration * 128)
                
                # แสดงข้อมูล
                stats_texts = [
                    f"Score: {self.score}",
                    f"Perfect: {self.perfect}",
                    f"Good: {self.good}",
                    f"Bad: {self.bad}",
                    f"Miss: {self.miss}",
                    f"Combo: {self.combo}",
                    f"Accuracy: {self.acc:.2f}%",
                ]

                stats_texts_faded = []
                for text in stats_texts:
                    faded_text = self.font.render(text, True, (255, 255, 255))
                    faded_text.set_alpha(alpha)
                    stats_texts_faded.append(faded_text)

                # คำนวณและแสดงอันดับ
                rank = self.calculate_rank()
                rank_text = self.font_rank.render(rank, True, (255, 255, 0))  # สีเหลือง
                rank_rect = rank_text.get_rect(center=(self.screen.get_width() - 300, self.screen.get_height() // 2))
                
                # ตรวจสอบให้แน่ใจว่า rank_rect ถูกกำหนดค่าแล้วก่อนที่จะใช้ set_alpha
                rank_text.set_alpha(alpha)
                self.screen.blit(rank_text, rank_rect)

                # วาดข้อความ
                for i, text in enumerate(stats_texts_faded):
                    self.screen.blit(text, (200, 225 + i * 90))

                # วาดปุ่ม
                mouse_pos = pygame.mouse.get_pos()
                self.restart_button.draw(self.screen, mouse_pos)
                self.select_song_button.draw(self.screen, mouse_pos)
                self.main_menu_button.draw(self.screen, mouse_pos)

                pygame.display.flip()
                """

