import librosa

# Load the audio file
y, sr = librosa.load("songs/SONG4.mp3")

# Get the beat times (in seconds)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Save the beats to a text file
with open("SONG4.txt", "w") as f:
    for beat in beat_times:
        lane = (int(beat * 1000) % 4)  # Assign a lane based on time
        f.write(f"{lane},{beat}\n")
