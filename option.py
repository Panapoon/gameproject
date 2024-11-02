"""
import pygame
เปลี่ยน volumn
เปลี่ยน note speed
เปลี่ยน key blind
วีทำ
"""
import pygame
import sys
import config

class Options:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = config.screen_size[config.load_settings()["screen_size"]]
        self.screen = self.game.screen
        self.BG = config.menuBG
        self.font = pygame.font.Font(config.FONT1, 60)

        self.left_button = config.Button("<<", 200, 300, 50, 50, config.BLACK, 0)
        self.right_button = config.Button(">>", 400, 300, 50, 50, config.BLACK, 0)
        self.apply_button = config.Button("APPLY", 350, 400, 50, 50, config.BLACK, 0)

    def show(self):
        popup_size = False

        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.BG, (0, 0))

            #ปุ่มปรับขนาดจอ
            font = pygame.font.Font(None, 30)
            OPTION_surface = font.render("OPTION", True, config.WHITE)
            OPTION_rect = OPTION_surface.get_rect(center=(self.WIDTH // 2, 50))
            self.screen.blit(OPTION_surface, OPTION_rect)

            self.songM_button = config.Button(config.screen_size[config.load_settings()["screen_size"]], 325, 300, 150, 150, self.WHITE, 175)
            # แสดงเมนูเลือกขนาดหน้าจอ
            for i, (name, (width, height)) in enumerate(config.screen_size.items()):
                text_surface = self.font.render(name, True, config.WHITE)
                text_rect = text_surface.get_rect(center=(self.WIDTH // 2, 100 + i * 50))
                self.screen.blit(text_surface, text_rect)

                # ตรวจสอบการคลิกเพื่อเปลี่ยนขนาดหน้าจอ
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if text_rect.collidepoint(mouse_pos):
                        self.change_resolution(name)
                        # บันทึกการตั้งค่า
                        config.save_settings({"screen_size": name})

            pygame.display.flip()