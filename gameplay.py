"""
import pygame
import note.py
พื้นหลังตามเพลงที่เลือก
สร้างเกมเพลย์คร่าวๆก็แบ่งบล๊อค(ตามเพลงก็แบ่งตามจังหวะโน๊ตหรือครึ่งโน๊ตกุก็ไม่รู้เล่นดนตรีไม่เป็น)โดยในไฟล์ .txt ก็บรรทัดละบล๊อค
จับจังหวะผู้เล่น หากกดยิ่งใกล้บล๊อคยิ่งได้คะแนนเยอะ(สมมติ 1 บล๊อค = 100 จุดกลาง = 50 ถ้ากด +-5 = PERFECT กด +-30 = GOOD กดดดนที่เหลือ = BAD ถ้ากดไม่โดน = MISS)
ในไฟล์ note จะมีทั้งกด1ครั้งและกดค้่าง
score จะแสดงให้ดูขวาบน
กด ESC เพื่อpauseโดยมีปุ่ม
resume-เพื่อเล่นค่อ
option-ก็option
quit-ออกจากplay
เมื่อเล่นเสดจะไปหน้า summary
แฮมทำ
"""
import pygame
import time
from pygame import mixer

# Initialize Pygame and the mixer
pygame.init()
mixer.init()

# Screen dimensions and constants
WIDTH, HEIGHT = 800, 600
LANE_WIDTH = WIDTH // 4
HIT_LINE_Y = HEIGHT - 50  
NOTE_SPEED = 300  

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTE_COLOR = (0, 255, 0)

# Game variables
notes = []
score = 0
combo = 0
hit_notes = 0
missed_notes = 0

# Message display variables
message = ""
message_display_time = 0
message_duration = 1.5  # Display time for the message in seconds

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load the song
pygame.mixer.music.load('songs/SONG1.mp3')
pygame.mixer.music.play()  # Play the song indefinitely

def load_notes(file_name):
    with open(file_name, "r") as f:
        for line in f:
            lane, spawn_time, note_type = line.strip().split(",")
            notes.append({
                "lane": int(lane),
                "spawn_time": float(spawn_time),
                "y_position": 0,
                "hit": False,
                "type": note_type  # Store the note type as a string
            })


def draw_chart():
    for i in range(4):
        pygame.draw.line(screen, WHITE, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (0, HIT_LINE_Y), (WIDTH, HIT_LINE_Y), 2)  # Hit line

def handle_input(keys, current_time):
    global score, combo, hit_notes, message, message_display_time

    for note in notes[:]:  
        if note["hit"]:
            continue

        offset = abs(note["y_position"] - HIT_LINE_Y)

        if (note["lane"] == 0 and keys[pygame.K_a]) or \
           (note["lane"] == 1 and keys[pygame.K_s]) or \
           (note["lane"] == 2 and keys[pygame.K_d]) or \
           (note["lane"] == 3 and keys[pygame.K_f]):

            if offset < 10:  # Perfect
                register_hit(note, 500, "Perfect!")
            elif offset < 20:  # Good
                register_hit(note, 300, "Good!")
            elif offset < 30:  # Bad
                register_hit(note, 100, "Bad!")

def register_hit(note, points, hit_message):
    global score, combo, hit_notes, message, message_display_time

    note["hit"] = True
    score += points
    combo += 1
    hit_notes += 1
    notes.remove(note)
    message = hit_message
    message_display_time = time.time()  # Record when the message was set

def draw_notes(current_time):
    global combo, missed_notes

    for note in notes[:]:
        elapsed = current_time - note["spawn_time"]
        note["y_position"] = elapsed * NOTE_SPEED

        if note["y_position"] <= HEIGHT:
            pygame.draw.circle(screen, NOTE_COLOR, (note["lane"] * LANE_WIDTH + LANE_WIDTH // 2, int(note["y_position"])), 20)
        else:
            if not note["hit"]:
                combo = 0
                missed_notes += 1
                notes.remove(note)

def display_message():
    if message and (time.time() - message_display_time) < message_duration:
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    combo_text = font.render(f"Combo: {combo}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(combo_text, (10, 50))

def game_loop():
    running = True
    load_notes("notes.txt")
    start_time = time.time()

    while running:
        current_time = time.time() - start_time
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        handle_input(keys, current_time)

        draw_chart()
        draw_notes(current_time)
        display_message()
        display_score()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
