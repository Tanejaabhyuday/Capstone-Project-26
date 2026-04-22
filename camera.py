import cv2

class Camera(object):
    def __init__(self):
        # The GStreamer pipeline is the 'translator' for the REES52 sensor
        pipeline = (
            "libcamerasrc ! "
            "video/x-raw, width=640, height=480, framerate=30/1 ! "
            "videoconvert ! "
            "video/x-raw, format=BGR ! "
            "appsink drop=true"
        )
        self.video = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not self.video.isOpened():
            # Fallback to standard V4L2 if GStreamer isn't initialized
            self.video = cv2.VideoCapture(0, cv2.CAP_V4L2)

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        
        # Flip 180 degrees (corrects for upside-down mounting)
        image = cv2.flip(image, -1) 
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def __del__(self):
        if hasattr(self, 'video') and self.video.isOpened():
            self.video.release()
