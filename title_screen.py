"""
import pygame
ใส่พื้นหลังสวยๆ
แสดงชื่อเกม
ปุ่ม play-ไปยัง select_song.py
ปุ่ม option-ไปยัง option.py
ปุ่ม quit-ออกจากเกม
ที่มี title_screen.py เนื่องจากกูต้องการให้มันสามารถกด esc จากหน้า select_song กลับมายังหน้า title ได้
ปู๊นทำ
"""
import pygame
import sys
import config

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # กำหนดสีพื้นฐาน
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)


        # โหลดรูปภาพพื้นหลัง
        self.menuBG = pygame.image.load("picture/menuBG.png")
        self.menuBG = pygame.transform.scale(self.menuBG, (self.WIDTH, self.HEIGHT))
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 180)

        # สร้างปุ่ม
        self.play_button = config.Button("Play", 72, 960, 460, 600, 120, self.GREEN, 255)
        self.options_button = config.Button("Options", 72, 960, 640, 600, 120, self.BLUE, 255)
        self.exit_button = config.Button("Exit", 72, 960, 820, 600, 120, self.RED, 255)

    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menuBG, (0, 0))  # วาดพื้นหลัง
            mouse_pos = pygame.mouse.get_pos()  # ตำแหน่งของเมาส์

            # วาดปุ่ม
            self.play_button.draw(self.screen, mouse_pos)
            self.options_button.draw(self.screen, mouse_pos)
            self.exit_button.draw(self.screen, mouse_pos)

            # สร้างการเปลี่ยนสีแบบฟุ้งสำหรับข้อความ
            title_surface = self.font.render("Rhythm Game", True, (255, 20, 147))  # สีชมพู
            title_rect = title_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 4))

            # จำลองเอฟเฟกต์ฟุ้ง โดยการวาดข้อความซ้ำหลายๆ ครั้งในตำแหน่งที่เบี่ยงเบน
            for dx in range(-5, 6, 2):  # เคลื่อนที่ตำแหน่งเล็กน้อย
                for dy in range(-5, 6, 2):  # เคลื่อนที่ตำแหน่งเล็กน้อย
                    shadow_surface = title_surface.copy()
                    shadow_rect = title_rect.move(dx, dy)
                    shadow_surface.set_alpha(100)  # ความโปร่งแสงต่ำเพื่อสร้างเอฟเฟกต์เบลอ
                    self.screen.blit(shadow_surface, shadow_rect)

            # วาดข้อความหลัก
            self.screen.blit(title_surface, title_rect)

            # ตรวจสอบการคลิกปุ่ม
            mouse_click = pygame.mouse.get_pressed()

            if self.play_button.is_clicked(mouse_pos, mouse_click):
                return 'select_song'
            if self.options_button.is_clicked(mouse_pos, mouse_click):
                return 'option'
            if self.exit_button.is_clicked(mouse_pos, mouse_click):
                pygame.quit()
                sys.exit()

            pygame.display.flip()