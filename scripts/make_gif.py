import os
import sys
import imageio
import shutil

PROCESSED_DIR = "data/processed"
RAW_DIR = "data/raw"
GIF_DIR = "frontend/react-app/public/gifs/"
Raw_Clip_DIR = "frontend/react-app/public/raw_clips/"

if len(sys.argv) < 2:
    print("Usage: python make_gifs.py <player_name>")
    sys.exit(1)

player_name = sys.argv[1]
os.makedirs(GIF_DIR, exist_ok=True)


def make_gif(input_dir, output_path, fps=15):
    frames = []
    for file in sorted(os.listdir(input_dir)):
        if file.startswith("pose_frame_") and file.endswith(".png"):
            img = imageio.imread(os.path.join(input_dir, file))
            frames.append(img)
    if frames:
        imageio.mimsave(output_path, frames, fps=fps, loop=0)
        print(f"[GIF] Saved {output_path}")
    else:
        print(f"[SKIP] No pose frames found in {input_dir}")

def cleanup_after_gif_generation(player_name):
    print(f"\n🧹 Cleaning up intermediate files for {player_name}")

    # Keep raw clips but move them to raw_clips/<player>
    player_clip_dir = os.path.join("frontend/react-app/public/raw_clips", player_name)
    os.makedirs(player_clip_dir, exist_ok=True)

    for f in os.listdir(RAW_DIR):
        if f.endswith(".mp4") and f.startswith(player_name) and "full" not in f:
            src = os.path.join(RAW_DIR, f)
            dst = os.path.join(player_clip_dir, f)
            shutil.move(src, dst)
            print(f"  📦 Moved raw clip: {f} → {player_clip_dir}")

    # Delete processed frame folders
    for folder in os.listdir(PROCESSED_DIR):
        if folder.startswith(player_name):
            path = os.path.join(PROCESSED_DIR, folder)
            if os.path.isdir(path):
                shutil.rmtree(path)
                print(f"  🗑️ Deleted processed folder: {folder}")

    # Move generated GIFs into gifs/<player>/
    player_gif_dir = os.path.join(GIF_DIR, player_name)
    os.makedirs(player_gif_dir, exist_ok=True)

    for f in os.listdir(GIF_DIR):
        if f.endswith(".gif") and f.startswith(player_name):
            src = os.path.join(GIF_DIR, f)
            dst = os.path.join(player_gif_dir, f)
            shutil.move(src, dst)
            print(f"  📦 Moved GIF: {f} → {player_gif_dir}")


if __name__ == "__main__":
    # === Main Script ===xwxqx
    for folder in sorted(os.listdir(PROCESSED_DIR)):
        if folder.startswith(player_name):
            input_dir = os.path.join(PROCESSED_DIR, folder)
            output_path = os.path.join(GIF_DIR, f"{folder}.gif")
            make_gif(input_dir, output_path)

    cleanup_after_gif_generation(player_name)
