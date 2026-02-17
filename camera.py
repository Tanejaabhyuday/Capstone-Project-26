import cv2
import time

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('static/feed.mp4')
        if not self.video.isOpened():
            raise RuntimeError("Could not open video source")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        
        # If the video reaches the end, rewind to the start
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
            
        if success:
            # Encode frame as JPEG
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        else:
            # Fallback if video still fails (should not happen with loop)
            return None
