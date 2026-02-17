import cv2
import numpy as np

def create_dummy_video(filename='static/feed.mp4', duration=5, fps=30):
    height, width = 480, 640
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    for i in range(duration * fps):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Create a moving circle
        x = int(width/2 + 100 * np.sin(2 * np.pi * i / (duration * fps)))
        y = int(height/2 + 100 * np.cos(2 * np.pi * i / (duration * fps)))
        cv2.circle(frame, (x, y), 50, (0, 255, 0), -1)
        
        # Add text
        cv2.putText(frame, f"Frame: {i}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)

    out.release()
    print(f"Video saved to {filename}")

if __name__ == "__main__":
    create_dummy_video()
