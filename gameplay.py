import pygame
import time
from pygame import mixer
import config
from select_song import *
from option import *
import SongNoteGen

class Note:
    def __init__(self, screen, lane, spawn_time, hit_lane_y, note_speed=300):
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = screen
        self.lane = lane
        self.screen = screen
        self.spawn_time = spawn_time
        self.hit_lane_y = hit_lane_y  # รับค่า hit_lane_y จากภายนอก
        self.hit = False
        self.note_speed = note_speed*300 # รับ note_speed จากภายนอก
        self.note_color = (0, 255, 0)
        self.lane_width = self.WIDTH / 8
        self.hit_line_y = self.HEIGHT - 150  # จุดที่จะตีโน้ต
        self.note_height_offset = 0
        self.y_position = 0

    def update_position(self, current_time):
        self.elapsed = current_time - self.spawn_time
        self.y_position = self.elapsed * self.note_speed  # ใช้ note_speed ในการอัปเดตตำแหน่ง

    def draw(self):
        if self.y_position <= self.HEIGHT:
            pygame.draw.circle(self.screen, self.note_color, (self.lane * self.lane_width + self.lane_width // 2 + self.WIDTH // 4, int(self.y_position)), 50)

    def check_hit(self, keys, offset_tolerance, key_bindings):
        """Check if the note is hit by checking the offset tolerance and key press."""
        
        # Return early if the note has already been hit
        if self.hit:
            return False

        # Calculate the offset between the note's y-position and the hit lane y position
        offset = abs(self.y_position - self.hit_lane_y)

        # Retrieve custom keys for the actions D, F, K, L from the key_bindings dictionary
        custom_keys = [key_bindings.get(action) for action in ["D", "F", "K", "L"]]

        # Add an additional tolerance for the hit detection
        tolerance_increase = 10  

        # Ensure the lane index is valid and within range
        if 0 <= self.lane < len(custom_keys):
            key_to_check = custom_keys[self.lane]
            
            # Ensure key_to_check is not None and that the corresponding key is pressed
            if key_to_check is not None:
                # Check if the key is pressed using pygame's key state
                if keys[key_to_check] and offset < (offset_tolerance + tolerance_increase):
                    self.hit = True
                    return True
        
        return False

class Long_Note:
    def __init__(self, screen, lane, spawn_time, duration,  hit_lane_y, note_speed=300):
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = screen
        self.lane = lane
        self.screen = screen
        self.spawn_time = spawn_time
        self.hit_lane_y = hit_lane_y  # รับค่า hit_lane_y จากภายนอก
        self.duration = duration
        self.hit = False
        self.note_speed = note_speed * 300 # รับ note_speed จากภายนอก
        self.note_color = (0, 255, 0)
        self.lane_width = self.WIDTH / 8
        self.hit_line_y = self.HEIGHT - 150  # จุดที่จะตีโน้ต
        self.note_height_offset = 0
        self.y_position = 0
        self.is_pressed = False
        self.is_hit = False
        self.hit_rect = None
        self.last_hit_time = 0

    def update_position(self, current_time):
        self.elapsed_start = current_time - self.spawn_time
        self.elapsed_end = current_time - self.duration
        self.y_position_start = self.elapsed_start * self.note_speed  # ใช้ note_speed ในการอัปเดตตำแหน่ง
        self.y_position_end = self.elapsed_end * self.note_speed

        lane_x = self.lane * self.lane_width + self.lane_width // 2
        if 0 <= self.y_position_start <= self.HEIGHT:
            self.hit_rect = pygame.Rect(lane_x - 10, self.y_position_start - 20, 20, 40)  # ตัวอย่างขนาด hit_rect

    def draw(self):
        lane_x = self.lane * self.lane_width + self.lane_width // 2 + self.WIDTH // 4  # ตำแหน่ง x ของเลน

        # วาดวงกลมที่จุดเริ่มต้นของโน้ตยาว (ต้นโน้ต)
        if 0 <= self.y_position_start <= self.HEIGHT:
            pygame.draw.circle(self.screen, self.note_color, (lane_x, self.y_position_start), 50)
        
        # วาดสี่เหลี่ยมเพื่อแสดงระยะความยาว duration ของโน้ตยาว
        if 0 <= self.y_position_start <= self.HEIGHT or self.y_position_end > 0:
            y_top = min(self.y_position_start, self.y_position_end)
            y_bottom = max(self.y_position_start, self.y_position_end)

            if y_bottom > self.HEIGHT:
                y_bottom = self.HEIGHT

            pygame.draw.rect(self.screen, self.note_color, (lane_x - 25, int(y_top), 50, int(y_bottom - y_top)))
        
        # วาดวงกลมที่จุดสิ้นสุดของโน้ตยาว (ปลายโน้ต)
        if 0 <= self.y_position_end <= self.HEIGHT:
            pygame.draw.circle(self.screen, self.note_color, (lane_x, int(self.y_position_end)), 50)

    def check_hit(self, keys, offset_tolerance, key_bindings, current_time):
        """Check if the long note is hit by checking the offset tolerance, key press, and note duration."""

        # Return early if the note has already been hit or is released
        if self.is_pressed or self.is_hit:
            return False

        # Check if the key is still pressed at the start of the long note
        custom_keys = [key_bindings.get(action) for action in ["D", "F", "K", "L"]]

        if 0 <= self.lane < len(custom_keys):
            key_to_check = custom_keys[self.lane]

            # Ensure key_to_check is not None and that the corresponding key is pressed
            if key_to_check is not None and keys[key_to_check]:
                # Ensure the key is pressed at the start of the note
                if 0 <= self.y_position_start <= self.HEIGHT:
                    # ตรวจสอบว่ากดค้างที่จุดเริ่มต้นหรือไม่
                    if not self.is_pressed:
                        if self.hit_rect.collidepoint(self.lane * self.lane_width + self.lane_width // 2, self.hit_line_y):
                            self.is_pressed = True
                            self.is_hit = True  # Mark the note as hit

                            # Register hit every 1 second while the key is pressed
                            if current_time - self.last_hit_time >= 1:  # Every 1 second
                                self.last_hit_time = current_time
                                return True

        # หากมือถูกปล่อยออกจากปุ่มหรือโน้ตไม่ตรงกับเงื่อนไข ไม่ให้กดที่เส้นระหว่างและจุดปลาย
        if not keys[key_to_check] and self.is_pressed:
            self.is_pressed = False  # กดปล่อยมือแล้วให้กลับมาเป็น False
            return False

        return False


class Gameplay:
    def __init__(self, game, song_index):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen
        self.key_bindings = game.option.key_bindings
        self.song_index = song_index
        self.select_song = SelectSong(self)

        self.hit_sound = pygame.mixer.Sound("Notes/Hit_Sound.mp3")
        self.hit_sound.set_volume(0.2)
        
        # สร้างชื่อเพลงจาก song_index
        self.song_name = f"SONG{self.song_index + 1}"  # เพิ่ม 1 เพราะ index เริ่มจาก 0
        
        # หาก song_index เกินขอบเขตของ songLIST ให้ตั้งค่า song เป็น None
        if self.song_index < len(config.songLIST):
            self.song = config.songLIST[self.song_index]
        else:
            self.song = None  # หรือสามารถจัดการกับกรณีนี้เพิ่มเติม
        
        self.lane_width = self.WIDTH / 8
        self.hit_line_y = self.HEIGHT - 150  # จุดที่จะตีโน้ต
        self.note_height_offset = 0

        self.settings = config.load_settings()  # โหลดการตั้งค่าจาก config
        self.note_speed = self.settings.get("note_speed", 300)  # ใช้ note_speed ที่ตั้งไว้

        self.messege_display_time = 0
        self.messege_duration = 1.5

        self.clock = pygame.time.Clock()

        self.lane = 0  # กำหนดให้เริ่มจากเลนที่ 0
        self.spawn_time = time.time()  # เริ่มต้นเวลา spawn_time ใช้เวลาปัจจุบัน (หรือใช้ค่าที่เหมาะสม)

        self.notes = []  # รายการโน้ตที่กำหนดขึ้น
        self.long_notes = []
        self.score = 0 
        self.combo = 0  
        self.hit_notes = 0 
        self.missed_notes = 0  
        self.total_notes = 0  
        self.accuracy = 100.0  
        self.message = ""  
        self.message_display_time = 0 
        self.message_duration = 1.5  
        self.running = True  
        self.start_time = time.time() 
        self.paused = False  
        self.perfect_hits = 0  
        self.good_hits = 0  
        self.bad_hits = 0  

    def load_notes(self, file_name):
        """โหลดโน้ตจากไฟล์"""
        with open(file_name, "r") as f:
            for line in f:
                parts = line.strip().split(",")  # แยกข้อมูลที่ใช้คั่นด้วยเครื่องหมายจุลภาค
                lane = int(parts[0])  # เลนที่โน้ตจะไป
                spawn_time = float(parts[1]) # เวลาที่โน้ตจะปรากฏ
                if len(parts) == 2:
                    self.notes.append(Note(self.screen, lane, spawn_time, self.hit_line_y, note_speed=self.note_speed)) 
                elif len(parts) == 3:
                    duration = float(parts[2])
                    self.long_notes.append(Long_Note(self.screen, lane, spawn_time, duration, self.hit_line_y, note_speed=self.note_speed))  
                else:
                    print("Error load_notes")
                self.total_notes += 1

    def handle_input(self, keys, current_time):
        """จัดการกับการกดปุ่มและตรวจสอบการตีโน้ต"""
        hit_tolerances = [10, 20, 30]  # ความเบี่ยงเบนสำหรับการตี Perfect, Good, Bad
        hit_messages = ["Perfect!", "Good!", "Bad!"]  # ข้อความที่แสดงเมื่อตีโน้ต
        points = [500, 300, 100]  # คะแนนสำหรับแต่ละประเภทของการตีโน้ต

        if self.paused:  # ถ้าเกมหยุดชั่วคราว
            return

        key_bindings = self.game.gameplay.key_bindings  # ดึง key_bindings จาก gameplay

        for note in self.notes[:]:  
            for i, tolerance in enumerate(hit_tolerances):  # ตรวจสอบแต่ละระดับของการตีโน้ต
                if note.check_hit(keys, tolerance, key_bindings):  # ส่ง key_bindings ให้ฟังก์ชัน is_hit()
                    self.register_hit(note, points[i], hit_messages[i])
                    break

        for long_note in self.long_notes[:]:  
            for i, tolerance in enumerate(hit_tolerances):  # ตรวจสอบแต่ละระดับของการตีโน้ต
                if long_note.check_hit(keys, tolerance, key_bindings, current_time):  # ส่ง key_bindings ให้ฟังก์ชัน is_hit()
                    self.register_hit(note, points[i], hit_messages[i])
                    break

    def register_hit(self, note, points, hit_message):
        """ลงทะเบียนการตีโน้ต"""
        self.score += points  # เพิ่มคะแนนตามประเภทของการตี
        self.combo += 1  # เพิ่มคอมโบ
        self.hit_notes += 1  # เพิ่มจำนวนโน้ตที่ถูกตี

        self.hit_sound.play() # เล่นเสียงตอนกด

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
        for i in range(5):
            pygame.draw.line(self.screen, config.WHITE, (i * self.lane_width + self.WIDTH // 4, 0), (i * self.lane_width+ self.WIDTH // 4, self.HEIGHT), 2)
        for i in range(4):
            circle_surface = pygame.Surface((100, 100), pygame.SRCALPHA)  
            circle_surface = circle_surface.convert_alpha()  

            pygame.draw.circle(circle_surface, (255, 255, 255, 255), (50, 50), 50) 
            pygame.draw.circle(circle_surface, (0, 0, 0, 0), (50, 50), 45)  

            self.screen.blit(circle_surface, (i * self.lane_width + self.lane_width // 2 + self.WIDTH // 4 - 50, int(self.hit_line_y) - 50))

    def draw_notes(self, current_time):
        """วาดโน้ตทั้งหมดและอัปเดตตำแหน่งของโน้ต"""
        for note in self.notes[:]:
            note.update_position(current_time)  # อัปเดตตำแหน่งของโน้ต
            note.draw()  # วาดโน้ต
            if note.y_position > self.HEIGHT and not note.hit:
                self.combo = 0  # รีเซ็ตคอมโบเมื่อโน้ตพลาด
                self.register_miss(note)  # ลงทะเบียนการพลาด
        
        for long_note in self.long_notes[:]:
            long_note.update_position(current_time)  # อัปเดตตำแหน่งของโน้ต
            long_note.draw()  # วาดโน้ต
            if long_note.y_position > self.HEIGHT and not long_note.hit:
                self.combo = 0  # รีเซ็ตคอมโบเมื่อโน้ตพลาด
                self.register_miss(long_note)  # ลงทะเบียนการพลาด

    def display_message(self):
        if self.message and (time.time() - self.message_display_time) < self.message_duration:
            font = pygame.font.Font(None, 72)
            
            # ตั้งสีข้อความ
            if self.message == "Perfect!":
                text_color = (0, 255, 0)  # Green
            elif self.message == "Good!":
                text_color = (255, 165, 0)  # Orange
            elif self.message == "Bad!":
                text_color = (255, 0, 0)  # Red
            elif self.message == "Missed!":
                text_color = (128, 128, 128)  # Gray

            message_surface = font.render(self.message, True, text_color)
            
            # ข้อความกลางจอ
            x, y = self.WIDTH // 2 - message_surface.get_width() // 2, self.HEIGHT // 3
            self.screen.blit(message_surface, (x, y))

    def display_score(self):
        """แสดงคะแนนและคอมโบ"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, config.WHITE)
        combo_text = font.render(f"Combo: {self.combo}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))  # แสดงคะแนนที่มุมซ้ายบน
        self.screen.blit(combo_text, (10, 50))  # แสดงคอมโบที่มุมซ้ายบน

     

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
        self.fade(fade_out=True)  # เริ่ม fade out
        self.fade(fade_out=False)  # เริ่ม fade in       
        self.notes = []  # Clear the list of notes
        self.score = 0
        self.combo = 0
        self.hit_notes = 0
        self.missed_notes = 0
        self.total_notes = 0
        self.accuracy = 100.0
        self.message = ""
        self.message_display_time = 0
        self.start_time = time.time()  # Reset the game timer
        self.paused = False  # Unpause if game was paused
        self.perfect_hits = 0
        self.good_hits = 0
        self.bad_hits = 0
        self.missed_notes = 0
        self.show()


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
        
        mouse_pos = pygame.mouse.get_pos()

        # Font for text
        font = pygame.font.Font(config.FONT1, 150)

        # Create buttons using the Button class
        menu_button = config.Button("To Menu", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.4) - 50, 300, 80, config.WHITE, 255)
        resume_button = config.Button("Resume", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.5) + 50, 300, 80, config.WHITE, 255)
        restart_button = config.Button("Restart", 40, int(self.WIDTH * 0.5), int(self.HEIGHT * 0.6) + 150, 300, 80, config.WHITE, 255)

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

        pygame.display.flip()  # Update the display

        # Handle mouse events (clicking on buttons)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if any button was clicked using collidepoint
                    if resume_button.rect.collidepoint(mouse_pos):  # Resume
                        self.toggle_pause()
                        waiting = False
                    elif restart_button.rect.collidepoint(mouse_pos):  # Restart
                        self.reset_game()
                        waiting = False
                    elif menu_button.rect.collidepoint(mouse_pos):  # To Menu
                        # Fade-out, then switch to the menu, then fade-in
                        self.fade(fade_out=True) 
                        waiting = False  
                        return "select_song"

                        
                elif event.type == pygame.MOUSEMOTION:
                    # Highlight buttons on hover
                    if resume_button.rect.collidepoint(event.pos):
                        resume_button.color = (200, 200, 255)
                    else:
                        resume_button.color = config.WHITE

                    if restart_button.rect.collidepoint(event.pos):
                        restart_button.color = (200, 200, 255)
                    else:
                        restart_button.color = config.WHITE

                    if menu_button.rect.collidepoint(event.pos):
                        menu_button.color = (200, 200, 255)
                    else:
                        menu_button.color = config.WHITE

            pygame.display.flip()


    def fade(self, fade_out=True, speed=5):
        """สร้างเอฟเฟกต์ Fade (เข้าหรือออก)"""
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill((0, 0, 0))  # เติมสีดำ
        alpha = 0 if fade_out else 255  # ตั้งค่า alpha เริ่มต้น

        # กำหนดให้สีมีความทึบ (alpha) ตั้งแต่ 0 (โปร่งใส) ถึง 255 (ทึบสุด)
        if fade_out:
            while alpha < 255:
                alpha += speed
                fade_surface.set_alpha(alpha)
                self.screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)
        else:
            while alpha > 0:
                alpha -= speed
                fade_surface.set_alpha(alpha)
                self.screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)
    

    def show(self):
        """ลูปหลักของเกม"""
        SongNoteGen.analyze_song(self.song_index)
        self.load_notes(f"Notes/song_note.txt")
        
        start_time = time.time()
        background_image = pygame.image.load(f'picture/BACKGROUND/BG{self.song_index}.png')
        background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
        
        # สร้าง overlay ที่มีความโปร่งใส
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        
        # เริ่มต้นด้วยการวาดพื้นหลังและ overlay
        self.screen.blit(background_image, (0, 0))
        self.screen.blit(overlay, (0, 0))

        # กำหนดสถานะ paused และตัวแปร music_played
        self.paused = False
        music_played = False  # ตัวแปรเพื่อให้เพลงเล่นแค่ครั้งเดียว

        while True:
            current_time = time.time() - start_time

            # ถ้าถึงเวลาที่กำหนดให้เล่นเพลง
            if not music_played and 2.7 <= current_time <= 2.9:
                pygame.mixer.music.load(f'songs/SONG{self.song_index}.mp3')
                pygame.mixer.music.play()
                music_played = True  # ตั้งค่าให้ไม่เล่นเพลงซ้ำ

            # วาดพื้นหลังและ overlay ทุกเฟรม
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(overlay, (0, 0))

            # การจัดการอีเวนต์
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # กด ESC เพื่อหยุดหรือเล่นเกม
                        self.toggle_pause()
                        self.paused = True # สลับสถานะ paused

            # ถ้าเกมถูกหยุด (paused) จะแสดงเมนู Pause
                if self.paused:
                    result = self.display_pause_menu()
                    if result == "select_song":
                        song_result, song_index = self.game.select_song.show()
                        if song_result == "gameplay":
                            self.song_index = song_index  # เลือกเพลงใหม่
                            self.paused = False  # ปิดสถานะ paused
                            return "select_song"  # ส่งผลให้กลับไปที่หน้าเลือกเพลง
                        elif song_result == "title":
                            return "title"
                    elif result == "resume":
                        self.paused = False
                        continue  # กลับไปเล่นเกม
            
            # ถ้าเกมไม่ได้หยุด (ไม่ได้อยู่ในสถานะ paused) ให้ทำการอัปเดตสถานะต่างๆ
            if not self.paused:
                keys = pygame.key.get_pressed()
                self.handle_input(keys, current_time)

                # ฟังก์ชันการวาดต่างๆ
                self.draw_chart()
                self.draw_notes(current_time)
                self.display_message()
                self.display_score()
                self.display_accuracy()

            # อัปเดตการแสดงผล
            pygame.display.flip()

            # ควบคุมอัตราเฟรมให้คงที่ที่ 60 fps
            self.clock.tick(60)
