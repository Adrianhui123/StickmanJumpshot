import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mediapipe as mp
import imageio
import sys
from make_gif import cleanup_after_gif_generation


# === Config ===
PROCESSED_DIR = "data/processed"
GIF_DIR = "frontend/react-app/public/gifs_3d"
os.makedirs(GIF_DIR, exist_ok=True)

# === CLI input ===
if len(sys.argv) < 2:
    print("Usage: python render_pose_3d.py <player_name>")
    sys.exit(1)

player = sys.argv[1]

# === Setup Pose Estimation ===
POSE_CONNECTIONS = [
    (11, 13), (13, 15),  # Left arm
    (12, 14), (14, 16),  # Right arm
    (11, 12),            # Shoulders
    (23, 24),            # Hips
    (11, 23), (12, 24),  # Torso sides
    (23, 25), (25, 27),  # Left leg
    (24, 26), (26, 28),  # Right leg
]

mp_pose = mp.solutions.pose
pose_tracker = mp_pose.Pose(static_image_mode=True)

# === Helper: Render Single Frame ===
def render_3d_pose(xs, ys, zs, angle, out_path):
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs, ys, zs, c='blue', s=20)
    for i, j in POSE_CONNECTIONS:
        ax.plot([xs[i], xs[j]], [ys[i], ys[j]], [zs[i], zs[j]], c='gray')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(-0.5, 0.5)
    ax.view_init(elev=15, azim=angle)
    ax.axis('off')
    fig.tight_layout()
    plt.savefig(out_path)
    plt.close()

# === Main Processing Loop ===
frames = []
clip_folders = [f for f in sorted(os.listdir(PROCESSED_DIR)) if f.startswith(player)]
for clip_folder in clip_folders:
    clip_path = os.path.join(PROCESSED_DIR, clip_folder)
    for idx, file in enumerate(sorted(os.listdir(clip_path))):
        if not file.startswith("frame_") or not file.endswith(".png"):
            continue

        img_path = os.path.join(clip_path, file)
        img = cv2.imread(img_path)
        if img is None:
            continue

        results = pose_tracker.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            continue

        landmarks = results.pose_landmarks.landmark
        xs = [lm.x for lm in landmarks]
        ys = [lm.y for lm in landmarks]
        zs = [lm.z for lm in landmarks]

        tmp_path = f"/tmp/pose3d_{idx:03d}.png"
        render_3d_pose(xs, ys, zs, angle=idx * 5, out_path=tmp_path)
        frames.append(imageio.imread(tmp_path))

# === Save 3D GIF ===
output_gif = os.path.join(GIF_DIR, f"{player}_3d.gif")
imageio.mimsave(output_gif, frames, fps=10)
print(f"✅ Saved 3D GIF: {output_gif}")
cleanup_after_gif_generation(player)
