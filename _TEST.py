import pygame

pygame.init()
pygame.display.set_caption("Rhythm Game")
#ขนาดหน้าจอ
screen_w = 1600
screen_h = 1800
screen = pygame.display.set_mode((screen_w, screen_h))

#ตั้งค่าสี
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
screen.fill(BLUE)

#ตั้งค่าข้อความ
sys_font_1 = pygame.font.SysFont('garamond',50)
title_text = sys_font_1.render('Rhythm Game',True,WHITE)
text_rect = title_text.get_rect()
text_rect.centerx = screen_w // 2 
text_rect.top = 80 
#ดึงฟอนด์
fonts = pygame.font.get_fonts()
for font in fonts:
    print(font)

#แสดงหน้าจอ
running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    screen.blit(title_text, text_rect)
    pygame.display.update()
pygame.quit()