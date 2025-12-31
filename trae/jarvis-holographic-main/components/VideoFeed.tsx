import React, { useEffect, useRef, useState } from 'react';
import { MediaPipeService } from '../services/mediapipeService';
import { HandTrackingState, HandInteractionData } from '../types';

interface VideoFeedProps {
  onTrackingUpdate: (state: HandTrackingState) => void;
}

const VideoFeed: React.FC<VideoFeedProps> = ({ onTrackingUpdate }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const requestRef = useRef<number | null>(null);
  const lastVideoTimeRef = useRef<number>(-1);
  const [status, setStatus] = useState<string>("Initializing Camera...");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    const startCamera = async () => {
      try {
        setStatus("Requesting Camera Access...");
        let stream;
        try {
            // Try HD first
            stream = await navigator.mediaDevices.getUserMedia({
              video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: "user"
              }
            });
        } catch (e) {
            console.warn("HD Camera failed, trying basic constraints...", e);
            // Fallback to any available video
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
        }

        if (videoRef.current && isMounted) {
          videoRef.current.srcObject = stream;
          
          // Robust video play handling
          try {
             await videoRef.current.play();
          } catch (e) {
             console.warn("Auto-play prevented, waiting for user interaction or metadata", e);
             setStatus("Waiting for Camera (Click page if stuck)...");
             await new Promise<void>((resolve) => {
                 if (!videoRef.current) return resolve();
                 videoRef.current.onloadeddata = () => {
                     videoRef.current?.play().then(() => resolve()).catch(() => resolve());
                 };
                 if (videoRef.current.readyState >= 2) resolve();
             });
          }
          
          console.log("Camera started, initializing tracking...");
          setStatus("Loading AI Models...");
          try {
            const recognizer = await MediaPipeService.initialize();
            setStatus("System Active - Tracking Hands");
            
            const renderLoop = () => {
              if (!isMounted) return;

              if (videoRef.current && 
                  videoRef.current.readyState >= 2 && 
                  !videoRef.current.paused) {
                
                // Set canvas size to match video
                if (canvasRef.current && videoRef.current.videoWidth > 0) {
                    canvasRef.current.width = videoRef.current.videoWidth;
                    canvasRef.current.height = videoRef.current.videoHeight;
                }

                if (videoRef.current.currentTime !== lastVideoTimeRef.current) {
                    lastVideoTimeRef.current = videoRef.current.currentTime;
                    
                    try {
                      const results = recognizer.recognizeForVideo(videoRef.current, Date.now());
                      
                      // Clear canvas
                      if (canvasRef.current) {
                          const ctx = canvasRef.current.getContext('2d');
                          if (ctx) {
                              ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
                          }
                      }

                      const newState: HandTrackingState = {
                        leftHand: null,
                        rightHand: null
                      };

                      if (results.landmarks) {
                        results.landmarks.forEach((landmarks, index) => {
                          const handednessCategory = results.handedness[index]?.[0];
                          const handedness = (handednessCategory?.categoryName || 'Right') as 'Left' | 'Right';
                          
                          // Draw landmarks & Interaction Feedback
                          if (canvasRef.current) {
                             const ctx = canvasRef.current.getContext('2d');
                             if (ctx) {
                                 const isLeft = handedness === 'Left';
                                 const color = isLeft ? '#00F0FF' : '#FF0055';
                                 
                                 // Draw points
                                 ctx.fillStyle = color;
                                 ctx.strokeStyle = '#FFFFFF';
                                 ctx.lineWidth = 2;
                                 
                                 // Draw skeleton
                                 ctx.beginPath();
                                 landmarks.forEach((p) => {
                                     const x = p.x * canvasRef.current!.width;
                                     const y = p.y * canvasRef.current!.height;
                                     ctx.moveTo(x, y);
                                     ctx.arc(x, y, 3, 0, 2 * Math.PI);
                                 });
                                 ctx.fill();
                                 
                                 // Interaction Cues
                                 const wrist = landmarks[0];
                                 const wx = wrist.x * canvasRef.current.width;
                                 const wy = wrist.y * canvasRef.current.height;

                                 ctx.font = "bold 20px monospace";
                                 ctx.fillStyle = "#FFFFFF";
                                 ctx.textAlign = "center";
                                 
                                 // Note: Text is mirrored due to CSS, so we need to reverse text drawing? 
                                 // Actually CSS flips the whole canvas, so text written normally will appear backwards.
                                 // We need to un-flip context for text or just accept it's AR style.
                                 // Let's try to draw text normally, user will see it mirrored. 
                                 // FIX: Save context, scale(-1, 1), draw text, restore.
                                 
                                 ctx.save();
                                 // Move to target position
                                 ctx.translate(wx, wy - 40);
                                 // Flip back to normal for text
                                 ctx.scale(-1, 1); 
                                 ctx.fillText(isLeft ? "ZOOM (PINCH)" : "ROTATE (MOVE)", 0, 0);
                                 ctx.restore();

                                 if (isLeft) {
                                     // Draw Pinch Line
                                     const t = landmarks[4];
                                     const i = landmarks[8];
                                     const tx = t.x * canvasRef.current.width;
                                     const ty = t.y * canvasRef.current.height;
                                     const ix = i.x * canvasRef.current.width;
                                     const iy = i.y * canvasRef.current.height;
                                     
                                     // Pinch Dist Calculation for Color
                                     const dist = Math.sqrt(Math.pow(t.x - i.x, 2) + Math.pow(t.y - i.y, 2));
                                     ctx.strokeStyle = dist < 0.05 ? '#00FF00' : '#FFFFFF';
                                     ctx.lineWidth = 4;
                                     ctx.beginPath();
                                     ctx.moveTo(tx, ty);
                                     ctx.lineTo(ix, iy);
                                     ctx.stroke();
                                 } else {
                                     // Draw Rotation Joystick
                                     const m = landmarks[9];
                                     const mx = m.x * canvasRef.current.width;
                                     const my = m.y * canvasRef.current.height;
                                     
                                     ctx.beginPath();
                                     ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
                                     ctx.lineWidth = 2;
                                     ctx.arc(canvasRef.current.width / 2, canvasRef.current.height / 2, 50, 0, 2 * Math.PI); // Center reference
                                     ctx.stroke();
                                     
                                     ctx.beginPath();
                                     ctx.moveTo(canvasRef.current.width / 2, canvasRef.current.height / 2);
                                     ctx.lineTo(mx, my);
                                     ctx.strokeStyle = '#FF0055';
                                     ctx.stroke();
                                 }
                             }
                          }

                          // Calculate Pinch (Thumb tip 4, Index tip 8)
                          const thumbTip = landmarks[4];
                          const indexTip = landmarks[8];
                          const pinchDist = Math.sqrt(
                            Math.pow(thumbTip.x - indexTip.x, 2) + 
                            Math.pow(thumbTip.y - indexTip.y, 2)
                          );
                          const isPinching = pinchDist < 0.05;

                          let expansionFactor = 0;
                          let rotationControl = { x: 0, y: 0 };

                          if (handedness === 'Left') {
                              // Left Hand: Expansion/Zoom Control
                              const minPinch = 0.02;
                              const maxPinch = 0.18;
                              const normalized = (pinchDist - minPinch) / (maxPinch - minPinch);
                              expansionFactor = Math.max(0, Math.min(1, normalized));
                          } else {
                              // Right Hand: 2D Rotation Control (Joystick style)
                              // Hand Center (Middle finger MCP index 9)
                              const handX = landmarks[9].x; 
                              const handY = landmarks[9].y;
                              
                              // X Axis: Left (-1) to Right (1) -> Controls Spin (Yaw)
                              const rotX = (handX - 0.5) * 2; 
                              
                              // Y Axis: Top (-1) to Bottom (1) -> Controls Tilt (Pitch)
                              // Note: In video coords, Y=0 is top.
                              const rotY = (handY - 0.5) * 2;
                              
                              rotationControl = { x: rotX, y: rotY };
                          }

                          const handData: HandInteractionData = {
                              isPinching,
                              pinchDistance: pinchDist,
                              position: { x: landmarks[9].x, y: landmarks[9].y, z: landmarks[9].z },
                              expansionFactor,
                              rotationControl
                          };

                          if (handedness === 'Left') {
                              newState.leftHand = handData;
                          } else {
                              newState.rightHand = handData;
                          }
                        });
                      }

                      onTrackingUpdate(newState);
                    } catch (e) {
                      console.error("Tracking Loop Error:", e);
                    }
                }
              }
              
              requestRef.current = requestAnimationFrame(renderLoop);
            };

            renderLoop();
          } catch (err: any) {
             console.error("MediaPipe Init Error:", err);
             setStatus(`AI Init Failed: ${err.message || err}`);
             setError(err.message || JSON.stringify(err));
          }
        }
      } catch (err: any) {
        console.error("Error accessing camera:", err);
        setStatus(`Camera Error: ${err.message}`);
        setError("Camera Access Denied or Unavailable");
      }
    };

    startCamera();

    return () => {
      isMounted = false;
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [onTrackingUpdate]);

  return (
    <>
      <div className="absolute inset-0 w-full h-full pointer-events-none" style={{ transform: 'scaleX(-1)' }}>
          <video
            ref={videoRef}
            className="absolute inset-0 w-full h-full object-cover opacity-60"
            playsInline
            muted
          />
          <canvas
            ref={canvasRef}
            className="absolute inset-0 w-full h-full object-cover opacity-80"
          />
      </div>
      
      {/* Debug Status Overlay - Not Mirrored */}
      <div className="absolute top-0 left-0 p-2 bg-black/80 text-green-400 font-mono text-xs z-50 pointer-events-none">
        <div>STATUS: {status}</div>
        {error && <div className="text-red-500">ERROR: {error}</div>}
      </div>

      {/* Instructions Overlay - Centered Bottom */}
      <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 bg-black/60 p-4 rounded-xl border border-cyan-500/50 text-cyan-400 font-mono text-sm pointer-events-none text-center">
          <div className="font-bold mb-2">GESTURE CONTROLS</div>
          <div className="grid grid-cols-2 gap-8">
              <div>
                  <div className="text-white font-bold">🖐 LEFT HAND</div>
                  <div>Pinch Thumb & Index</div>
                  <div className="text-xs text-gray-400">Controls Zoom / Expansion</div>
              </div>
              <div>
                  <div className="text-white font-bold">✋ RIGHT HAND</div>
                  <div>Move Hand in Air</div>
                  <div className="text-xs text-gray-400">Controls Rotation (Joystick)</div>
              </div>
          </div>
      </div>
    </>
  );
};

export default VideoFeed;
