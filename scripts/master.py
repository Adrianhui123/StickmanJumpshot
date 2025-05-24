import os
import subprocess
import shutil
from VideoDuration import get_video_duration

# === User Input ===
player = input("Enter player name (e.g., curry_gym): ").strip()
url = input("Enter YouTube video URL: ").strip()

# === Config ===
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
GIF_DIR = f"frontend/public/gifs/{player}"
FULL_VIDEO = os.path.join(RAW_DIR, f"{player}_full.mp4")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(GIF_DIR, exist_ok=True)

# === Step 1: Download YouTube Video ===
print(f"\n🔽 Downloading video as {FULL_VIDEO}")
subprocess.run(["yt-dlp", "-o", FULL_VIDEO, url])

# === Step 2: Extract Clips ===
video_duration = get_video_duration(FULL_VIDEO)
num_shots = int(input("Enter number of jumpshots taken in the video: ").strip())

print(f"\n✂️ Running extract_shots.py for {player}")
subprocess.run(["python3", "extract_shots.py", player, str(video_duration), str(num_shots)])


# === Step 3: Run Pose Estimation ===
print(f"\n🧍 Running make_pose_stickfigures.py for {player}")
subprocess.run(["python3", "make_pose_stickfigures.py", player])

# === Step 4: Generate GIFs + Cleanups ===
print(f"\n🌀 Running make_gifs.py for {player}")
subprocess.run(["python3", "make_gif.py", player])

print(f"\n✅ Done! GIFs ready in: {GIF_DIR}")

subprocess.run(["python3", "giftomp4.py"])
