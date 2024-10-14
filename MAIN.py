import pygame
import sys

# กำหนดขนาดหน้าจอ
WIDTH, HEIGHT = 800, 600

# เริ่มต้น Pygame
pygame.init()

# สร้างหน้าจอ
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Rhythm Game lnwza007')

# กำหนดสี
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ฟังก์ชันในการวาดปุ่ม
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

#โหลดรูปภาพ
menuBG = pygame.image.load("picture/menuBG.png")

# ฟังก์ชันสำหรับหน้าจอหลัก
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(menuBG, (0, 0))

        draw_button("Play", 300, 200, 200, 50, GREEN)
        draw_button("option", 300, 300, 200, 50, BLUE)
        draw_button("Exit", 300, 400, 200, 50, RED)

        font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)
        text_surface = font.render("Rhythm game", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(text_surface, text_rect)


        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if 300 <= mouse_pos[0] <= 500 and 200 <= mouse_pos[1] <= 250:
            if mouse_click[0]:
                game_loop() 
       
        if 300 <= mouse_pos[0] <= 500 and 300 <= mouse_pos[1] <= 350:
            if mouse_click[0]:
                option_loop() 

        if 300 <= mouse_pos[0] <= 500 and 400 <= mouse_pos[1] <= 450:
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# ฟังก์ชันสำหรับเกม
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(menuBG, (0, 0))

        # แสดงข้อความในเกม
        font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)
        text_surface = font.render("Press ENTER to start!!!", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

# ฟังก์ชันสำหรับoption
def option_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(RED)  # เปลี่ยนพื้นหลังเป็นสีน้ำเงิน

        # แสดงข้อความในเกม
        font = pygame.font.Font(sys_font_1, 74)
        text_surface = font.render("Option Running", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

# เริ่มต้นที่หน้าจอหลัก
main_menu()