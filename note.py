"""
defind โหลดโน๊ตจากไฟล์ .txt 
defind อ่าน score จากโน๊ต
สร้างไฟล์นี้มาเพื่อจัดให้เป็นระเบียบเฉยๆไม่มีไร
ปู๊นทำ
"""
import pygame
import time
from pygame import mixer
import config
from select_song import *
from option import *

class Note:
        def __init__(self, lane, spawn_time, duration=None):
            self.lane= lane
            self.spawn_time = spawn_time
            self.duration = duration

        def update_position(self, current_time):
            self.elapsed = current_time - self.spawn_time
            self.y_position = self.elapsed * self.note_speed
        
        def draw(self):
            if self.y_position <= self.HEIGHT:
                pygame.draw.circle(self.screen, self.note_color, (self.lane * self.lane_width + self.lane_width // 2, int(self.y_position)), 30)

        def is_hit(self, keys, offset_tolerance):
            """เช็คว่าโน้ตถูกตีหรือไม่ โดยพิจารณาจากการกดปุ่มและระยะเบี่ยงเบนจากเส้น HIT_LINE_Y"""
            if self.hit:
                return False
            offset = abs(self.y_position - self.hit_lane_y)
            key_mapping = [pygame.K_a, pygame.K_s, pygame.K_j, pygame.K_k]
            
            # เพิ่มระยะเบี่ยงเบนในการตีให้กว้างขึ้น
            tolerance_increase = 10  # เพิ่ม ระยะเบี่ยงเบนอีก 10
            if keys[key_mapping[self.lane]] and offset < (offset_tolerance + tolerance_increase):
                self.hit = True
                return True
            return False