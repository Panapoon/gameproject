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

class Button:
    def __init__(self, text, x, y, width, height, color, border_radius=15):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_radius = border_radius
        self.hover_color = self._adjust_color(color, -50)  # สร้างสีจางลง

    def _adjust_color(self, color, amount):
        """ ลดความสว่างของสี """
        return (
            max(0, min(255, color[0] + amount)),
            max(0, min(255, color[1] + amount)),
            max(0, min(255, color[2] + amount))
        )

    def draw(self, screen, mouse_pos):
        # วาดสี่เหลี่ยมมน
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        
        # วาดข้อความลงบนปุ่ม
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]

class Menu:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = self.game.WIDTH, self.game.HEIGHT
        self.screen = self.game.screen

        # กำหนดสี
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # โหลดรูปภาพ
        self.menuBG = pygame.image.load("picture/menuBG.png")
        self.font = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60)

        # สร้างปุ่ม
        self.play_button = Button("Play", 300, 200, 200, 50, self.GREEN)
        self.options_button = Button("Options", 300, 300, 200, 50, self.BLUE)
        self.exit_button = Button("Exit", 300, 400, 200, 50, self.RED)

    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menuBG, (0, 0))
            mouse_pos = pygame.mouse.get_pos()  # รับตำแหน่งของเมาส์
            self.play_button.draw(self.screen, mouse_pos)
            self.options_button.draw(self.screen, mouse_pos)
            self.exit_button.draw(self.screen, mouse_pos)

            title_surface = self.font.render("Rhythm Game", True, self.WHITE)
            title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 100))
            self.screen.blit(title_surface, title_rect)

            mouse_click = pygame.mouse.get_pressed()

            if self.play_button.is_clicked(mouse_pos, mouse_click):
                self.game.game_loop()
            if self.options_button.is_clicked(mouse_pos, mouse_click):
                self.game.option_loop()
            if self.exit_button.is_clicked(mouse_pos, mouse_click):
                pygame.quit()
                sys.exit()

            pygame.display.flip()

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Rhythm Game lnwza007')
        self.menu = Menu(self)

        # ปุ่มกลับ
        self.back_button = Button("Back", 300, 500, 200, 50, (255, 165, 0))

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))  # ล้างหน้าจอ
            text_surface = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 60).render("Press ENTER to start!!!", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)

            # วาดปุ่มกลับ
            self.back_button.draw(self.screen, pygame.mouse.get_pos())

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return  # กลับไปยังเมนูหลัก

            pygame.display.flip()

    def option_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 0, 0))  # เปลี่ยนพื้นหลังเป็นสีแดง
            option_surface = pygame.font.Font("Font/Ldfcomicsans-jj7l.ttf", 74).render("Option Running", True, (255, 255, 255))
            option_rect = option_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(option_surface, option_rect)

            # วาดปุ่มกลับ
            self.back_button.draw(self.screen, pygame.mouse.get_pos())

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return  # กลับไปยังเมนูหลัก

            pygame.display.flip()

# เริ่มต้นเกม
if __name__ == "__main__":
    game_instance = Game()
    game_instance.menu.main_menu()