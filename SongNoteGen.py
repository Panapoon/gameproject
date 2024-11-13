import librosa
import numpy as np

# Load the audio file
y, sr = librosa.load("songs/SONG4.mp3")

# Get the beat frames and corresponding times
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Calculate RMS energy over short windows
hop_length = 512
frame_length = 2048
rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

# Define RMS threshold for detecting long notes based on sustained energy
rms_threshold = np.percentile(rms, 75)  # Using the 75th percentile as an example threshold

# Save notes to a text file
with open("SONG4.txt", "w") as f:
    for i in range(len(beat_times) - 1):
        # Calculate the lane number based on beat time (modulo 4 for lane selection)
        lane = (int(beat_times[i] * 1000) % 4)

        # Get the frame indices for the current and next beat
        start_frame = librosa.time_to_frames(beat_times[i], sr=sr, hop_length=hop_length)
        end_frame = librosa.time_to_frames(beat_times[i + 1], sr=sr, hop_length=hop_length)
        
        # Calculate the RMS energy between the two beats
        beat_energy = np.mean(rms[start_frame:end_frame])  # RMS between beats

        # If energy is high and sustained, mark as long note
        if beat_energy >= rms_threshold:
            f.write(f"{lane},{beat_times[i]},{beat_times[i + 1]}\n")  # long note with start and end times
        else:
            f.write(f"{lane},{beat_times[i]}\n")  # normal note with start time only

    # Last note handling
    if len(beat_times) > 0:
        lane = (int(beat_times[-1] * 1000) % 4)
        f.write(f"{lane},{beat_times[-1]}\n")
