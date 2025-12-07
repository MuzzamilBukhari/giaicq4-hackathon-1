---
title: Chapter 1 Lab - Isaac Sim Basic Scene
sidebar_position: 2
description: Lab exercise to launch a sample Isaac Sim scene, spawn a robot, and publish camera data.
---

# Chapter 1 Lab: Isaac Sim Basic Scene

## Objective

In this lab, you will learn how to install and configure NVIDIA Isaac Sim, launch a sample scene, spawn a robot, and publish camera data. This hands-on exercise will help you understand the basic workflow of setting up and running simulations in Isaac Sim.

## Prerequisites

- NVIDIA GPU with Compute Capability 6.0+ (Pascal architecture or newer)
- Ubuntu 22.04 with ROS 2 Humble installed
- Docker installed (for Docker-based installation)
- NVIDIA Container Toolkit installed
- Basic understanding of Docker and containerization

## Estimated Time

90-120 minutes

## Lab Setup

### Step 1: Verify System Requirements

First, verify your system meets the requirements:

```bash
# Check GPU information
nvidia-smi

# Check CUDA version
nvcc --version

# Check Docker installation
docker --version

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

### Step 2: Install NVIDIA Container Toolkit

If not already installed, install the NVIDIA Container Toolkit:

```bash
# Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update

# Install NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-Container-runtime-configure --config=/etc/nvidia-container-runtime/config.toml

# Restart Docker
sudo systemctl restart docker
```

## Lab Exercises

### Exercise 1: Install Isaac Sim via Docker

In this exercise, you'll install Isaac Sim using the Docker method, which is recommended for development.

#### Step 1: Pull Isaac Sim Docker Image

Pull the latest Isaac Sim Docker image:

```bash
# Pull the Isaac Sim Docker image
docker pull nvcr.io/nvidia/isaac-sim:4.0.0

# Verify the image is downloaded
docker images | grep isaac-sim
```

#### Step 2: Create Docker Run Script

Create a script to run Isaac Sim with the proper configuration:

```bash
mkdir -p ~/isaac_sim_lab
cd ~/isaac_sim_lab

# Create a run script
cat > run_isaac_sim.sh << 'EOF'
#!/bin/bash

# Isaac Sim Docker Run Script

# Check if X11 forwarding is available
if [ -z "$DISPLAY" ]; then
    echo "Error: DISPLAY is not set. Please run this script from a graphical session."
    exit 1
fi

# Run Isaac Sim container
docker run --gpus all -it --rm \
  --network=host \
  --env "ACCEPT_EULA=Y" \
  --env "NVIDIA_VISIBLE_DEVICES=all" \
  --env "NVIDIA_DRIVER_CAPABILITIES=all" \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  --env "DISPLAY=$DISPLAY" \
  --volume $HOME/.Xauthority:/root/.Xauthority \
  --runtime=nvidia \
  --env "PRIVACY_CONSENT=Y" \
  --volume $HOME/isaac_sim_lab/assets:/assets \
  --volume $HOME/isaac_sim_lab/output:/output \
  nvcr.io/nvidia/isaac-sim:4.0.0
EOF

chmod +x run_isaac_sim.sh
```

#### Step 3: Create Assets Directory

Create directories for your custom assets and outputs:

```bash
mkdir -p ~/isaac_sim_lab/assets
mkdir -p ~/isaac_sim_lab/output
```

### Exercise 2: Launch Isaac Sim and Create Basic Scene

Now you'll launch Isaac Sim and create a basic scene with a robot and camera.

#### Step 1: Launch Isaac Sim

Run Isaac Sim using the script you created:

```bash
./run_isaac_sim.sh
```

**Note**: This will start Isaac Sim inside the Docker container. The Isaac Sim application should launch in a new window.

#### Step 2: Create a New Scene

Once Isaac Sim is running:

1. **Create New Stage**: Go to `File` → `New Stage`
2. **Set Units**: Go to `Window` → `Stage` → Set `Meters Per Unit` to `1.0`
3. **Set Up Axis**: Ensure `Y` is the up axis (default)

#### Step 3: Add Ground Plane

Add a ground plane to your scene:

1. **Create Ground**: Right-click in the viewport → `Create` → `Geometry` → `Plane`
2. **Rename**: Rename the plane to "GroundPlane"
3. **Position**: Set position to (0, 0, 0)
4. **Scale**: Set scale to (10, 1, 10) to create a 10x10 meter ground

#### Step 4: Add Physics to Ground

Make the ground plane a physical object:

1. **Select GroundPlane** in the Stage panel
2. **Add Physics**: Right-click → `Add Physics` → `Rigid Body`
3. **Set Static**: Check the `Kinematic` checkbox to make it static

### Exercise 3: Add a Robot to the Scene

In this exercise, you'll add a robot to the scene. We'll create a simple wheeled robot.

#### Step 1: Create Robot Base

1. **Create Base**: Right-click → `Create` → `Geometry` → `Cylinder`
2. **Rename**: Rename to "RobotBase"
3. **Position**: Set position to (0, 0.2, 0)
4. **Scale**: Set scale to (0.3, 0.2, 0.3) - this creates a 30cm diameter, 20cm tall base

#### Step 2: Add Physics to Robot Base

1. **Select RobotBase**
2. **Add Physics**: Right-click → `Add Physics` → `Rigid Body`
3. **Set Properties**:
   - Mass: 10.0 kg
   - Collision: Add collision approximation

#### Step 3: Add Wheels

1. **Create Wheels**: Right-click → `Create` → `Geometry` → `Cylinder`
2. **Left Wheel**: Position at (-0.2, 0.1, 0.2), scale (0.1, 0.05, 0.1)
3. **Right Wheel**: Position at (-0.2, 0.1, -0.2), scale (0.1, 0.05, 0.1)
4. **Rename**: "LeftWheel" and "RightWheel"

#### Step 4: Add Joints (Optional)

For a more advanced robot, you can add joints to connect wheels to the base:

1. **Select LeftWheel** in the Stage panel
2. **Add Joint**: Right-click → `Add Physics` → `Joint` → `Revolute Joint`
3. **Configure Joint**:
   - Set parent to RobotBase
   - Set axis to Y-axis rotation
   - Set limits as needed

### Exercise 4: Add and Configure Camera

Now you'll add a camera to the scene and configure it to publish data.

#### Step 1: Add Camera Prim

1. **Create Camera**: Right-click → `Create` → `Isaac Sensors` → `Camera`
2. **Rename**: Rename to "RobotCamera"
3. **Position**: Place on top of the robot base at (0, 0.5, 0)

#### Step 2: Configure Camera Properties

1. **Select RobotCamera**
2. **Set Properties** in the Property panel:
   - **Resolution**: Width: 640, Height: 480
   - **Focal Length**: 24.0
   - **Horizontal Aperture**: 20.955
   - **Vertical Aperture**: 15.2907

#### Step 3: Add ROS Bridge Components

To publish camera data to ROS:

1. **Add ROS Bridge**: In the Isaac Sim extension window, find `Isaac ROS Bridge`
2. **Add Camera Publisher**: Add a `ROS Camera Publisher` component
3. **Configure Topic**: Set topic name to `/robot_camera/image_raw`
4. **Connect**: Connect the camera output to the publisher

### Exercise 5: Create Python Script for Robot Control

Create a Python script that will run inside Isaac Sim to control the robot and process camera data.

#### Step 1: Create Robot Control Script

Create `~/isaac_sim_lab/robot_control.py`:

```python
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.sensor import Camera
import numpy as np
import carb
import asyncio

class SimpleRobotController:
    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)
        self.camera = None
        self.robot_base = None

    def setup_scene(self):
        """Setup the scene with robot and camera"""

        # Create ground plane
        self.world.scene.add_default_ground_plane()

        # Create robot base (simple approach using a cube)
        from omni.isaac.core.objects import DynamicCuboid
        self.robot_base = self.world.scene.add(
            DynamicCuboid(
                prim_path="/World/RobotBase",
                name="robot_base",
                position=np.array([0, 0.2, 0]),
                size=0.3,
                mass=10.0
            )
        )

        # Add camera
        self.camera = self.world.scene.add(
            Camera(
                prim_path="/World/RobotCamera",
                position=np.array([0, 0.5, 0]),
                frequency=20
            )
        )

        # Set initial camera view
        set_camera_view(eye=np.array([2, 2, 2]), target=np.array([0, 0, 0]))

    async def run_simulation(self):
        """Run the simulation with robot control"""
        self.world.reset()

        for i in range(1000):  # Run for 1000 steps
            self.world.step(render=True)

            # Simple movement pattern every 10 steps
            if i % 10 == 0:
                # Apply force to move robot forward
                if self.robot_base:
                    current_pos = self.robot_base.get_world_pose()[0]
                    new_pos = current_pos + np.array([0.01, 0, 0.02])
                    self.robot_base.set_world_pose(position=new_pos)

            # Capture and log camera data every 20 steps
            if i % 20 == 0 and self.camera:
                try:
                    rgb_image = self.camera.get_rgb()
                    if rgb_image is not None:
                        print(f"Captured RGB image at step {i}, shape: {rgb_image.shape}")
                except Exception as e:
                    print(f"Error capturing camera data: {e}")

            if i % 100 == 0:
                print(f"Simulation step: {i}")

        print("Simulation completed")

def run_robot_control():
    """Main function to run the robot controller"""
    controller = SimpleRobotController()
    controller.setup_scene()

    # Run the async simulation
    async def run_async():
        await controller.run_simulation()

    asyncio.run(run_async())

# This can be run from Isaac Sim's scripting window
if __name__ == "__main__":
    run_robot_control()
```

#### Step 2: Create USD Stage File

Create a simple USD file that defines your robot:

Create `~/isaac_sim_lab/assets/simple_robot.usd`:

```usd
#usda 1.0
(
    doc = "Simple robot for Isaac Sim lab"
    metersPerUnit = 1.0
    upAxis = "Y"
)

def Xform "SimpleRobot"
{
    def Xform "Base"
    {
        def Cylinder "BaseLink"
        {
            radius = 0.15
            height = 0.2
            extent = [(-0.15, -0.1, -0.15), (0.15, 0.1, 0.15)]

            prepend apiSchemas = ["PhysicsRigidBodyAPI"]
            PhysicsRigidBodyAPI:mass = 10.0
        }
    }

    def Xform "LeftWheel"
    {
        add xformOp:translate = (-0.2, 0.1, 0.2)
        def Cylinder "Wheel"
        {
            radius = 0.1
            height = 0.05
            extent = [(-0.1, -0.025, -0.05), (0.1, 0.025, 0.05)]

            prepend apiSchemas = ["PhysicsRigidBodyAPI"]
            PhysicsRigidBodyAPI:mass = 0.5
        }
    }

    def Xform "RightWheel"
    {
        add xformOp:translate = (-0.2, 0.1, -0.2)
        def Cylinder "Wheel"
        {
            radius = 0.1
            height = 0.05
            extent = [(-0.1, -0.025, -0.05), (0.1, 0.025, 0.05)]

            prepend apiSchemas = ["PhysicsRigidBodyAPI"]
            PhysicsRigidBodyAPI:mass = 0.5
        }
    }

    def Camera "Camera"
    {
        add xformOp:translate = (0, 0.5, 0)
        prepend apiSchemas = ["Camera"]
        Camera:resolution = (640, 480)
        Camera:clippingRange = (0.1, 1000.0)
    }
}
```

### Exercise 6: Run Isaac Sim with Custom Assets

Now you'll run Isaac Sim and load your custom robot.

#### Step 1: Load Custom Robot

In Isaac Sim:

1. **Open Stage**: Go to `File` → `Open Stage`
2. **Navigate**: Go to `/assets/simple_robot.usd`
3. **Load**: Open the file to load your custom robot

#### Step 2: Add ROS Bridge for Camera Data

1. **Open Isaac ROS Extension**: Go to `Window` → `Extensions` → Find and enable `Isaac ROS Bridge`
2. **Add Camera Publisher**: In the extension panel, add a camera publisher
3. **Configure**: Set the camera path to `/World/SimpleRobot/Camera` and topic to `/robot_camera/image_raw`

#### Step 3: Run the Simulation

1. **Play Simulation**: Click the play button in Isaac Sim
2. **Monitor Camera**: Check that camera data is being published to ROS
3. **Observe Robot**: Watch the robot move in the simulation

### Exercise 7: Verify Camera Data Publication

Now you'll verify that camera data is being published correctly.

#### Step 1: Set up ROS Terminal

Open a new terminal outside the Isaac Sim container:

```bash
# Source ROS
source /opt/ros/humble/setup.bash

# Check available topics
ros2 topic list
```

#### Step 2: Monitor Camera Data

Monitor the camera topic to verify data publication:

```bash
# Echo the camera info topic
ros2 topic echo /robot_camera/camera_info

# Or use rqt_image_view to visualize the camera feed
sudo apt update
sudo apt install ros-humble-rqt-image-view
ros2 run rqt_image_view rqt_image_view
```

#### Step 3: Create ROS Subscriber Node

Create a ROS node to subscribe to the camera data:

Create `~/isaac_sim_lab/camera_subscriber.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/robot_camera/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.bridge = CvBridge()
        self.image_counter = 0

        self.get_logger().info('Camera subscriber node started')

    def listener_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Display image info
            self.get_logger().info(f'Received image {self.image_counter}: {cv_image.shape}')

            # Optionally save the image
            if self.image_counter % 100 == 0:  # Save every 100th image
                filename = f'/tmp/isaac_sim_image_{self.image_counter:06d}.png'
                cv2.imwrite(filename, cv_image)
                self.get_logger().info(f'Saved image to {filename}')

            self.image_counter += 1

        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    camera_subscriber = CameraSubscriber()

    try:
        rclpy.spin(camera_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        camera_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Step 4: Run the ROS Subscriber

Run the ROS subscriber in your host terminal:

```bash
# Make sure Isaac Sim is running with the ROS bridge
# In a new terminal, run:
python3 ~/isaac_sim_lab/camera_subscriber.py
```

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: Isaac Sim Installation
- [ ] Isaac Sim Docker container runs successfully
- [ ] Isaac Sim GUI launches without errors
- [ ] Basic scene creation tools are accessible

### Verification 2: Robot Creation
- [ ] Robot model appears in Isaac Sim scene
- [ ] Robot has proper physics properties
- [ ] Robot responds to basic physics simulation

### Verification 3: Camera Setup
- [ ] Camera is properly positioned on the robot
- [ ] Camera captures images in the simulation
- [ ] Camera has correct resolution and properties

### Verification 4: ROS Bridge
- [ ] ROS bridge extension is enabled and configured
- [ ] Camera data is published to `/robot_camera/image_raw`
- [ ] ROS subscriber successfully receives camera messages

### Verification 5: Data Publication
- [ ] Camera images are being saved to `/tmp/` directory
- [ ] Image dimensions match configured camera resolution
- [ ] ROS topics are accessible and publishing data

## Expected Results

After completing this lab, you should have:

1. Successfully installed and configured NVIDIA Isaac Sim using Docker
2. Created a basic scene with a robot and camera in Isaac Sim
3. Configured the ROS bridge to publish camera data
4. Verified that camera data is being published to ROS topics
5. Demonstrated the end-to-end workflow from Isaac Sim to ROS

## Troubleshooting

### Common Issues

**Isaac Sim won't start:**
- Check that your GPU supports Isaac Sim requirements
- Verify NVIDIA drivers are properly installed
- Ensure Docker and NVIDIA Container Toolkit are correctly configured

**No camera data in ROS:**
- Verify ROS bridge extension is enabled
- Check camera path matches the one configured in the bridge
- Confirm Isaac Sim is actively simulating

**Docker permission errors:**
- Add your user to the docker group: `sudo usermod -aG docker $USER`
- Log out and back in for changes to take effect
- Verify Docker permissions with `docker run hello-world`

**Camera images not displaying:**
- Check that the camera is properly positioned in the scene
- Verify camera resolution and aperture settings
- Ensure the camera has a clear view of the scene

## Summary

This lab provided hands-on experience with setting up NVIDIA Isaac Sim, creating a basic robot simulation, and establishing ROS communication for camera data. You learned how to install Isaac Sim using Docker, create custom USD assets, configure sensors, and bridge simulation data to ROS. These foundational skills are essential for more advanced Isaac Sim workflows.

## Next Steps

In the next chapter, you'll explore Isaac Sim's advanced perception pipeline capabilities, including synthetic RGB/Depth generation, semantic segmentation, and LiDAR simulation.