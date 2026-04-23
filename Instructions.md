### **Startup Instructions for Raspberry Pi**


#### **1. Neutralize Resource Hijacking**
Modern Raspberry Pi OS uses background services that may lock the camera hardware. Run these commands to ensure the REES52 sensor is available for the Docker container:

```bash
# Stop background media services that may hold a lock on /dev/video0
systemctl --user stop pipewire.socket wireplumber.socket
systemctl --user stop pipewire wireplumber
sudo killall -9 pipewire wireplumber

# Verify the camera node is free (this should return no output)
sudo fuser /dev/video0
```

#### **2. Launch the Forensic Container**
Navigate to your project directory and execute the container with high-privilege hardware access:

```bash
cd ~/Desktop/Capstone-Project-26

sudo docker run -d \
  --name smart-camera-live \
  --privileged \
  --net host \
  --device /dev/video0:/dev/video0 \
  --device /dev/vchiq:/dev/vchiq \
  --device /dev/media0:/dev/media0 \
  -v /run/udev:/run/udev:ro \
  -v $(pwd)/forensics:/app/forensics \
  smart-camera
```

#### **3. Optional: Persistent Auto-Start**
For a permanent deployment (e.g., a capstone demonstration), configure Docker to restart the container automatically upon system boot:

```bash
# Add the --restart flag to the run command
sudo docker run -d --restart always --name smart-camera-live ...
```

---

### **Troubleshooting and Verification**
* **IP Verification**: If the site is unreachable, verify the Pi's IP address (especially if using a mobile hotspot). Run `hostname -I` to confirm.
* **Hardware Check**: If the feed is black, ensure the CSI ribbon cable is securely seated.
* **Log Integrity**: Verify forensic logging is active by checking the local audit trail:
    ```bash
    tail -f forensics/access_control.log
    ```

### **Forensic Rationale**
This startup procedure is designed for **System Persistence and Recovery**. By neutralizing the host OS multimedia framework before container instantiation, we prevent hardware resource hijacking and ensure a consistent GStreamer hardware pipeline for forensic data acquisition.
