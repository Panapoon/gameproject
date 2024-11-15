import librosa
import numpy as np

def analyze_song(song_index):
    # สร้าง path ของเพลงที่ต้องการโหลด
    song_path = f"songs/SONG{song_index}.mp3"
    
    # โหลดไฟล์เพลงใหม่ทุกครั้ง
    y, sr = librosa.load(song_path)

    # คำนวณการตีกลอง (beat frames) และเวลา
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # คำนวณ RMS energy ในแต่ละ window
    hop_length = 512
    frame_length = 2048
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

    # กำหนดเกณฑ์ RMS สำหรับการตรวจจับโน้ตยาว
    rms_threshold = np.percentile(rms, 75)

    # ใช้โหมด 'w' เพื่อเขียนทับไฟล์ที่มีอยู่แล้ว
    with open("Notes/song_note.txt", "w") as f:        
        # คำนวณโน้ตจาก beats
        for i in range(len(beat_times) - 1):
            start_time, end_time = beat_times[i], beat_times[i + 1]
            lane = (int(start_time * 1000) % 4)

            # คำนวณ frame indices ของ beat ปัจจุบันและถัดไป
            start_frame = librosa.time_to_frames(start_time, sr=sr, hop_length=hop_length)
            end_frame = librosa.time_to_frames(end_time, sr=sr, hop_length=hop_length)

            # คำนวณ RMS energy ระหว่าง beats
            beat_energy = np.mean(rms[start_frame:end_frame])

            # บันทึกโน้ต (ถ้า energy สูงเป็นโน้ตยาว)
            if beat_energy >= rms_threshold:
                f.write(f"{lane},{start_time},{end_time}\n")
            else:
                f.write(f"{lane},{start_time}\n")

        # จัดการกับโน้ตสุดท้าย
        if len(beat_times) > 0:
            lane = (int(beat_times[-1] * 1000) % 4)
            f.write(f"{lane},{beat_times[-1]}\n")