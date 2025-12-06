---
id: setup-guides-hardware-setup
title: Hardware Setup
sidebar_label: Hardware Setup
sidebar_position: 2
---

# Hardware Setup Guide

This guide covers the physical hardware setup for the Physical AI & Humanoid Robotics course, including workstation configuration and Jetson development kit assembly.

## Workstation Requirements

### Minimum Specifications
- **CPU**: Intel i5/AMD Ryzen 5 or better (8+ cores recommended)
- **RAM**: 16GB DDR4 (32GB recommended for Isaac Sim)
- **GPU**: NVIDIA RTX 3060 or better (RTX 4070+ recommended)
- **Storage**: 100GB free SSD space (NVMe preferred)
- **OS**: Ubuntu 22.04 LTS native or Windows 11 with WSL2

### Recommended Setup
- **CPU**: Intel i7-12700K / AMD Ryzen 7 5800X or better
- **RAM**: 32GB DDR4/DDR5
- **GPU**: NVIDIA RTX 4070 Ti / RTX 4080 (12GB+ VRAM)
- **Storage**: 500GB NVMe SSD
- **Display**: Dual monitors (productivity boost)

### GPU Driver Installation

**For Ubuntu (Native):**
```bash
# Add NVIDIA package repositories
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install latest NVIDIA driver (545+ recommended)
sudo apt install -y nvidia-driver-545
sudo reboot

# Verify installation
nvidia-smi
```

**For Windows with WSL2:**
- Install [NVIDIA GPU drivers for Windows](https://www.nvidia.com/Download/index.aspx)
- WSL2 will automatically use the Windows driver (no separate install needed)
- Verify in WSL: `nvidia-smi`

## NVIDIA Jetson Setup

### Supported Jetson Modules
- **Jetson Orin Nano** (8GB): Entry-level, good for learning
- **Jetson Orin NX** (16GB): Mid-range, balanced performance
- **Jetson AGX Orin** (32GB/64GB): High-end, production-grade

### Initial Jetson Configuration

1. **Flash JetPack SDK**
   - Download [NVIDIA SDK Manager](https://developer.nvidia.com/sdk-manager)
   - Flash JetPack 6.0+ (includes Ubuntu 22.04, CUDA, cuDNN)
   - Connect Jetson via USB-C in recovery mode
   - Follow SDK Manager prompts

2. **First Boot Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install essential tools
   sudo apt install -y build-essential cmake git nano htop
   
   # Verify CUDA installation
   nvcc --version
   
   # Check Jetson stats
   sudo -H pip3 install -U jetson-stats
   jtop
   ```

3. **Enable Maximum Performance**
   ```bash
   # Set to maximum power mode
   sudo nvpmodel -m 0
   
   # Enable all CPU cores
   sudo jetson_clocks
   ```

## Sensor Integration

### Camera Setup

**USB Webcam:**
```bash
# List video devices
v4l2-ctl --list-devices

# Test camera
sudo apt install -y cheese
cheese
```

**Intel RealSense D435i (Recommended):**
```bash
# Add Intel RealSense repository
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main"
sudo apt update

# Install RealSense SDK
sudo apt install -y librealsense2-dkms librealsense2-utils

# Test camera
realsense-viewer
```

### IMU Sensor (Optional)

**MPU6050/MPU9250 via I2C:**
```bash
# Enable I2C
sudo apt install -y i2c-tools
sudo usermod -aG i2c $USER

# Detect IMU
sudo i2cdetect -y -r 1

# Install Python library
pip3 install mpu6050-raspberrypi
```

### LiDAR Setup (Advanced)

**YDLiDAR X4:**
```bash
# Set permissions
sudo chmod 666 /dev/ttyUSB0

# Install ROS 2 driver (see Module 1)
```

## Networking & Connectivity

### WiFi Configuration
```bash
# Connect to WiFi
nmcli device wifi list
nmcli device wifi connect "SSID" password "PASSWORD"
```

### SSH Access (for headless operation)
```bash
# Enable SSH
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

# Find Jetson IP
ip addr show

# From workstation:
ssh username@jetson-ip
```

### Network Time Sync
```bash
# Install chrony for time synchronization
sudo apt install -y chrony
sudo systemctl enable chrony
```

## Power Management

### Jetson Power Considerations
- Use official NVIDIA power supply (15W for Nano, 65W for AGX)
- Avoid powering via USB-C alone for compute-intensive tasks
- Monitor power draw: `sudo jtop` → Power tab

### UPS Recommendation (Optional)
For production deployments, use an uninterruptible power supply to prevent data corruption during power loss.

## Verification Checklist

After completing hardware setup, verify:

- [ ] Workstation GPU recognized: `nvidia-smi` shows correct GPU
- [ ] Jetson boots successfully with JetPack 6.0+
- [ ] Camera detected and produces video feed
- [ ] IMU (if used) detected on I2C bus
- [ ] Network connectivity established (WiFi/Ethernet)
- [ ] SSH access working (for headless operation)
- [ ] Sufficient disk space available: `df -h`
- [ ] All fans operational, temperatures normal

## Troubleshooting

### GPU Not Detected
- Verify secure PCIe connection
- Check BIOS settings (ensure PCIe set to Gen3/Gen4)
- Try different driver version

### Jetson Won't Boot
- Re-flash JetPack with SDK Manager
- Check power supply (use official adapter)
- Try recovery mode boot

### Camera Not Working
- Check USB cable and port
- Verify permissions: `sudo usermod -aG video $USER`
- Test with different USB port

## Next Steps

With hardware configured, proceed to:
1. [Software & Environment Setup](./software-setup.md)
2. [Cloud & Bridge Setup](./cloud-bridge.md) (if using cloud resources)

Need help? Join the course Discord/Slack for hardware support! 🔧
