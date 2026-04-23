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





### **Maintenance: Removing and Rebuilding**

If you need to update the application code or reset the environment, follow these steps to ensure a clean rebuild without any cached "ghost" data.

#### **1. Stop and Remove Existing Containers**
Docker preserves the state of stopped containers. To reuse the name `smart-camera-live`, you must explicitly remove the old instance.
```bash
# Stop the running container
sudo docker stop smart-camera-live

# Remove the container record from the system
sudo docker rm smart-camera-live
```

#### **2. Force a Fresh Image Build**
Use the `--no-cache` flag to ensure Docker reads your latest file changes (like edits to `camera.py`) instead of using a saved version from its memory.
```bash
# Rebuild the image from scratch
sudo docker build --no-cache -t smart-camera .
```

#### **3. Clean the Host Hardware State**
If the camera fails to initialize after a restart, ensure the host OS has not reclaimed the sensor.
```bash
# Neutralize Pipewire middlemen
systemctl --user stop pipewire.socket wireplumber.socket
systemctl --user stop pipewire wireplumber
sudo killall -9 pipewire wireplumber
```

#### **4. Standard Deployment Command**
Once the environment is clean, launch the container with the required hardware passthrough flags.
```bash
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

### **The "One-Line" Reset (For Speed)**
You can combine these into a single command string to reset everything in seconds:
```bash
sudo docker stop smart-camera-live && sudo docker rm smart-camera-live && sudo docker build --no-cache -t smart-camera . && sudo docker run -d --name smart-camera-live --privileged --net host --device /dev/video0:/dev/video0 --device /dev/vchiq:/dev/vchiq --device /dev/media0:/dev/media0 -v /run/udev:/run/udev:ro -v $(pwd)/forensics:/app/forensics smart-camera
```





```markdown
# Vulnerability Assessment & Forensic Interception Report

## 1. Overview
This document details the methodology for a Man-in-the-Middle (MitM) attack and credential sniffing performed against the Raspberry Pi Forensic Camera system. This assessment proves the risks of plaintext HTTP communication in an evidence-collection pipeline.

## 2. Laboratory Environment
* **Target (IoT Sensor):** Raspberry Pi 4/5 (IP: `192.168.2.5`)
* **Victim (Client):** MacBook Pro (Accessing camera via Web UI)
* **Attacker (Forensic Workstation):** MacBook Air/Pro (Running Interception Tools)

## 3. Technical Execution

### Phase A: Enabling IP Forwarding (macOS)
To prevent the Attacker node from dropping packets and causing a Denial of Service (DoS), IP forwarding must be enabled:
```bash
sudo sysctl -w net.inet.ip.forwarding=1
```

### Phase B: ARP Poisoning via CLI
During testing, the Ettercap GUI experienced a "Beachball" hang and `malloc` errors due to macOS interface abstraction. To ensure stability, the attack was executed via the Command Line Interface (CLI) explicitly targeting the physical Wi-Fi interface (`en0`).
Run ipscanner on the attacker for demonstration 

**Command:**
```bash
#command to get ip
ifconfig | grep "inet "
```

**Command:**
```bash
# Target 1: Victim IP | Target 2: Raspberry Pi IP
sudo ettercap -T -q -i en0 -M arp:remote /192.168.2.10// /192.168.2.5//
```

### Phase C: Credential Sniffing (Wireshark)
1. Open Wireshark on the **Attacker** device.
2. Listen on interface `en0`.
3. Filter by: `http.request.method == "POST"`
4. When the Victim logs into the Camera UI, the `POST` packet is intercepted.

## 4. Evidence & Findings

### Artifact Extraction

Because the application uses standard HTTP (Port 5001), the authentication artifacts are transmitted in plaintext.
* **Intercepted Username:** `admin`
* **Intercepted Password:** `admin`

### Log Discrepancy (Forensic Analysis)
A critical finding of this assessment is the **Log Correlation Gap**.
* The Raspberry Pi's `access_control.log` shows a `SUCCESS` entry from the Victim's IP.
* The Pi has **no record** that the data was intercepted by a third party.
* **Conclusion:** Host-based logging is insufficient for proving Data Confidentiality.

## 5. Remediation
To secure the forensic pipeline, the following controls are recommended:
1.  **Transport Layer Security (TLS):** Implement HTTPS to encrypt data in transit.
2.  **HSTS:** Enforce Strict Transport Security to prevent protocol downgrade attacks.
3.  **Static ARP:** Use static entries for critical IoT sensors to prevent spoofing.
```

### **Instructions for your GitHub:**
1.  Create a new file in your repo called `ATTACK_README.md`.
2.  Paste the code above.
3.  **Crucial:** Take a screenshot of your **Wireshark window** showing the `POST` packet and the password. Upload that image to your repo as `sniff_evidence.png`.
4.  Change the line `` in the text above to `![Sniff Evidence](./sniff_evidence.png)` so the image shows up on GitHub.

**Do you have the Wireshark screenshot ready to upload, or do you need help identifying the exact line in Wireshark to capture?**
