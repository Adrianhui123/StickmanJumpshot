# StickmanJumpshot

**StickmanJumpshot** is an interactive web-based game that challenges users to identify NBA players based solely on stick-figure animations of their jump shot. The game uses pose estimation and joint angle overlays to visualize player movement, gradually revealing the original video as the user interacts.

## Overview

- Leverages MediaPipe for frame-level full-body pose detection
- Converts trimmed basketball clips into animated skeletal motion sequences
- Annotates each frame with joint angles (elbows, knees) using NumPy vector math
- Synchronizes stick-figure overlays with real footage using fixed 15 FPS
- Users guess player names, progressing through controlled reveal stages

## Features

### Pose-Based Guessing Game

Simplifies each player's jump shot into a skeletal figure. Players must identify the shooter based on pose and motion style.

### Biomechanical Angle Overlays

Displays real-time joint angle measurements on right/left elbows and knees for each frame, aiding in movement analysis and differentiation.

### Controlled Reveal Mechanism

Users can gradually reveal the underlying video clip from bottom to top using interactive buttons. The overlay and original video are synchronized.

### Multi-Player Dataset

Supports over 50 NBA players with extensible support for future additions.

## Technologies Used

### Frontend

- React
- HTML5 video with `clip-path` masking
- Custom CSS animations for reveal logic

### Backend and Pose Pipeline (Python)

- OpenCV: Video frame extraction and image I/O
- MediaPipe: Human pose landmark estimation
- NumPy: Vector math and joint angle calculation
- ffmpeg: Video trimming and conversion
- imageio: GIF generation from annotated frames
- JSON: Metadata export for angle overlays

## Project Directory Structure

```plaintext
StickmanJumpshot/
├── data/
│   ├── raw/                    # Input full and trimmed video clips
│   └── processed/              # Frame-wise pose data and stick figures
├── frontend/
│   └── react-app/
│       ├── public/
│       │   ├── gifs/           # Generated animated stickman clips
│       │   ├── raw_clips/      # Trimmed source footage
│       │   └── angles/         # Angle values per frame in JSON format
├── scripts/
│   ├── extract_shots.py        # Splits full videos into uniform clips
│   ├── make_pose_stickfigures.py
│   ├── make_gifs.py
│   └── convert_gifs_to_mp4.py
└── README.md
