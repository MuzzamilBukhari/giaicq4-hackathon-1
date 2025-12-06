---
id: setup-guides-software-setup
title: Software & Environment Setup
sidebar_label: Software Setup
sidebar_position: 3
---

# Software & Environment Setup

This guide covers installation of all required software for the Physical AI & Humanoid Robotics course, including ROS 2, simulation tools, and development environments.

## Ubuntu 22.04 LTS Setup

### Native Installation (Recommended)
1. Download [Ubuntu 22.04.3 LTS Desktop](https://ubuntu.com/download/desktop)
2. Create bootable USB with [Rufus](https://rufus.ie/) (Windows) or `dd` (Linux)
3. Install Ubuntu (dual-boot or dedicated machine)
4. Update system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### WSL2 Setup (Windows Alternative)
```powershell
# Run in PowerShell as Administrator
wsl --install -d Ubuntu-22.04

# After installation, create user account and update
sudo apt update && sudo apt upgrade -y

# Install WSLg for GUI support (included in Windows 11)
```

## ROS 2 Humble Installation

### Set Up Sources
```bash
# Ensure Ubuntu Universe repository is enabled
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add repository to sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### Install ROS 2 Packages
```bash
# Update package index
sudo apt update

# Install ROS 2 Humble Desktop (includes RViz, demos, tutorials)
sudo apt install -y ros-humble-desktop

# Install development tools
sudo apt install -y ros-dev-tools

# Install additional useful packages
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-joint-state-publisher \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-tf2-tools \
  ros-humble-rqt*
```

### Configure Environment
```bash
# Source ROS 2 setup (add to ~/.bashrc for persistence)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

### Verify Installation
```bash
# Check ROS 2 environment
printenv | grep -i ROS

# Run demo talker-listener
ros2 run demo_nodes_cpp talker  # Terminal 1
ros2 run demo_nodes_py listener  # Terminal 2
```

## Gazebo Simulation

### Gazebo Classic (Included with ROS 2)
Already installed with `ros-humble-desktop`. Verify:
```bash
gazebo --version  # Should show Gazebo 11.x
```

### Gazebo Fortress (Optional, Modern Alternative)
```bash
sudo apt install -y gazebo-fortress
```

## Python Development Environment

### Python 3.10+ Setup
```bash
# Python 3.10 included in Ubuntu 22.04
python3 --version

# Install pip and venv
sudo apt install -y python3-pip python3-venv

# Create virtual environment for course
python3 -m venv ~/envs/robotics
source ~/envs/robotics/bin/activate

# Add to ~/.bashrc for convenience
echo "alias activate-robotics='source ~/envs/robotics/bin/activate'" >> ~/.bashrc
```

### Install Core Python Packages
```bash
# Activate environment
source ~/envs/robotics/bin/activate

# Install essential libraries
pip install --upgrade pip
pip install \
  numpy \
  scipy \
  matplotlib \
  opencv-python \
  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
  transformers \
  gymnasium \
  pybullet \
  jupyter \
  pandas \
  scikit-learn
```

### ROS 2 Python Dependencies
```bash
pip install \
  colcon-common-extensions \
  rosdep \
  vcstool
```

## NVIDIA Isaac Sim Setup

### Prerequisites
- NVIDIA GPU with 8GB+ VRAM
- Driver 525.60.11 or later
- Vulkan support

### Install Omniverse Launcher
1. Download from [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/)
2. Install launcher:
   ```bash
   chmod +x omniverse-launcher-linux.AppImage
   ./omniverse-launcher-linux.AppImage
   ```
3. Sign in with NVIDIA account (free)

### Install Isaac Sim
1. Open Omniverse Launcher
2. Go to **Exchange** tab
3. Search for "Isaac Sim"
4. Install **Isaac Sim 2023.1.1** or later
5. Launch from **Library** tab

### Verify Isaac Sim
```bash
# Isaac Sim will be in:
~/.local/share/ov/pkg/isaac_sim-2023.1.1/

# Test import (from Isaac Sim Python)
~/.local/share/ov/pkg/isaac_sim-2023.1.1/python.sh -c "import omni.isaac.core"
```

## Unity Setup (Module 2)

### Install Unity Hub
```bash
# Download Unity Hub
wget https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.AppImage
chmod +x UnityHubSetup.AppImage
./UnityHubSetup.AppImage
```

### Install Unity Editor
1. Open Unity Hub
2. Install Unity **2022.3 LTS** (recommended for ROS integration)
3. Add Linux Build Support module

### Unity ROS Packages
- [ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [URDF-Importer](https://github.com/Unity-Technologies/URDF-Importer)

Installation instructions provided in Module 2.

## Development Tools

### Visual Studio Code
```bash
# Install via Snap
sudo snap install --classic code

# Install extensions
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code --install-extension ms-iot.vscode-ros
code --install-extension ms-toolsai.jupyter
```

### Git Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "nano"
```

### Additional Tools
```bash
sudo apt install -y \
  terminator \
  htop \
  tree \
  net-tools \
  curl \
  wget \
  unzip \
  cmake \
  build-essential
```

## Verification Script

Create a verification script to test all installations:

```bash
#!/bin/bash
# save as ~/verify_setup.sh

echo "=== ROS 2 Check ==="
ros2 --version

echo -e "\n=== Gazebo Check ==="
gazebo --version

echo -e "\n=== Python Check ==="
python3 --version
pip3 --version

echo -e "\n=== NVIDIA GPU Check ==="
nvidia-smi

echo -e "\n=== PyTorch CUDA Check ==="
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"

echo -e "\n=== ROS 2 Environment ==="
printenv | grep ROS_DISTRO

echo -e "\nSetup verification complete!"
```

Run verification:
```bash
chmod +x ~/verify_setup.sh
~/verify_setup.sh
```

## Post-Installation Checklist

- [ ] ROS 2 Humble installed and sourced
- [ ] Gazebo launches without errors
- [ ] Python virtual environment created
- [ ] PyTorch with CUDA support installed
- [ ] Isaac Sim launches (if using)
- [ ] Unity installed (for Module 2)
- [ ] VS Code installed with extensions
- [ ] Git configured
- [ ] All verification tests pass

## Common Issues

### ROS 2 Commands Not Found
```bash
# Add to ~/.bashrc
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

### Python Import Errors
```bash
# Activate virtual environment first
source ~/envs/robotics/bin/activate
```

### CUDA Not Available in PyTorch
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Gazebo Black Screen
```bash
# Update graphics drivers
sudo ubuntu-drivers autoinstall
sudo reboot
```

## Next Steps

With software installed:
1. Complete [Cloud & Bridge Setup](./cloud-bridge.md) (if using cloud)
2. Begin [Module 1: ROS 2 Fundamentals](../modules/module-1-ros2/index.md)
3. Test environment with Module 1 first lab

Happy coding! 💻🤖
