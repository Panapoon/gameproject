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
