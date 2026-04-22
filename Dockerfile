FROM debian:trixie-slim
ENV DEBIAN_FRONTEND=noninteractive

# Install system-level camera drivers and OpenCV
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    libcamera-dev \
    gstreamer1.0-libcamera \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-tools \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Flask (OpenCV is already handled by the system)
RUN pip3 install --break-system-packages --no-cache-dir flask

EXPOSE 5001
CMD ["python3", "app.py"]
