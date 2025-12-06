---
id: setup-guides-cloud-bridge
title: Cloud & Bridge Setup
sidebar_label: Cloud & Bridge
sidebar_position: 4
---

# Cloud & Bridge Setup

This guide covers cloud-based development workflows and bridging simulation environments with physical hardware. Ideal for students without local GPU resources or those wanting scalable compute power.

## Cloud Platform Options

### AWS EC2 GPU Instances

**Recommended Instance Types:**
- **g4dn.xlarge**: Entry-level (T4 GPU, 16GB RAM) - ~$0.52/hr
- **g5.xlarge**: Mid-range (A10G GPU, 24GB VRAM) - ~$1.00/hr
- **p3.2xlarge**: High-end (V100 GPU, 16GB VRAM) - ~$3.00/hr

**Setup Instructions:**

1. **Launch Instance**
   ```bash
   # Use AWS CLI or Console
   # Select Ubuntu 22.04 LTS Deep Learning AMI
   # Configure security groups (SSH, RDP, ROS ports)
   ```

2. **Install ROS 2**
   ```bash
   # SSH into instance
   ssh -i your-key.pem ubuntu@ec2-instance-ip
   
   # Follow software setup guide
   # ROS 2, Gazebo, Isaac Sim installation
   ```

3. **Configure Remote Desktop** (for GUI apps)
   ```bash
   # Install XFCE desktop
   sudo apt update
   sudo apt install -y xfce4 xfce4-goodies tightvncserver
   
   # Start VNC server
   vncserver :1
   
   # Connect with VNC client from local machine
   ```

### Google Cloud Platform (GCP)

**Recommended Instance:**
- **n1-standard-4** with **NVIDIA T4 GPU**
- ~$0.35/hr (preemptible) or ~$1.10/hr (standard)

**Setup:**
```bash
# Create instance with GPU
gcloud compute instances create robotics-dev \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --maintenance-policy=TERMINATE

# SSH into instance
gcloud compute ssh robotics-dev --zone=us-central1-a

# Install NVIDIA drivers
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
sudo python3 install_gpu_driver.py
```

### Azure Cloud

**Recommended VM:**
- **NC6s_v3**: Tesla V100, 6 vCPUs, 112 GB RAM - ~$3.00/hr

```bash
# Create resource group and VM
az group create --name robotics-rg --location eastus

az vm create \
  --resource-group robotics-rg \
  --name robotics-vm \
  --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts:latest \
  --size Standard_NC6s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys
```

## Cost Optimization Strategies

### Use Preemptible/Spot Instances
Save 60-90% by using interruptible instances for non-critical workloads:
```bash
# GCP Preemptible
gcloud compute instances create ... --preemptible

# AWS Spot
# Request via Spot Instances console
```

### Auto-Shutdown Scripts
```bash
# Schedule instance shutdown when idle
crontab -e

# Add: Shutdown at 11 PM daily
0 23 * * * sudo shutdown -h now
```

### Storage Management
```bash
# Use smaller boot disks, attach volumes as needed
# Clean Docker images regularly
docker system prune -a

# Remove old ROS build artifacts
cd ~/ros2_ws && rm -rf build install log
```

## Simulation-to-Hardware Bridge

### ROS 2 Bridge Architecture

**Cloud Simulation** ↔️ **ROS 2 Bridge** ↔️ **Local Jetson Hardware**

### Network Configuration

**1. VPN Setup (Recommended for Security)**
```bash
# Install WireGuard on both cloud and Jetson
sudo apt install -y wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Configure /etc/wireguard/wg0.conf
# Then:
sudo wg-quick up wg0
```

**2. Port Forwarding for Direct Connection**
- Open ports: 11311 (ROS), 9090 (rosbridge), custom DDS ports
- Use SSH tunneling for secure connection:
  ```bash
  ssh -L 9090:localhost:9090 -L 11311:localhost:11311 user@cloud-ip
  ```

### ROS 2 Domain ID Configuration

Ensure cloud and Jetson use same domain:
```bash
# On both systems, add to ~/.bashrc
export ROS_DOMAIN_ID=42

# Restart terminals or source
source ~/.bashrc
```

### rosbridge for WebSocket Communication

**On Cloud Instance:**
```bash
# Install rosbridge
sudo apt install -y ros-humble-rosbridge-server

# Launch rosbridge
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

**On Jetson (or any client):**
```python
# Python client example
import roslibpy

client = roslibpy.Ros(host='cloud-instance-ip', port=9090)
client.run()

listener = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
listener.subscribe(lambda message: print(message['data']))
```

### FastDDS Discovery Server (Recommended)

For efficient cloud-to-Jetson communication:

**On Cloud (Discovery Server):**
```bash
# Install FastDDS
sudo apt install -y ros-humble-fastrtps

# Launch discovery server
fastdds discovery --server-id 0 --ip-address 0.0.0.0 --port 11811
```

**On Jetson (Client):**
```bash
# Configure FastDDS to use discovery server
export ROS_DISCOVERY_SERVER="cloud-ip:11811"
export FASTRTPS_DEFAULT_PROFILES_FILE=/path/to/fastdds_profile.xml

# Create fastdds_profile.xml
cat << EOF > ~/fastdds_profile.xml
<?xml version="1.0" encoding="UTF-8" ?>
<profiles>
    <participant profile_name="client" is_default_profile="true">
        <rtps>
            <builtin>
                <discovery_config>
                    <discoveryProtocol>CLIENT</discoveryProtocol>
                    <discoveryServersList>
                        <RemoteServer prefix="44.53.00.5f.45.50.52.4f.53.49.4d.41">
                            <metatrafficUnicastLocatorList>
                                <locator>
                                    <udpv4>
                                        <address>cloud-ip</address>
                                        <port>11811</port>
                                    </udpv4>
                                </locator>
                            </metatrafficUnicastLocatorList>
                        </RemoteServer>
                    </discoveryServersList>
                </discovery_config>
            </builtin>
        </rtps>
    </participant>
</profiles>
EOF
```

## Hybrid Workflows

### Pattern 1: Cloud Training, Jetson Inference
```
1. Train models on cloud GPU (A100/V100)
2. Export to ONNX/TensorRT
3. Deploy to Jetson for real-time inference
```

**Example:**
```bash
# On cloud: Train PyTorch model
python train_model.py --epochs 100 --gpu

# Export to ONNX
python export_onnx.py --model checkpoint.pth

# Transfer to Jetson
scp model.onnx jetson-user@jetson-ip:~/models/

# On Jetson: Run inference with TensorRT
trtexec --onnx=model.onnx --saveEngine=model.trt
```

### Pattern 2: Sim-to-Real Transfer
```
1. Develop and test in cloud simulation (Isaac Sim/Gazebo)
2. Validate algorithms with high iteration speed
3. Deploy to Jetson with real sensors
4. Fine-tune with real-world data
```

### Pattern 3: Cloud as Compute Backend
```
1. Jetson collects sensor data
2. Send to cloud for heavy processing (SLAM, planning)
3. Return commands to Jetson
4. Jetson executes low-latency control
```

**Latency Considerations:**
- Local control loop: &lt;10ms (Jetson-only)
- Cloud-assisted: 50-200ms (acceptable for planning)
- Use edge computing for time-critical tasks

## Data Synchronization

### Sync Code and Datasets
```bash
# Use rsync for efficient sync
rsync -avz --progress ~/ros2_ws/ user@cloud-ip:~/ros2_ws/

# Or use Git with cloud repositories
git push origin main  # From local
git pull origin main   # On cloud
```

### ROS Bag Recording in Cloud
```bash
# Record simulation data
ros2 bag record -a -o simulation_data

# Download to local
scp -r user@cloud-ip:~/simulation_data.db3 ./
```

## Monitoring and Debugging

### Cloud Instance Monitoring
```bash
# GPU utilization
nvidia-smi -l 1

# Network traffic
iftop -i eth0

# ROS 2 network
ros2 node list
ros2 topic hz /topic_name
```

### Debug Bridge Connection
```bash
# Test network connectivity
ping cloud-ip

# Check ROS 2 discovery
ros2 daemon stop
ros2 daemon start
ros2 node list

# Check DDS traffic
tcpdump -i any port 7400
```

## Security Best Practices

1. **Use SSH Keys** (disable password auth)
2. **Firewall Rules**: Allow only necessary ports
3. **VPN for Production**: WireGuard or Tailscale
4. **Rotate Credentials**: Change keys regularly
5. **Monitor Access Logs**: Check for unauthorized access

## Verification Checklist

- [ ] Cloud instance launches with GPU support
- [ ] ROS 2 installed and functional on cloud
- [ ] Network bridge established (cloud ↔️ Jetson)
- [ ] ROS 2 topics visible across network
- [ ] Simulation runs smoothly (Gazebo/Isaac Sim)
- [ ] Latency acceptable for use case (&lt;200ms)
- [ ] Data sync working (rsync or Git)
- [ ] Cost monitoring enabled (billing alerts)

## Next Steps

With cloud and bridge configured:
1. Start [Module 1: ROS 2 Fundamentals](../modules/module-1-ros2/index.md)
2. Test cloud simulation with sample ROS 2 packages
3. Experiment with sim-to-real workflows

Need help with cloud setup? Join the course support channels! ☁️🤖
