import os
import subprocess

GIF_DIR = "frontend/react-app/public/gifs/"

def convert_gif_to_mp4(gif_path, mp4_path):
    cmd = [
        "ffmpeg", "-y",
        "-r", "15",
        "-i", gif_path,
        "-movflags", "faststart",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        mp4_path
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    for player_folder in os.listdir(GIF_DIR):
        player_path = os.path.join(GIF_DIR, player_folder)
        if os.path.isdir(player_path):
            for gif_file in os.listdir(player_path):
                if gif_file.endswith(".gif"):
                    gif_path = os.path.join(player_path, gif_file)
                    mp4_path = gif_path.replace(".gif", ".mp4")
                    print(f"🎬 Converting {gif_path} → {mp4_path}")
                    convert_gif_to_mp4(gif_path, mp4_path)
                    print(f"✅ Converted {gif_file}")
