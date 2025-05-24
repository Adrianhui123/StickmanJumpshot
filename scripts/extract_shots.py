import os
import sys
import subprocess

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/raw"

if len(sys.argv) < 4:
    print("Usage: python extract_shots.py <player_name> <video_duration_sec> <num_shots>")
    sys.exit(1)

player = sys.argv[1]
duration_sec = float(sys.argv[2])
num_shots = int(sys.argv[3])

full_video_path = os.path.join(RAW_DIR, f"{player}_full.mp4")

if not os.path.exists(full_video_path):
    print(f"[ERROR] File not found: {full_video_path}")
    sys.exit(1)

print(f"[INFO] Trimming clips from: {full_video_path}")

duration_per_shot = duration_sec / num_shots

for i in range(num_shots):
    start_sec = i * duration_per_shot
    out_name = f"{player}_{i+1}.mp4"
    out_path = os.path.join(PROCESSED_DIR, out_name)

    print(f"✂️ Trimming clip {i+1}: start={start_sec:.2f}s → {out_name}")

    result = subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-t", str(duration_per_shot),
        "-i", full_video_path,
        out_path,
        "-loglevel", "error"
    ])

    if result.returncode != 0:
        print(f"[ERROR] Failed to trim {out_name}")
    else:
        print(f"[SAVED] {out_path}")
