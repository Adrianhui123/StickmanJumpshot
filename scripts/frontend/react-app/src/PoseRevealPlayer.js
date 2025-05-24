import React, { useRef, useEffect, useState } from "react";
import "./RevealPlayer.css";

function PoseRevealPlayer({ player, clipNum = 1, steps = 10 }) {
  const [revealStep, setRevealStep] = useState(0);
  const videoRef = useRef(null);
  const overlayRef = useRef(null);

  const baseURL = process.env.PUBLIC_URL;
  const videoSrc = `${baseURL}/raw_clips/${player}/${player}_${clipNum}.mp4`;
  const overlaySrc = `${baseURL}/gifs/${player}/${player}_${clipNum}.mp4`;

  useEffect(() => {
    const video = videoRef.current;
    const overlay = overlayRef.current;
    if (!video || !overlay) return;

    const syncAndPlay = () => {
      if (video.readyState >= 2 && overlay.readyState >= 2) {
        video.currentTime = 0;
        overlay.currentTime = 0;

        Promise.all([video.play(), overlay.play()]).catch((err) => {
          console.error("Sync play failed:", err);
        });

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

  const increaseReveal = () => {
    setRevealStep((prev) => Math.min(prev + 1, steps));
  };

  const decreaseReveal = () => {
    setRevealStep((prev) => Math.max(prev - 1, 0));
  };

  const revealHeight = `${(revealStep / steps) * 100}%`;

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
          }}
        />
      </div>

      <div className="reveal-controls">
        <button onClick={decreaseReveal}>◀ Reveal Less</button>
        <button onClick={increaseReveal}>▶ Reveal More</button>
      </div>
    </div>
  );
}

export default PoseRevealPlayer;
