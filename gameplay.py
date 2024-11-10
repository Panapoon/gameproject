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
total_notes = 0
accuracy = 100.0

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

class Note:
    def __init__(self, lane, spawn_time):
        self.lane = lane
        self.spawn_time = spawn_time
        self.y_position = 0
        self.hit = False

    def update_position(self, current_time):
        elapsed = current_time - self.spawn_time
        self.y_position = elapsed * NOTE_SPEED

    def draw(self):
        if self.y_position <= HEIGHT:
            pygame.draw.circle(screen, NOTE_COLOR, (self.lane * LANE_WIDTH + LANE_WIDTH // 2, int(self.y_position)), 20)

    def is_hit(self, keys, offset_tolerance):
        if self.hit:
            return False
        offset = abs(self.y_position - HIT_LINE_Y)
        key_mapping = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]
        if keys[key_mapping[self.lane]] and offset < offset_tolerance:
            self.hit = True
            return True
        return False

def load_notes(file_name):
    global total_notes
    with open(file_name, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 2:
                print(f"Skipping invalid line: {line.strip()}")
                continue
            lane = int(parts[0])
            spawn_time = float(parts[1])
            notes.append(Note(lane, spawn_time))
            total_notes += 1


def draw_chart():
    for i in range(4):
        pygame.draw.line(screen, WHITE, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (0, HIT_LINE_Y), (WIDTH, HIT_LINE_Y), 2)

def handle_input(keys, current_time):
    global score, combo, hit_notes, message, message_display_time
    for note in notes[:]:  
        if note.is_hit(keys, 10):  # Perfect
            register_hit(note, 500, "Perfect!")
        elif note.is_hit(keys, 20):  # Good
            register_hit(note, 300, "Good!")
        elif note.is_hit(keys, 30):  # Bad
            register_hit(note, 100, "Bad!")

def register_hit(note, points, hit_message):
    global score, combo, hit_notes, message, message_display_time
    score += points
    combo += 1
    hit_notes += 1
    notes.remove(note)
    message = hit_message
    message_display_time = time.time()

def display_accuracy():
    if total_notes > 0:
        accuracy = (hit_notes / total_notes) * 100
    else:
        accuracy = 0
    font = pygame.font.Font(None, 36)
    accuracy_text = font.render(f"Accuracy: {accuracy:.2f}%", True, WHITE)
    screen.blit(accuracy_text, (10, 90))

def draw_notes(current_time):
    global combo, missed_notes
    for note in notes[:]:
        note.update_position(current_time)
        note.draw()
        if note.y_position > HEIGHT and not note.hit:
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
    load_notes("Notes/SONG1.txt")
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
        display_accuracy()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
