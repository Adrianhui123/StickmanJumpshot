import cv2
import os

def create_silhouettes(frame_dir):
    for file in os.listdir(frame_dir):
        if file.endswith(".png") and not file.startswith("silhouette_"):
            path = os.path.join(frame_dir, file)
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, silhouette = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            out_path = os.path.join(frame_dir, f"silhouette_{file}")
            cv2.imwrite(out_path, silhouette)

# Optional: run directly
if __name__ == "__main__":
    create_silhouettes("../data/processed/curry_1")
