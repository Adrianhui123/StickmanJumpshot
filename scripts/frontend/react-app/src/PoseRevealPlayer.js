import React, { useRef, useEffect, useState } from "react";
import "./RevealPlayer.css";

function PoseRevealPlayer({ playerList = ["Dame", "MPJ", "Kobe", "Ja", "Jokic", "Harden", "Murray"], steps = 10 }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [revealStep, setRevealStep] = useState(0);
  const [guess, setGuess] = useState("");
  const videoRef = useRef(null);
  const overlayRef = useRef(null);

  const player = playerList[currentIndex];
  const baseURL = process.env.PUBLIC_URL;
  const videoSrc = `${baseURL}/raw_clips/${player}/${player}_1.mp4`;
  const overlaySrc = `${baseURL}/gifs/${player}/${player}_1.mp4`;

  // Video sync
  useEffect(() => {
    const video = videoRef.current;
    const overlay = overlayRef.current;
    if (!video || !overlay) return;

    const syncAndPlay = () => {
      if (video.readyState >= 2 && overlay.readyState >= 2) {
        video.currentTime = 0;
        overlay.currentTime = 0;

        Promise.all([video.play(), overlay.play()]).catch((err) =>
          console.error("Sync play failed:", err)
        );

        const interval = setInterval(() => {
          if (Math.abs(video.currentTime - overlay.currentTime) > 0.1) {
            overlay.currentTime = video.currentTime;
          }
        }, 1000);

        return () => clearInterval(interval);
      } else {
        setTimeout(syncAndPlay, 50);
      }
    };

    syncAndPlay();
  }, [videoSrc, overlaySrc]);

  const increaseReveal = () => setRevealStep((prev) => Math.min(prev + 1, steps));
  const decreaseReveal = () => setRevealStep((prev) => Math.max(prev - 1, 0));

  const handleGuess = (e) => {
    if (e.key === "Enter") {
      if (guess.trim().toLowerCase() === player.toLowerCase()) {
        alert("✅ Correct! Moving to next player...");
        setTimeout(() => {
          const nextIndex = (currentIndex + 1) % playerList.length;
          setCurrentIndex(nextIndex);
          setRevealStep(0);
          setGuess("");
        }, 500);
      } else {
        alert("❌ Incorrect, try again.");
      }
    }
  };

  return (
    <div className="reveal-container">
      <div className="video-layer">
        <video
          ref={videoRef}
          src={overlaySrc}
          className="reveal-video"
          muted
          loop
          playsInline
        />
        <video
          ref={overlayRef}
          src={videoSrc}
          className="pose-overlay"
          muted
          loop
          playsInline
          style={{
            clipPath: `inset(${100 - (revealStep / steps) * 100}% 0% 0% 0%)`,
            transition: "clip-path 0.3s ease",
          }}
        />
      </div>

      <div className="reveal-controls">
        <button onClick={decreaseReveal}>◀ Reveal Less</button>
        <button onClick={increaseReveal}>▶ Reveal More</button>
      </div>

      <input
        type="text"
        placeholder="Guess the player..."
        value={guess}
        onChange={(e) => setGuess(e.target.value)}
        onKeyDown={handleGuess}
        className="guess-input"
      />
    </div>
  );
}

export default PoseRevealPlayer;
