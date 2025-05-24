import os
import subprocess

# === User Input ===
player = input("Enter player name (e.g., curry_gym): ").strip()
url = input("Enter YouTube video URL: ").strip()

# === Config ===
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
FULL_VIDEO = os.path.join(RAW_DIR, f"{player}_full.mp4")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# === Step 1: Download YouTube Video ===
print(f"\n🔽 Downloading video as {FULL_VIDEO}")
subprocess.run(["yt-dlp", "-o", FULL_VIDEO, url])

# === Step 2: Extract 4-second Clips ===
print(f"\n✂️ Running extract_shots.py for {player}")
subprocess.run(["python3", "extract_shots.py", player, FULL_VIDEO])

# === Step 3: Run Pose Estimation ===
print(f"\n🧍 Running make_pose_stickfigures.py for {player}")
subprocess.run(["python3", "make_pose_stickfigures.py", player])

# === Step 4: Generate 3D Rotating Pose GIFs ===
print(f"\n🔁 Running render_pose_3d.py for {player}")
subprocess.run(["python3", "renderpose3d.py", player])

print(f"\n✅ 3D GIFs ready in: frontend/react-app/public/gifs_3d/{player}_3d.gif")
