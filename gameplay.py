import pygame
import time
from pygame import mixer
import config
from select_song import *
from option import *

class Note:
    def __init__(self, lane, spawn_time, hit_lane_y, duration=None):
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        self.lane = lane
        self.spawn_time = spawn_time
        self.hit_lane_y = hit_lane_y  # รับค่า hit_lane_y จากภายนอก
        self.duration = duration
        self.hit = False
        self.note_speed = 300
        self.note_color = (0, 255, 0)
        self.lane_width = self.WIDTH / 8
        self.center_offset = (self.WIDTH - (self.lane_width * 4)) / 2
        self.hit_line_y = self.HEIGHT - 50  # จุดที่จะตีโน้ต
        self.note_height_offset = 0
        self.y_position = 0

    def update_position(self, current_time):
        self.elapsed = current_time - self.spawn_time
        self.y_position = self.elapsed * self.note_speed

    def draw(self):
        if self.y_position <= self.HEIGHT:
            # คำนวณตำแหน่ง x โดยใช้ center offset
            x_position = self.lane * self.lane_width + self.lane_width // 2 + self.center_offset
            pygame.draw.circle(self.screen, self.note_color, 
                               (int(x_position), int(self.y_position)), 30)

    def is_hit(self, keys, offset_tolerance, key_bindings):
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



class Gameplay:
    def __init__(self, game, song_index):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen
        self.key_bindings = game.option.key_bindings
        # กำหนด song_index ที่ได้รับมา
        self.song_index = song_index
        
        # สร้างชื่อเพลงจาก song_index
        self.song_name = f"SONG{self.song_index + 1}"  # เพิ่ม 1 เพราะ index เริ่มจาก 0
        
        # หาก song_index เกินขอบเขตของ songLIST ให้ตั้งค่า song เป็น None
        if self.song_index < len(config.songLIST):
            self.song = config.songLIST[self.song_index]
        else:
            self.song = None  # หรือสามารถจัดการกับกรณีนี้เพิ่มเติม
        
        self.background_images = []
        for i in range(len(config.songLIST)):  # แก้ไขให้ตรงกับจำนวนเพลงที่มี
            image_path = f"picture/BACKGROUND/BGB{i+1}.png"
            try:
                # โหลดและเพิ่มภาพพื้นหลัง
                self.background_images.append(pygame.transform.scale(pygame.image.load(image_path), (self.WIDTH, self.HEIGHT)))
            except pygame.error as e:
                print(f"Error loading image {image_path}: {e}")

        self.lane_width = self.WIDTH / 8
        self.center_offset = (self.WIDTH - (self.lane_width * 4)) / 2
        self.hit_line_y = self.HEIGHT - 50  # จุดที่จะตีโน้ต
        self.note_height_offset = 0

        self.settings = config.load_settings()
        self.note_speed = self.settings.get("note_speed")  # ความเร็วของโน้ตที่ลงมา

        self.messege_display_time = 0
        self.messege_duration = 1.5

        self.clock = pygame.time.Clock()

        # กำหนดค่าเริ่มต้นให้กับ lane และ spawn_time
        self.lane = 0  # กำหนดให้เริ่มจากเลนที่ 0
        self.spawn_time = time.time()  # เริ่มต้นเวลา spawn_time ใช้เวลาปัจจุบัน (หรือใช้ค่าที่เหมาะสม)

        # สร้างโน้ตใหม่ที่กำหนด lane และ spawn_time
        self.Note = Note(self.lane, self.spawn_time, self.hit_line_y, duration=None)

        self.notes = []  # รายการโน้ตที่กำหนดขึ้น
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
                if len(parts) != 2:
                    print(f"Skipping invalid line: {line.strip()}")  # ข้ามบรรทัดที่ไม่ถูกต้อง
                    continue
                lane = int(parts[0])  # เลนที่โน้ตจะไป
                spawn_time = float(parts[1])  # เวลาที่โน้ตจะปรากฏ

                # สร้างโน้ตใหม่พร้อมกับ hit_lane_y
                self.notes.append(Note(lane, spawn_time, self.hit_line_y))  # ส่ง hit_line_y ไปให้ Note
                self.total_notes += 1


    def handle_input(self, keys, current_time):
        """จัดการกับการกดปุ่มและตรวจสอบการตีโน้ต"""
        hit_tolerances = [10, 20, 30]  # ความเบี่ยงเบนสำหรับการตี Perfect, Good, Bad
        hit_messages = ["Perfect!", "Good!", "Bad!"]  # ข้อความที่แสดงเมื่อตีโน้ต
        points = [500, 300, 100]  # คะแนนสำหรับแต่ละประเภทของการตีโน้ต

        if self.paused:  # ถ้าเกมหยุดชั่วคราว
            return

        # ตรวจสอบว่า key_bindings มีอยู่ใน self.game.gameplay หรือไม่
        if not hasattr(self.game.gameplay, 'key_bindings'):
            print("Error: key_bindings not found!")
            return  # ไม่ทำอะไรถ้าไม่มี key_bindings

        key_bindings = self.game.gameplay.key_bindings  # ดึง key_bindings จาก gameplay

        # ตรวจสอบว่า key_bindings มีค่าเป็น dictionary หรือไม่
        if not isinstance(key_bindings, dict):
            print("Error: key_bindings is not a dictionary!")
            return  # หากไม่ใช่ dictionary ให้หยุดการทำงาน

        # ลูปผ่านโน้ตทั้งหมด
        for note in self.notes[:]:  
            for i, tolerance in enumerate(hit_tolerances):  # ตรวจสอบแต่ละระดับของการตีโน้ต
                if note.is_hit(keys, tolerance, key_bindings):  # ส่ง key_bindings ให้ฟังก์ชัน is_hit()
                    self.register_hit(note, points[i], hit_messages[i])
                    break

    def show_hit_flash(self, x_position, y_position):
        """แสดงแฟลชที่จุดที่โน้ตถูกตี"""
        flash_color = (255, 255, 255)
        for radius in range(10, 30, 5):
            pygame.draw.circle(self.screen, flash_color, (x_position, y_position), radius, 2)

    def register_hit(self, note, points, hit_message):
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
        """วาดเส้นที่ใช้แบ่งเลนสำหรับการเล่นเกม และเพิ่มเส้นขอบด้านขวาสำหรับเลนสุดท้าย"""
        for i in range(4):
            pygame.draw.line(self.screen, config.WHITE, (i * self.lane_width + self.center_offset, 0), (i * self.lane_width + self.center_offset, self.HEIGHT), 2)
        # เพิ่มเส้นขอบด้านขวาสำหรับเลนที่ 4
        pygame.draw.line(self.screen, config.WHITE, (self.center_offset + 4 * self.lane_width, 0), (self.center_offset + 4 * self.lane_width, self.HEIGHT), 2)
        # วาดเส้นที่ตำแหน่งตีโน้ต
        pygame.draw.line(self.screen, config.WHITE, (self.center_offset, self.hit_line_y), (self.center_offset + 4 * self.lane_width, self.hit_line_y), 2)

    def draw_notes(self, current_time):
        """วาดโน้ตทั้งหมดและอัปเดตตำแหน่งของโน้ต"""
        for note in self.notes[:]:
            note.update_position(current_time)  # อัปเดตตำแหน่งของโน้ต
            note.draw()  # วาดโน้ต
            if note.y_position > self.HEIGHT and not note.hit:
                self.combo = 0  # รีเซ็ตคอมโบเมื่อโน้ตพลาด
                self.register_miss(note)  # ลงทะเบียนการพลาด

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

    def toggle_pause(self):
        """ฟังก์ชั่นที่ใช้สำหรับการหยุดหรือเล่นเพลงเมื่อเกมหยุดชั่วคราว"""
        if self.paused:
            pygame.mixer.music.unpause()  # ถ้าเกมกลับมาเล่นก็ให้เพลงเล่นต่อ
            self.paused = False
        else:
            pygame.mixer.music.pause()  # ถ้าเกมหยุดก็ให้เพลงหยุด
            self.paused = True
    
    def draw_combo_effects(self):
        """Draw effects for high combo counts."""
        if self.combo >= 10:  # Only start effects if combo is high
            color_intensity = min(255, self.combo * 10)  # Intensity based on combo count
            color = (255, color_intensity, color_intensity)  # Red-ish color based on combo
            effect_radius = min(100, self.combo * 3)  # Increase radius with combo
            
            pygame.draw.circle(self.screen, color, 
                            (self.WIDTH // 2, self.hit_line_y), 
                            effect_radius, 5)
     
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
        self.load_notes(f"Notes/SONG{self.song_index}.txt")
        pygame.mixer.music.load(f'songs/SONG{self.song_index}.mp3')
        pygame.mixer.music.play()
        print(f"Notes/SONG{self.song_index}.txt")
        
        start_time = time.time()
        running = True
        while running:
            current_time = time.time() - start_time

            # วาดภาพพื้นหลังตาม song_index
            if 0 <= self.song_index - 1 < len(self.background_images):
                self.screen.blit(self.background_images[self.song_index - 1], (0, 0))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()

            if self.paused:
                self.display_pause_menu()
                continue

            keys = pygame.key.get_pressed()
            self.handle_input(keys, current_time)

            self.draw_chart()
            self.draw_notes(current_time)
            self.display_message()
            self.display_score()
            self.display_accuracy()

            pygame.display.flip()
            self.clock.tick(60)