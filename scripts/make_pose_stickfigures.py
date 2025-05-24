
import cv2
import os
import mediapipe as mp
import numpy as np
import sys
import json
from collections import defaultdict

# === Config ===
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
ANGLE_EXPORT_DIR = "frontend/react-app/public/angles/"
os.makedirs(ANGLE_EXPORT_DIR, exist_ok=True)

if len(sys.argv) < 2:
    print("Usage: python make_pose_stickfigures.py <player_name>")
    sys.exit(1)

player = sys.argv[1]

# === MediaPipe Setup ===
mp_pose = mp.solutions.pose
pose_tracker = mp_pose.Pose(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

# === Angle Helper ===
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# === Extract Frames ===
def extract_frames(video_path, out_dir, fps=15):
    if not os.path.exists(video_path):
        print(f"[ERROR] File not found: {video_path}")
        return

    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Could not open video: {video_path}")
        return

    fps_actual = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps_actual if fps_actual > 0 else 0

    if fps_actual == 0 or duration == 0:
        print(f"[ERROR] Invalid FPS or duration in {video_path}")
        return

    max_frames = int(duration * fps)
    interval = int(fps_actual // fps) if fps_actual >= fps else 1

    print(f"[INFO] Extracting ~{max_frames} frames over {duration:.2f}s at {fps} FPS")

    i = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret or saved >= max_frames:
            break
        if i % interval == 0:
            out_path = os.path.join(out_dir, f"frame_{saved:03d}.png")
            if cv2.imwrite(out_path, frame):
                print(f"[FRAME] Saved {out_path}")
                saved += 1
        i += 1

    cap.release()

# === Draw Pose ===
def draw_pose_on_frame(image):
    results = pose_tracker.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None, None

    lm = results.pose_landmarks.landmark
    h, w = image.shape[:2]
    points = [(int(lm[i].x * w), int(lm[i].y * h)) for i in range(len(lm))]

    # Create white canvas
    canvas = 255 * np.ones_like(image)

    # Draw bones
    POSE_CONNECTIONS = [
        (11, 13), (13, 15), (12, 14), (14, 16),
        (11, 12), (23, 24), (11, 23), (12, 24),
        (23, 25), (25, 27), (24, 26), (26, 28)
    ]
    for start, end in POSE_CONNECTIONS:
        if start < len(points) and end < len(points):
            cv2.line(canvas, points[start], points[end], (50, 50, 50), thickness=4)

    # Draw joints
    for (x, y) in points:
        cv2.circle(canvas, (x, y), 6, (255, 0, 0), -1)

    # Overlay angles
    if len(points) > 28:
        def safe_angle(a, b, c):
            return calculate_angle(points[a], points[b], points[c])

        right_elbow_angle = safe_angle(12, 14, 16)
        left_elbow_angle = safe_angle(11, 13, 15)
        right_knee_angle = safe_angle(24, 26, 28)
        left_knee_angle = safe_angle(23, 25, 27)

        cv2.putText(canvas, f"{right_elbow_angle:.1f}", (points[14][0]+10, points[14][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(canvas, f"{left_elbow_angle:.1f}", (points[13][0]+10, points[13][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(canvas, f"{right_knee_angle:.1f}", (points[26][0]+10, points[26][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(canvas, f"{left_knee_angle:.1f}", (points[25][0]+10, points[25][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return canvas, points

# === Process Pose Frames ===
def process_pose_frames(frame_dir):
    angle_series = defaultdict(list)

    for file in sorted(os.listdir(frame_dir)):
        if file.startswith("frame_") and file.endswith(".png"):
            path = os.path.join(frame_dir, file)
            img = cv2.imread(path)
            if img is None:
                print(f"[SKIP] Could not read {file}")
                continue

            pose_img, points = draw_pose_on_frame(img)
            if pose_img is not None:
                out_path = os.path.join(frame_dir, f"pose_{file}")
                cv2.imwrite(out_path, pose_img)
                print(f"[POSE] Saved {out_path}")

                if points and len(points) > 28:
                    angle_series["right_elbow"].append(calculate_angle(points[12], points[14], points[16]))
                    angle_series["left_elbow"].append(calculate_angle(points[11], points[13], points[15]))
                    angle_series["right_knee"].append(calculate_angle(points[24], points[26], points[28]))
                    angle_series["left_knee"].append(calculate_angle(points[23], points[25], points[27]))
            else:
                print(f"[SKIP] No pose detected in {file}")

    out_json = os.path.join(frame_dir, "angles.json")
    with open(out_json, "w") as f:
        json.dump(angle_series, f)
    print(f"[📈] Saved angle data to {out_json}")

# === Main Processing ===
for file in sorted(os.listdir(RAW_DIR)):
    if file.startswith(player) and file.endswith(".mp4") and not file.endswith("_full.mp4"):
        clip_name = os.path.splitext(file)[0]
        video_path = os.path.join(RAW_DIR, file)
        out_dir = os.path.join(PROCESSED_DIR, clip_name)

        print(f"🎬 Processing {clip_name}")
        extract_frames(video_path, out_dir, fps=15)
        process_pose_frames(out_dir)
        print(f"[DONE] Processed {clip_name}")

combined_angles = defaultdict(list)
for folder in sorted(os.listdir(PROCESSED_DIR)):
    if folder.startswith(player):
        angle_file = os.path.join(PROCESSED_DIR, folder, "angles.json")
        if os.path.exists(angle_file):
            with open(angle_file, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    combined_angles[k].extend(v)

final_path = os.path.join(ANGLE_EXPORT_DIR, f"{player}_angles.json")
with open(final_path, "w") as f:
    json.dump(combined_angles, f, indent=2)

print(f"✅ Combined angle data saved to {final_path}")
