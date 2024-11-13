import pygame
import time
from pygame import mixer
import config
from select_song import *
from option import *
from note import *

class Gameplay:
    def __init__(self, game, song_index):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen
        self.song_index = song_index
        self.song = config.songLIST[self.song_index]
        self.lane_width = self.WIDTH / 4
        self.hit_line_y = self.HEIGHT - 50 # จุดที่จะตีโน้ต
        self.note_height_offset = 0

        self.settings = config.load_settings()
        self.note_speed = self.settings.get("note_speed")  # ความเร็วของโน้ตที่ลงมา

        self.messege_display_time = 0
        self.messege_duration = 1.5

        self.clock = pygame.time.Clock()

        self.Note = Note(self, self.lane, self.spawn_time, duration=None)

        self.notes = []  
        self.score = 0 
        self.combo = 0  
        self.hit_notes = 0 
        self.missed_notes = 0  
        self.total_notes = 0  
        self.accuracy = 100.0  
        self.message = ""  
        self.message_display_time = 0 
        self.message_duration = 1.5  
        self.running = True  # 
        self.start_time = time.time() 
        self.paused = False  
        self.perfect_hits = 0  
        self.good_hits = 0  
        self.bad_hits = 0  

        config.play_song(self.song_name)
    
    def load_notes(self, file_name):
        """โหลดโน้ตจากไฟล์"""
        global total_notes
        with open(file_name, "r") as f:
            for line in f:
                parts = line.strip().split(",")  # แยกข้อมูลที่ใช้คั่นด้วยเครื่องหมายจุลภาค
                if len(parts) != 2:
                    print(f"Skipping invalid line: {line.strip()}")  # ข้ามบรรทัดที่ไม่ถูกต้อง
                    continue
                lane = int(parts[0])  # เลนที่โน้ตจะไป
                spawn_time = float(parts[1])  # เวลาที่โน้ตจะปรากฏ
                self.notes.append(Note(lane, self.spawn_time))  # เพิ่มโน้ตใหม่ในรายการ
                self.total_notes += 1

    def handle_input(self, keys, current_time):
        """จัดการกับการกดปุ่มและตรวจสอบการตีโน้ต"""
        hit_tolerances = [10, 20, 30]  # ความเบี่ยงเบนสำหรับการตี Perfect, Good, Bad
        hit_messages = ["Perfect!", "Good!", "Bad!"]  # ข้อความที่แสดงเมื่อตีโน้ต
        points = [500, 300, 100]  # คะแนนสำหรับแต่ละประเภทของการตีโน้ต

        if self.paused:  # ถ้าเกมหยุดชั่วคราว
            return

        for note in self.notes[:]:  # ลูปผ่านโน้ตทั้งหมด
            for i, tolerance in enumerate(hit_tolerances):  # ตรวจสอบแต่ละระดับของการตีโน้ต
                if note.is_hit(keys, tolerance):  # เช็คว่าโน้ตถูกตีหรือไม่
                    self.register_hit(note, points[i], hit_messages[i])
                    break

    def register_hit(self, note, points, hit_message):
        """ลงทะเบียนการตีโน้ต"""
        self.score += points  # เพิ่มคะแนนตามประเภทของการตี
        self.combo += 1  # เพิ่มคอมโบ
        self.hit_notes += 1  # เพิ่มจำนวนโน้ตที่ถูกตี
        if hit_message == "Perfect!":
            self.perfect_hits += 1
        elif hit_message == "Good!":
            self.good_hits += 1
        elif hit_message == "Bad!":
            self.bad_hits += 1
        self.notes.remove(note)  # ลบโน้ตที่ตีแล้วออกจากรายการ
        self.message = hit_message  # เก็บข้อความที่จะแสดง
        self.message_display_time = time.time()  # ตั้งเวลาแสดงข้อความ

    def register_miss(self, note):
        """ลงทะเบียนการพลาดโน้ต"""
        self.missed_notes += 1  # เพิ่มจำนวนโน้ตที่พลาด
        self.notes.remove(note)  # ลบโน้ตที่พลาดออกจากรายการ
        self.message = "Missed!"  # แสดงข้อความ "Missed!"
        self.message_display_time = time.time()  # ตั้งเวลาแสดงข้อความ

    def display_accuracy(self):
        total_notes = self.total_notes  # จำนวนโน้ตทั้งหมด
        if total_notes > 0:
            if (self.perfect_hits + self.good_hits + self.bad_hits + self.missed_notes) > 0:
                self.accuracy = ((self.perfect_hits * 1 + self.good_hits * 0.6 + self.bad_hits * 0.2)/(self.perfect_hits + self.good_hits + self.bad_hits + self.missed_notes)) * 100
     
        # แสดงผลความแม่นยำบนหน้าจอ
        font = pygame.font.Font(None, 36)
        accuracy_text = font.render(f"Accuracy: {self.accuracy:.2f}%", True, WHITE)
        self.screen.blit(accuracy_text, (10, 90))  # แสดงที่มุมซ้ายบน

    def draw_chart(self):
        """วาดเส้นที่ใช้แบ่งเลนสำหรับการเล่นเกม"""
        for i in range(4):
            pygame.draw.line(self.screen, config.WHITE, (i * self.lane_width, 0), (i * self.lane_width, self.HEIGHT), 2)
        pygame.draw.line(self.screen, config.WHITE, (0, self.hie_lane_y), (self.WIDTH, self.hit_lane_y), 2)  # วาดเส้น HIT_LINE_Y

    def draw_notes(self, current_time):
        """วาดโน้ตทั้งหมดและอัปเดตตำแหน่งของโน้ต"""
        for note in self.notes[:]:
            note.update_position(current_time)  # อัปเดตตำแหน่งของโน้ต
            note.draw()  # วาดโน้ต
            if note.y_position > self.HEIGHT and not note.hit:
                self.combo = 0  # รีเซ็ตคอมโบเมื่อโน้ตพลาด
                self.register_miss(note)  # ลงทะเบียนการพลาด

    def display_message(self):
        """แสดงข้อความ feedback เช่น "Perfect!", "Good!", "Missed!" เป็นต้น"""
        if self.message and (time.time() - self.message_display_time) < self.message_duration:
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, True, WHITE)
            self.screen.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))

    def display_score(self):
        """แสดงคะแนนและคอมโบ"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, config.WHITE)
        combo_text = font.render(f"Combo: {self.combo}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))  # แสดงคะแนนที่มุมซ้ายบน
        self.screen.blit(combo_text, (10, 50))  # แสดงคอมโบที่มุมซ้ายบน

    def show_game_over(self):
        """แสดงหน้าจอสรุปผลหลังจากจบเกม"""
        self.screen.fill(config.BLACK)  # ล้างหน้าจอด้วยสีดำ
        font = pygame.font.Font(None, 72)

        game_over_text = font.render("Game Over", True, config.WHITE)
        self.screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, self.HEIGHT // 4))

        score_text = font.render(f"Final Score: {self.score}", True, config.WHITE)
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, self.HEIGHT // 2))

        accuracy_text = font.render(f"Accuracy: {self.accuracy:.2f}%", True, WHITE)
        self.screen.blit(accuracy_text, (self.WIDTH // 2 - accuracy_text.get_width() // 2, self.HEIGHT // 2 + 50))

        pygame.display.flip()

        time.sleep(2)  # ให้เวลา 2 วินาที ก่อนจะกลับไปที่หน้าหลักหรือรีสตาร์ท

        # ให้ผู้เล่นเลือกว่าจะเล่นต่อหรือออกจากเกม
        self.show_restart_or_exit()

    def show_restart_or_exit(self):
        """แสดงตัวเลือกให้ผู้เล่นเลือกว่าจะเล่นใหม่หรือออก"""
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press 'R' to Restart, 'M' for Menu, 'Q' to Quit", True, config.WHITE)
        self.screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, self.HEIGHT // 2 + 150))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()  # รีเซ็ตเกมใหม่
                        waiting = False
                    elif event.key == pygame.K_m:
                        self.show_menu()  # แสดงเมนูหลัก
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def reset_game(self):
        """รีเซ็ตข้อมูลเกมเมื่อเริ่มใหม่"""
        return "gameplay", self.song_index

    def toggle_pause(self):
        """ฟังก์ชั่นที่ใช้สำหรับการหยุดหรือเล่นเพลงเมื่อเกมหยุดชั่วคราว"""
        if self.paused:
            pygame.mixer.music.unpause()  # ถ้าเกมกลับมาเล่นก็ให้เพลงเล่นต่อ
            self.paused = False
        else:
            pygame.mixer.music.pause()  # ถ้าเกมหยุดก็ให้เพลงหยุด
            self.paused = True
    
    
     
    def update_button_colors(self, buttons, mouse_pos):
        """อัพเดตสีของปุ่มเมื่อเมาส์เคลื่อนที่เข้าไป"""
        for button in buttons:
            if button.rect.collidepoint(mouse_pos):
                button.color = (200, 200, 255)  # Highlight color when hovered
            else:
                button.color = config.WHITE  # Default color

    def display_pause_menu(self):
       
        """แสดงเมนู pause ขณะที่เกมหยุดชั่วคราว"""
        self.screen.fill(config.BLACK)
        
        # Get the current mouse position (used for hover effects)
        mouse_pos = pygame.mouse.get_pos()
        
        # Font for text
        font = pygame.font.Font(config.FONT1, 150)
        
        # Create buttons using the Button class
        resume_button = config.Button("Resume", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.4) - 50, 300, 80, config.WHITE, 255)
        restart_button = config.Button("Restart", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.5) + 50, 300, 80, config.WHITE, 255)
        menu_button = config.Button("To Menu", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.6) + 150, 300, 80, config.WHITE, 255)
        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # Draw the buttons and update hover effects
        resume_button.draw(self.screen, mouse_pos)
        restart_button.draw(self.screen, mouse_pos)
        menu_button.draw(self.screen, mouse_pos)
        
        # Draw the "Game Paused" text with shadow
        pause_surface = font.render("Game Paused", True, config.WHITE)
        pause_rect = pause_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 7))
        
        shadow_surface = font.render("Game Paused", True, (255, 255, 255))  
        shadow_rect = shadow_surface.get_rect(center=(self.WIDTH // 2 + 5, self.HEIGHT // 7 + 5))  
        
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(pause_surface, pause_rect)

        # Update the display once, after all drawing
        pygame.display.flip()

        # Handling mouse events (hover and click)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if any button was clicked using collidepoint
                    if resume_button.rect.collidepoint(mouse_pos):  # Using collidepoint directly
                        self.toggle_pause()  # Or whatever action is associated with this button
                        waiting = False
                    elif restart_button.rect.collidepoint(mouse_pos):  # Using collidepoint directly
                        self.reset_game() 
                        waiting = False
                    elif  menu_button.is_clicked(mouse_pos, mouse_click):
                        return "select_song"
                    
                elif event.type == pygame.MOUSEMOTION:
                    # Highlight buttons on hover by changing their color when hovered
                    if resume_button.rect.collidepoint(event.pos):
                        resume_button.color = (200, 200, 255)  # Highlight color when hovered
                    else:
                        resume_button.color = config.WHITE  # Default color

                    if restart_button.rect.collidepoint(event.pos):
                        restart_button.color = (200, 200, 255)  # Highlight color when hovered
                    else:
                        restart_button.color = config.WHITE  # Default color

                    if menu_button.rect.collidepoint(event.pos):
                        menu_button.color = (200, 200, 255)  # Highlight color when hovered
                    else:
                        menu_button.color = config.WHITE  # Default color

            # Only update the display once after all handling is done
            pygame.display.flip()

        
       
    def show(self):
        """ลูปหลักของเกม"""
        self.load_notes(f"Notes/SONG{self.current_song_index}.txt")
        pygame.mixer.music.load(f'songs/SONG{self.current_song_index}.mp3')
        pygame.mixer.music.play()
        print(f"Notes/SONG{self.current_song_index}.txt")
        
        start_time = time.time()

        running = True
        while running:
            current_time = time.time() - start_time
            self.screen.fill(config.BLACK)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # กด ESC เพื่อหยุดหรือเล่นเกม
                        self.toggle_pause()  # เรียกใช้ฟังก์ชั่น toggle_pause
                        
                    
            if self.paused:
                self.display_pause_menu()  # เมื่อเกมหยุด ให้แสดงเมนู pause
                continue  # ข้ามการอัปเดตเกม

            keys = pygame.key.get_pressed()
            self.handle_input(keys, current_time)

            self.draw_chart()
            self.draw_notes(current_time)
            self.display_message()
            self.display_score()
            self.display_accuracy()

            pygame.display.flip()
            self.clock.tick(60)




