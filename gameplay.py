import pygame
import time
from pygame import mixer
import config

# เริ่มต้น Pygame และ mixer
pygame.init()
mixer.init()

# ขนาดหน้าจอและค่าคงที่
WIDTH, HEIGHT = 1920, 1080
LANE_WIDTH = WIDTH // 4
HIT_LINE_Y = HEIGHT - 50  # จุดที่จะตีโน้ต
NOTE_SPEED = 300  # ความเร็วของโน้ตที่ลงมา

# กำหนดสีที่ใช้ในเกม
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTE_COLOR = (0, 255, 0)

# ตัวแปรเกม
notes = []  # รายการโน้ตทั้งหมด
score = 0  # คะแนน
combo = 0  # คอมโบ
hit_notes = 0  # จำนวนโน้ตที่ถูกตี
missed_notes = 0  # จำนวนโน้ตที่พลาด
total_notes = 0  # จำนวนโน้ตทั้งหมด
accuracy = 100.0  # ความแม่นยำเริ่มต้นที่ 100%

# ตัวแปรการแสดงข้อความ
message = ""
message_display_time = 0
message_duration = 1.5  # เวลาที่จะแสดงข้อความในวินาที

# ตั้งค่าหน้าจอ Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# โหลดเพลง
pygame.mixer.music.load('songs/SONG1.mp3')
pygame.mixer.music.play()  # เล่นเพลงอย่างต่อเนื่อง

class Note:
    """คลาสที่ใช้จัดการกับพฤติกรรมของโน้ต"""
    def __init__(self, lane, spawn_time):
        self.lane = lane  # เลนที่โน้ตจะมาถึง
        self.spawn_time = spawn_time  # เวลาที่โน้ตเริ่มต้น
        self.y_position = 0  # ตำแหน่ง Y ของโน้ต
        self.hit = False  # เช็คว่าโน้ตถูกตีหรือยัง

    def update_position(self, current_time):
        """อัปเดตตำแหน่งของโน้ตตามเวลา"""
        elapsed = current_time - self.spawn_time
        self.y_position = elapsed * NOTE_SPEED  # การเคลื่อนที่ของโน้ต

    def draw(self):
        """วาดโน้ตบนหน้าจอ"""
        if self.y_position <= HEIGHT:
            pygame.draw.circle(screen, NOTE_COLOR, 
                               (self.lane * LANE_WIDTH + LANE_WIDTH // 2, 
                                int(self.y_position)), 30)

    def is_hit(self, keys, offset_tolerance):
        """เช็คว่าโน้ตถูกตีหรือไม่ โดยพิจารณาจากการกดปุ่มและระยะเบี่ยงเบนจากเส้น HIT_LINE_Y"""
        if self.hit:
            return False
        offset = abs(self.y_position - HIT_LINE_Y)
        key_mapping = [pygame.K_a, pygame.K_s, pygame.K_j, pygame.K_k]
        
        # เพิ่มระยะเบี่ยงเบนในการตีให้กว้างขึ้น
        tolerance_increase = 10  # เพิ่ม ระยะเบี่ยงเบนอีก 10
        if keys[key_mapping[self.lane]] and offset < (offset_tolerance + tolerance_increase):
            self.hit = True
            return True
        return False

class Game:
    """คลาสหลักของเกมที่ควบคุมกระบวนการต่างๆ ในเกม"""
    def __init__(self):
        self.notes = []  # รายการโน้ตทั้งหมด
        self.score = 0  # คะแนน
        self.combo = 0  # คอมโบ
        self.hit_notes = 0  # จำนวนโน้ตที่ถูกตี
        self.missed_notes = 0  # จำนวนโน้ตที่พลาด
        self.total_notes = 0  # จำนวนโน้ตทั้งหมด
        self.accuracy = 100.0  # ความแม่นยำ
        self.message = ""  # ข้อความที่จะแสดง เช่น Perfect!, Missed!
        self.message_display_time = 0  # เวลาที่จะแสดงข้อความ
        self.message_duration = 1.5  # เวลาที่จะแสดงข้อความ
        self.running = True  # สถานะการทำงานของเกม
        self.start_time = time.time()  # เวลาที่เริ่มเกม
        self.paused = False  # สถานะเกมหยุดชั่วคราว
        self.perfect_hits = 0  # จำนวนโน้ตที่ตี "Perfect!"
        self.good_hits = 0  # จำนวนโน้ตที่ตี "Good!"
        self.bad_hits = 0  # จำนวนโน้ตที่ตี "Bad!"

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
                self.notes.append(Note(lane, spawn_time))  # เพิ่มโน้ตใหม่ในรายการ
                self.total_notes += 1

    def draw_chart(self):
        """วาดเส้นที่ใช้แบ่งเลนสำหรับการเล่นเกม"""
        for i in range(5):  # Draw 5 lines
            pygame.draw.line(screen, WHITE, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 2)
        pygame.draw.line(screen, WHITE, (WIDTH, 0), (WIDTH, HEIGHT), 2)
        pygame.draw.line(screen, WHITE, (0, HIT_LINE_Y), (WIDTH, HIT_LINE_Y), 2)  # Draw the HIT_LINE_Y

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
            total_hits = (0 * self.perfect_hits) + (2 * self.good_hits) + (4 * self.bad_hits) + (5 * self.missed_notes) # คะแนนรวมจากการตีโน้ต
            self.accuracy = (5 * total_notes - total_hits) / (5 * total_notes) * 100  # คำนวณความแม่นยำเป็นเปอร์เซ็นต์

        # แสดงผลความแม่นยำบนหน้าจอ
        font = pygame.font.Font(None, 36)
        accuracy_text = font.render(f"Accuracy: {self.accuracy:.2f}%", True, WHITE)
        screen.blit(accuracy_text, (10, 90))  # แสดงที่มุมซ้ายบน

    def draw_notes(self, current_time):
        """วาดโน้ตทั้งหมดและอัปเดตตำแหน่งของโน้ต"""
        for note in self.notes[:]:
            note.update_position(current_time)  # อัปเดตตำแหน่งของโน้ต
            note.draw()  # วาดโน้ต
            if note.y_position > HEIGHT and not note.hit:
                self.combo = 0  # รีเซ็ตคอมโบเมื่อโน้ตพลาด
                self.register_miss(note)  # ลงทะเบียนการพลาด

    def display_message(self):
        """แสดงข้อความ feedback เช่น "Perfect!", "Good!", "Missed!" เป็นต้น"""
        if self.message and (time.time() - self.message_display_time) < self.message_duration:
            font = pygame.font.Font(None, 36)
            text = font.render(self.message, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    def display_score(self):
        """แสดงคะแนนและคอมโบ"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        combo_text = font.render(f"Combo: {self.combo}", True, WHITE)
        screen.blit(score_text, (10, 10))  # แสดงคะแนนที่มุมซ้ายบน
        screen.blit(combo_text, (10, 50))  # แสดงคอมโบที่มุมซ้ายบน

    def show_game_over(self):
        """แสดงหน้าจอสรุปผลหลังจากจบเกม"""
        screen.fill(BLACK)  # ล้างหน้าจอด้วยสีดำ
        font = pygame.font.Font(None, 72)

        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        accuracy_text = font.render(f"Accuracy: {self.accuracy:.2f}%", True, WHITE)
        screen.blit(accuracy_text, (WIDTH // 2 - accuracy_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        time.sleep(2)  # ให้เวลา 2 วินาที ก่อนจะกลับไปที่หน้าหลักหรือรีสตาร์ท

        # ให้ผู้เล่นเลือกว่าจะเล่นต่อหรือออกจากเกม
        self.show_restart_or_exit()

    def show_restart_or_exit(self):
        """แสดงตัวเลือกให้ผู้เล่นเลือกว่าจะเล่นใหม่หรือออก"""
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press 'R' to Restart, 'M' for Menu, 'Q' to Quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 150))

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
                        self.to_menu()  # แสดงเมนูหลัก
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def reset_game(self):
        """รีเซ็ตข้อมูลเกมเมื่อเริ่มใหม่"""
        self.notes = []  
        self.score = 0
        self.combo = 0
        self.hit_notes =  0
        self.missed_notes = 0
        self.total_notes = 0
        self.accuracy = 100.0
        self.message = ""
        self.message_display_time = 0
        self.start_time = time.time()

    def toggle_pause(self):
        """ฟังก์ชั่นที่ใช้สำหรับการหยุดหรือเล่นเพลงเมื่อเกมหยุดชั่วคราว"""
        if self.paused:
            pygame.mixer.music.unpause()  # ถ้าเกมกลับมาเล่นก็ให้เพลงเล่นต่อ
            self.paused = False
        else:
            pygame.mixer.music.pause()  # ถ้าเกมหยุดก็ให้เพลงหยุด
            self.paused = True

    def to_menu(self):
        return 'select_song'

    def display_pause_menu(self):
        """แสดงเมนู pause ขณะที่เกมหยุดชั่วคราว"""
        screen.fill(BLACK)

        # Get the current mouse position (used for hover effects)
        mouse_pos = pygame.mouse.get_pos()

        # Font for text
        font = pygame.font.Font(None, 150)

        # Create buttons using the Button class
        resume_button = config.Button("Resume", 40, int(WIDTH * 0.5), int(HEIGHT * 0.4) - 50, 300, 80, WHITE, 255)
        restart_button = config.Button("Restart", 40, int(WIDTH * 0.5), int(HEIGHT * 0.5) + 50, 300, 80, WHITE, 255)
        menu_button = config.Button("To Menu", 40, int(WIDTH * 0.5), int(HEIGHT * 0.6) + 150, 300, 80, WHITE, 255)

        # Draw the buttons and update hover effects
        resume_button.draw(screen, mouse_pos)
        restart_button.draw(screen, mouse_pos)
        menu_button.draw(screen, mouse_pos)

        # Draw the "Game Paused" text with shadow
        pause_surface = font.render("Game Paused", True, WHITE)
        pause_rect = pause_surface.get_rect(center=(WIDTH // 2, HEIGHT // 7))

        shadow_surface = font.render("Game Paused", True, (255, 255, 255))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 5, HEIGHT // 7 + 5))

        screen.blit(shadow_surface, shadow_rect)
        screen.blit(pause_surface, pause_rect)

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
                    if resume_button.rect.collidepoint(mouse_pos):
                        self.toggle_pause()
                        waiting = False
                    elif restart_button.rect.collidepoint(mouse_pos):
                        self.reset_game()
                        waiting = False
                    elif menu_button.rect.collidepoint(mouse_pos):
                        self.to_menu()

                elif event.type == pygame.MOUSEMOTION:
                    # Highlight buttons on hover by changing their color when hovered
                    if resume_button.rect.collidepoint(event.pos):
                        resume_button.color = (200, 200, 255)
                    else:
                        resume_button.color = WHITE

                    if restart_button.rect.collidepoint(event.pos):
                        restart_button.color = (200, 200, 255)
                    else:
                        restart_button.color = WHITE

                    if menu_button.rect.collidepoint(event.pos):
                        menu_button.color = (200, 200, 255)
                    else:
                        menu_button.color = WHITE

            # Only update the display once after all handling is done
            pygame.display.flip()

    def game_loop(self):
        """ลูปหลักของเกม"""
        self.load_notes("Notes/SONG1.txt")
        start_time = time.time()

        running = True
        while running:
            current_time = time.time() - start_time
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # กด ESC เพื่อหยุดหรือเล่นเกม
                        self.toggle_pause()

            if self.paused:
                self.display_pause_menu()  # เมื่อเกมหยุด ให้แสดงเมนู pause
                continue  # ข้ามการอัปเดตเกม

            keys = pygame.key.get_pressed()
            self.handle_input(keys, current_time)

            self .draw_chart()
            self.draw_notes(current_time)
            self.display_message()
            self.display_score()
            self.display_accuracy()
            self.show_game_over()

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()  # สร้างอินสแตนซ์ของคลาส Game
    game.game_loop()  # เรียกเมธอด game_loop() ผ่านอินสแตนซ์