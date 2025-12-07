---
title: Chapter 2 Lab - Perception Pipeline Integration
sidebar_position: 3
description: Lab exercise to build a simple perception pipeline and stream data to ROS 2 Humble.
---

# Chapter 2 Lab: Perception Pipeline Integration

## Objective

In this lab, you will build a complete perception pipeline in Isaac Sim that generates synthetic RGB/Depth data, semantic segmentation, and LiDAR point clouds, then stream this data to ROS 2 Humble. This hands-on exercise will help you understand how to integrate Isaac Sim's perception capabilities with ROS-based computer vision workflows.

## Prerequisites

- NVIDIA Isaac Sim installed and running (from Chapter 1)
- Ubuntu 22.04 with ROS 2 Humble installed
- Python 3.8+ with OpenCV and NumPy
- Completion of Chapter 1 lab
- Basic understanding of ROS 2 concepts (topics, messages)

## Estimated Time

120-150 minutes

## Lab Setup

### Step 1: Create ROS Workspace

Create a new ROS workspace for the perception pipeline:

```bash
mkdir -p ~/isaac_perception_ws/src
cd ~/isaac_perception_ws
colcon build
source install/setup.bash
```

### Step 2: Install Required Dependencies

Install additional Python packages needed for the perception pipeline:

```bash
pip3 install opencv-python numpy transforms3d
```

### Step 3: Create Lab Package

Create a package for the perception pipeline:

```bash
cd ~/isaac_perception_ws/src
ros2 pkg create --build-type ament_python isaac_perception_pipeline
```

Create the package structure:

```bash
mkdir -p ~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline
mkdir -p ~/isaac_perception_ws/src/isaac_perception_pipeline/test
```

## Lab Exercises

### Exercise 1: Create Isaac Sim Perception Scene

In this exercise, you'll create a scene in Isaac Sim with multiple sensors for the perception pipeline.

#### Step 1: Create USD Scene File

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/scenes/perception_scene.usd`:

```usd
#usda 1.0
(
    doc = "Perception pipeline test scene for Isaac Sim"
    metersPerUnit = 1.0
    upAxis = "Y"
)

def Xform "PerceptionScene"
{
    # Physics scene
    def PhysicsScene "PhysicsScene"
    {
        physics:gravity = (0, -9.81, 0)
    }

    # Ground plane
    def Xform "GroundPlane"
    {
        def Plane "Plane"
        {
            size = 10
        }

        def PhysicsRigidBodyAPI "Plane"
        {
            physics:kinematicEnabled = 1
        }
    }

    # Test objects with semantic labels
    def Xform "RedCube"
    {
        add xformOp:translate = (2, 0.5, 0)
        def Cube "Cube"
        {
            size = 1
        }

        def PhysicsRigidBodyAPI "Cube"
        {
            physics:mass = 1.0
        }

        # Semantic label
        custom string semantic:tag = "obstacle"
    }

    def Xform "BlueSphere"
    {
        add xformOp:translate = (-2, 0.5, 1)
        def Sphere "Sphere"
        {
            radius = 0.5
        }

        def PhysicsRigidBodyAPI "Sphere"
        {
            physics:mass = 1.0
        }

        # Semantic label
        custom string semantic:tag = "object"
    }

    def Xform "GreenCylinder"
    {
        add xformOp:translate = (0, 0.5, -2)
        def Cylinder "Cylinder"
        {
            radius = 0.4
            height = 1.0
        }

        def PhysicsRigidBodyAPI "Cylinder"
        {
            physics:mass = 1.0
        }

        # Semantic label
        custom string semantic:tag = "obstacle"
    }

    # Robot platform with sensors
    def Xform "RobotPlatform"
    {
        add xformOp:translate = (0, 0.5, 0)

        # RGB-D camera
        def Camera "RGBCamera"
        {
            add xformOp:translate = (0.2, 0.8, 0)
            custom float[] sensor:resolution = [640, 480]
            custom float sensor:horizontal_fov = 60
            custom float sensor:clipping_range = (0.1, 100)
        }

        # LiDAR sensor
        def Xform "LiDAR"
        {
            add xformOp:translate = (0.3, 0.8, 0)
        }
    }
}
```

#### Step 2: Create Isaac Sim Setup Script

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/isaac_sim_setup.py`:

```python
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.sensor import Camera, RotatingLidarSensor
import numpy as np

class PerceptionScene:
    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)
        self.rgb_camera = None
        self.lidar = None
        self.scene_initialized = False

    def setup_perception_scene(self):
        """Setup the perception scene with all required sensors"""
        print("Setting up perception scene...")

        # Add default ground plane
        self.world.scene.add_default_ground_plane()

        # Create RGB-D camera
        self.rgb_camera = self.world.scene.add(
            Camera(
                prim_path="/World/RobotPlatform/RGBCamera",
                position=np.array([0.2, 0.8, 0]),
                frequency=30,
                resolution=(640, 480),
                focal_length=24.0,
                horizontal_aperture=20.955,
                clipping_range=(0.1, 100.0)
            )
        )

        # Create LiDAR sensor
        self.lidar = self.world.scene.add(
            RotatingLidarSensor(
                prim_path="/World/RobotPlatform/LiDAR",
                position=np.array([0.3, 0.8, 0]),
                rotation_rate=10,  # 10 Hz
                channels=16,
                samples_per_channel=512,
                horizontal_resolution=1.0,  # degrees
                vertical_resolution=2.0,    # degrees
                range_threshold=50.0        # meters
            )
        )

        # Add test objects
        from omni.isaac.core.objects import DynamicCuboid, DynamicSphere, DynamicCylinder

        # Red cube (obstacle)
        self.world.scene.add(
            DynamicCuboid(
                prim_path="/World/RedCube",
                name="red_cube",
                position=np.array([2, 0.5, 0]),
                size=1.0,
                color=np.array([0.8, 0.1, 0.1])
            )
        )

        # Blue sphere (object)
        self.world.scene.add(
            DynamicSphere(
                prim_path="/World/BlueSphere",
                name="blue_sphere",
                position=np.array([-2, 0.5, 1]),
                radius=0.5,
                color=np.array([0.1, 0.1, 0.8])
            )
        )

        # Green cylinder (obstacle)
        self.world.scene.add(
            DynamicCylinder(
                prim_path="/World/GreenCylinder",
                name="green_cylinder",
                position=np.array([0, 0.5, -2]),
                radius=0.4,
                height=1.0,
                color=np.array([0.1, 0.8, 0.1])
            )
        )

        # Set initial camera view
        set_camera_view(eye=np.array([5, 5, 5]), target=np.array([0, 0, 0]))

        self.scene_initialized = True
        print("Perception scene setup complete!")

    def get_sensor_data(self):
        """Get data from all sensors"""
        if not self.scene_initialized:
            return None

        sensor_data = {}

        try:
            # Get RGB image
            rgb_image = self.rgb_camera.get_rgb()
            if rgb_image is not None:
                sensor_data['rgb'] = rgb_image

            # Get depth image
            depth_image = self.rgb_camera.get_depth()
            if depth_image is not None:
                sensor_data['depth'] = depth_image

            # Get semantic segmentation
            semantic_image = self.rgb_camera.get_semantic_segmentation(bbox_dims=True)
            if semantic_image is not None:
                sensor_data['semantic'] = semantic_image

            # Get LiDAR point cloud
            lidar_data = self.lidar.get_sensor_readings()
            if lidar_data:
                sensor_data['lidar'] = lidar_data

        except Exception as e:
            print(f"Error getting sensor data: {e}")

        return sensor_data

    def run_simulation(self, num_steps=1000):
        """Run the simulation and collect sensor data"""
        if not self.scene_initialized:
            print("Scene not initialized!")
            return

        print(f"Running simulation for {num_steps} steps...")

        self.world.reset()

        for step in range(num_steps):
            self.world.step(render=True)

            if step % 100 == 0:
                print(f"Simulation step: {step}")

        print("Simulation completed!")
```

### Exercise 2: Create ROS Bridge for Perception Data

Now you'll create a ROS bridge that publishes Isaac Sim perception data to ROS topics.

#### Step 1: Create Perception Bridge Node

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/perception_bridge.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2, CameraInfo
from std_msgs.msg import Header
from cv_bridge import CvBridge
import numpy as np
import array

class PerceptionBridge(Node):
    def __init__(self):
        super().__init__('perception_bridge')

        # Initialize CvBridge for image conversion
        self.bridge = CvBridge()

        # Publishers for different sensor types
        self.rgb_pub = self.create_publisher(Image, '/perception/rgb/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/perception/depth/image_raw', 10)
        self.camera_info_pub = self.create_publisher(CameraInfo, '/perception/rgb/camera_info', 10)
        self.lidar_pub = self.create_publisher(PointCloud2, '/perception/lidar/points', 10)

        # Camera parameters
        self.camera_width = 640
        self.camera_height = 480
        self.camera_fx = 554.25  # Focal length in x
        self.camera_fy = 554.25  # Focal length in y
        self.camera_cx = 320     # Principal point x
        self.camera_cy = 240     # Principal point y

        # Timer for publishing data
        self.timer = self.create_timer(0.1, self.publish_data)  # 10 Hz

        # Storage for latest sensor data (to be filled by Isaac Sim)
        self.latest_rgb = None
        self.latest_depth = None
        self.latest_lidar = None

        self.get_logger().info('Perception Bridge Node initialized')

    def set_sensor_data(self, sensor_data):
        """Set the latest sensor data from Isaac Sim"""
        if 'rgb' in sensor_data:
            self.latest_rgb = sensor_data['rgb']

        if 'depth' in sensor_data:
            self.latest_depth = sensor_data['depth']

        if 'lidar' in sensor_data:
            self.latest_lidar = sensor_data['lidar']

    def publish_data(self):
        """Publish the latest sensor data to ROS topics"""
        current_time = self.get_clock().now().to_msg()

        # Publish RGB image
        if self.latest_rgb is not None:
            try:
                rgb_msg = self.bridge.cv2_to_imgmsg(self.latest_rgb, encoding='rgb8')
                rgb_msg.header.stamp = current_time
                rgb_msg.header.frame_id = 'camera_rgb_optical_frame'
                self.rgb_pub.publish(rgb_msg)
            except Exception as e:
                self.get_logger().error(f'Error publishing RGB: {e}')

        # Publish depth image
        if self.latest_depth is not None:
            try:
                # Convert depth to 16-bit millimeters
                depth_16bit = (self.latest_depth * 1000).astype(np.uint16)
                depth_msg = self.bridge.cv2_to_imgmsg(depth_16bit, encoding='16UC1')
                depth_msg.header.stamp = current_time
                depth_msg.header.frame_id = 'camera_depth_optical_frame'
                self.depth_pub.publish(depth_msg)
            except Exception as e:
                self.get_logger().error(f'Error publishing depth: {e}')

        # Publish camera info
        camera_info_msg = CameraInfo()
        camera_info_msg.header.stamp = current_time
        camera_info_msg.header.frame_id = 'camera_rgb_optical_frame'
        camera_info_msg.width = self.camera_width
        camera_info_msg.height = self.camera_height
        camera_info_msg.k = [self.camera_fx, 0.0, self.camera_cx,
                            0.0, self.camera_fy, self.camera_cy,
                            0.0, 0.0, 1.0]
        camera_info_msg.p = [self.camera_fx, 0.0, self.camera_cx, 0.0,
                            0.0, self.camera_fy, self.camera_cy, 0.0,
                            0.0, 0.0, 1.0, 0.0]
        self.camera_info_pub.publish(camera_info_msg)

        # Publish LiDAR data (simplified - in real implementation, proper PointCloud2 construction needed)
        if self.latest_lidar is not None:
            # This is a simplified version - full implementation would need proper PointCloud2 message
            lidar_msg = PointCloud2()
            lidar_msg.header.stamp = current_time
            lidar_msg.header.frame_id = 'lidar_frame'
            lidar_msg.height = 1
            lidar_msg.width = len(self.latest_lidar) if self.latest_lidar else 0
            lidar_msg.is_dense = False
            lidar_msg.is_bigendian = False

            # Define point fields (x, y, z, intensity)
            lidar_msg.fields = [
                # Add proper field definitions here
            ]

            # Add data bytes here
            lidar_msg.data = b''

            if lidar_msg.width > 0:
                self.lidar_pub.publish(lidar_msg)

    def get_latest_data(self):
        """Get the latest published data for verification"""
        return {
            'rgb': self.latest_rgb,
            'depth': self.latest_depth,
            'lidar': self.latest_lidar
        }

def main(args=None):
    rclpy.init(args=args)

    # In a real scenario, this would be called from Isaac Sim
    # For this lab, we'll create a minimal test
    node = PerceptionBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Step 2: Create Main Integration Script

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/main_integration.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import time

class PerceptionPipelineIntegrator(Node):
    def __init__(self):
        super().__init__('perception_pipeline_integrator')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Subscribe to perception topics
        self.rgb_sub = self.create_subscription(
            Image, '/perception/rgb/image_raw', self.rgb_callback, 10)

        self.depth_sub = self.create_subscription(
            Image, '/perception/depth/image_raw', self.depth_callback, 10)

        # Timer for processing loop
        self.timer = self.create_timer(0.5, self.process_callback)

        # Data storage
        self.latest_rgb = None
        self.latest_depth = None
        self.frame_counter = 0

        self.get_logger().info('Perception Pipeline Integrator started')

    def rgb_callback(self, msg):
        """Process incoming RGB images"""
        try:
            self.latest_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
            self.get_logger().info(f'Received RGB image: {msg.width}x{msg.height}')
        except Exception as e:
            self.get_logger().error(f'Error processing RGB: {e}')

    def depth_callback(self, msg):
        """Process incoming depth images"""
        try:
            self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='16UC1')
            self.get_logger().info(f'Received depth image: {msg.width}x{msg.height}')
        except Exception as e:
            self.get_logger().error(f'Error processing depth: {e}')

    def process_callback(self):
        """Process perception data"""
        if self.latest_rgb is not None:
            # Perform basic processing on RGB image
            height, width, channels = self.latest_rgb.shape

            # Calculate some basic statistics
            avg_color = np.mean(self.latest_rgb, axis=(0, 1))
            self.get_logger().info(f'Average RGB values: R={avg_color[0]:.1f}, G={avg_color[1]:.1f}, B={avg_color[2]:.1f}')

            # Save processed image periodically
            if self.frame_counter % 10 == 0:
                import cv2
                filename = f'/tmp/processed_rgb_{self.frame_counter:06d}.png'
                cv2.imwrite(filename, cv2.cvtColor(self.latest_rgb, cv2.COLOR_RGB2BGR))
                self.get_logger().info(f'Saved processed image: {filename}')

        if self.latest_depth is not None:
            # Process depth data
            valid_depths = self.latest_depth[self.latest_depth > 0]
            if len(valid_depths) > 0:
                avg_depth = np.mean(valid_depths) / 1000.0  # Convert from mm to meters
                self.get_logger().info(f'Average depth: {avg_depth:.2f} meters')

        self.frame_counter += 1

def main(args=None):
    rclpy.init(args=args)
    integrator = PerceptionPipelineIntegrator()

    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Exercise 3: Create Perception Processing Node

Create a node that demonstrates how to process the perception data flowing from Isaac Sim.

#### Step 1: Create Object Detection Node

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/object_detector.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import numpy as np
import cv2

class ObjectDetector(Node):
    def __init__(self):
        super().__init__('object_detector')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Subscribe to RGB and depth images
        self.rgb_sub = self.create_subscription(
            Image, '/perception/rgb/image_raw', self.rgb_callback, 10)

        self.depth_sub = self.create_subscription(
            Image, '/perception/depth/image_raw', self.depth_callback, 10)

        self.camera_info_sub = self.create_subscription(
            CameraInfo, '/perception/rgb/camera_info', self.camera_info_callback, 10)

        # Publishers for processed data
        self.detection_pub = self.create_publisher(Image, '/perception/detections', 10)

        # Camera parameters storage
        self.camera_matrix = None
        self.distortion_coeffs = None

        # Data storage
        self.latest_rgb = None
        self.latest_depth = None

        self.get_logger().info('Object Detector Node started')

    def camera_info_callback(self, msg):
        """Process camera info to get intrinsic parameters"""
        self.camera_matrix = np.array(msg.k).reshape(3, 3)
        self.distortion_coeffs = np.array(msg.d)

    def rgb_callback(self, msg):
        """Process RGB image for object detection"""
        try:
            self.latest_rgb = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')

            # Perform object detection
            detections = self.detect_objects(self.latest_rgb)

            # Draw detections on image
            annotated_img = self.draw_detections(self.latest_rgb.copy(), detections)

            # Publish annotated image
            annotated_msg = self.bridge.cv2_to_imgmsg(annotated_img, encoding='rgb8')
            annotated_msg.header = msg.header
            self.detection_pub.publish(annotated_msg)

            self.get_logger().info(f'Detected {len(detections)} objects')

        except Exception as e:
            self.get_logger().error(f'Error in RGB callback: {e}')

    def depth_callback(self, msg):
        """Process depth image for 3D information"""
        try:
            self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='16UC1')
        except Exception as e:
            self.get_logger().error(f'Error in depth callback: {e}')

    def detect_objects(self, image):
        """Simple object detection based on color thresholds"""
        # Convert BGR to HSV for better color detection
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        detections = []

        # Define color ranges for different objects
        color_ranges = [
            ([0, 50, 50], [10, 255, 255], "Red"),      # Red objects
            ([100, 50, 50], [130, 255, 255], "Blue"),  # Blue objects
            ([40, 50, 50], [80, 255, 255], "Green")    # Green objects
        ]

        for lower, upper, label in color_ranges:
            # Create mask for this color range
            lower = np.array(lower)
            upper = np.array(upper)
            mask = cv2.inRange(hsv, lower, upper)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process each contour
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Filter small contours
                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(contour)

                    detection = {
                        'label': label,
                        'bbox': (x, y, w, h),
                        'confidence': 0.9,  # For synthetic data, high confidence
                        'center': (x + w//2, y + h//2)
                    }
                    detections.append(detection)

        return detections

    def draw_detections(self, image, detections):
        """Draw detection results on image"""
        annotated_img = image.copy()

        for detection in detections:
            x, y, w, h = detection['bbox']
            label = detection['label']
            confidence = detection['confidence']

            # Draw bounding box
            cv2.rectangle(annotated_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw label
            label_text = f"{label}: {confidence:.1f}"
            cv2.putText(annotated_img, label_text, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return annotated_img

    def get_3d_position(self, pixel_x, pixel_y, depth_value):
        """Convert 2D pixel + depth to 3D world coordinates"""
        if self.camera_matrix is None:
            return None

        # Convert depth from mm to meters
        depth_m = depth_value / 1000.0

        # Use camera intrinsics to convert to 3D
        x = (pixel_x - self.camera_matrix[0, 2]) * depth_m / self.camera_matrix[0, 0]
        y = (pixel_y - self.camera_matrix[1, 2]) * depth_m / self.camera_matrix[1, 1]
        z = depth_m

        return (x, y, z)

def main(args=None):
    rclpy.init(args=args)
    detector = ObjectDetector()

    try:
        rclpy.spin(detector)
    except KeyboardInterrupt:
        pass
    finally:
        detector.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Exercise 4: Test the Complete Pipeline

Now you'll test the complete perception pipeline integration.

#### Step 1: Update Package Configuration

Update the `setup.py` file in `~/isaac_perception_ws/src/isaac_perception_pipeline/`:

```python
from setuptools import setup

package_name = 'isaac_perception_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/scenes', ['scenes/perception_scene.usd']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Package for Isaac Sim perception pipeline integration',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'perception_bridge = isaac_perception_pipeline.perception_bridge:main',
            'main_integration = isaac_perception_pipeline.main_integration:main',
            'object_detector = isaac_perception_pipeline.object_detector:main',
        ],
    },
)
```

Update the `package.xml` file:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>isaac_perception_pipeline</name>
  <version>0.0.0</version>
  <description>Package for Isaac Sim perception pipeline integration</description>
  <maintainer email="user@todo.todo">user</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>sensor_msgs</depend>
  <depend>std_msgs</depend>
  <depend>cv_bridge</depend>

  <exec_depend>ros2launch</exec_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

#### Step 2: Build the Package

Build your ROS package:

```bash
cd ~/isaac_perception_ws
colcon build --packages-select isaac_perception_pipeline
source install/setup.bash
```

#### Step 3: Create Isaac Sim Integration Script

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/isaac_integration_test.py`:

```python
#!/usr/bin/env python3
"""
Isaac Sim Integration Test Script
This script demonstrates how to integrate Isaac Sim with the ROS perception pipeline
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import time
import asyncio

# Import Isaac Sim components (these would be available when running inside Isaac Sim)
try:
    from omni.isaac.core import World
    from omni.isaac.sensor import Camera
    import omni
    ISAAC_AVAILABLE = True
except ImportError:
    ISAAC_AVAILABLE = False
    print("Isaac Sim not available - running in test mode")

class IsaacSimROSIntegration(Node):
    def __init__(self):
        super().__init__('isaac_sim_ros_integration')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Publishers for Isaac Sim data
        self.rgb_pub = self.create_publisher(Image, '/isaac_sim/rgb/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/isaac_sim/depth/image_raw', 10)

        # Timer for publishing simulated data
        self.timer = self.create_timer(0.1, self.publish_simulated_data)  # 10 Hz

        # Simulated sensor data
        self.frame_counter = 0
        self.isaac_world = None

        self.get_logger().info('Isaac Sim ROS Integration Node started')

    def initialize_isaac_world(self):
        """Initialize Isaac Sim world (in real scenario)"""
        if ISAAC_AVAILABLE:
            self.isaac_world = World(stage_units_in_meters=1.0)
            # Setup would happen here in real implementation
            return True
        else:
            self.get_logger().warn('Isaac Sim not available - using simulated data')
            return False

    def get_isaac_sensor_data(self):
        """Get sensor data from Isaac Sim (simulated for this example)"""
        # In a real implementation, this would get actual data from Isaac Sim
        # For this lab, we'll generate simulated data

        # Generate a simple test image
        height, width = 480, 640
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

        # Add some color patches to simulate objects
        rgb_image[100:200, 100:200] = [255, 0, 0]    # Red patch
        rgb_image[200:300, 300:400] = [0, 255, 0]    # Green patch
        rgb_image[300:400, 200:300] = [0, 0, 255]    # Blue patch

        # Add a moving pattern
        offset = (self.frame_counter * 2) % width
        rgb_image[50:80, offset:offset+50] = [255, 255, 255]  # Moving white bar

        # Generate depth image (simplified)
        depth_image = np.ones((height, width), dtype=np.uint16) * 1000  # 1 meter
        depth_image[100:200, 100:200] = 2000   # 2 meters for red object
        depth_image[200:300, 300:400] = 1500   # 1.5 meters for green object
        depth_image[300:400, 200:300] = 2500   # 2.5 meters for blue object

        return {
            'rgb': rgb_image,
            'depth': depth_image
        }

    def publish_simulated_data(self):
        """Publish simulated Isaac Sim data to ROS topics"""
        try:
            # Get simulated sensor data
            sensor_data = self.get_isaac_sensor_data()

            current_time = self.get_clock().now().to_msg()

            # Publish RGB image
            if 'rgb' in sensor_data:
                rgb_msg = self.bridge.cv2_to_imgmsg(sensor_data['rgb'], encoding='rgb8')
                rgb_msg.header.stamp = current_time
                rgb_msg.header.frame_id = 'isaac_camera_rgb_optical_frame'
                self.rgb_pub.publish(rgb_msg)

            # Publish depth image
            if 'depth' in sensor_data:
                depth_msg = self.bridge.cv2_to_imgmsg(sensor_data['depth'], encoding='16UC1')
                depth_msg.header.stamp = current_time
                depth_msg.header.frame_id = 'isaac_camera_depth_optical_frame'
                self.depth_pub.publish(depth_msg)

            self.frame_counter += 1
            if self.frame_counter % 100 == 0:
                self.get_logger().info(f'Published {self.frame_counter} frames')

        except Exception as e:
            self.get_logger().error(f'Error publishing simulated data: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = IsaacSimROSIntegration()

    # Initialize Isaac Sim world if available
    node.initialize_isaac_world()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Step 4: Create Launch File

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/launch/perception_pipeline.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare launch arguments
    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # Perception bridge node
    perception_bridge = Node(
        package='isaac_perception_pipeline',
        executable='perception_bridge',
        name='perception_bridge',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Main integration node
    main_integration = Node(
        package='isaac_perception_pipeline',
        executable='main_integration',
        name='main_integration',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Object detector node
    object_detector = Node(
        package='isaac_perception_pipeline',
        executable='object_detector',
        name='object_detector',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_argument,
        perception_bridge,
        main_integration,
        object_detector
    ])
```

#### Step 5: Test the Pipeline

Test the complete perception pipeline:

```bash
# Build the workspace
cd ~/isaac_perception_ws
colcon build --packages-select isaac_perception_pipeline
source install/setup.bash

# Run the launch file
ros2 launch isaac_perception_pipeline perception_pipeline.launch.py
```

### Exercise 5: Verify Pipeline Functionality

Now you'll verify that the perception pipeline is working correctly.

#### Step 1: Create Verification Script

Create `~/isaac_perception_ws/src/isaac_perception_pipeline/isaac_perception_pipeline/verify_pipeline.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import time

class PipelineVerifier(Node):
    def __init__(self):
        super().__init__('pipeline_verifier')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Subscribe to perception topics
        self.rgb_sub = self.create_subscription(
            Image, '/perception/rgb/image_raw', self.rgb_callback, 10)

        self.depth_sub = self.create_subscription(
            Image, '/perception/depth/image_raw', self.depth_callback, 10)

        # Data verification storage
        self.received_rgb = False
        self.received_depth = False
        self.start_time = time.time()
        self.timeout = 30  # 30 seconds timeout

        # Verification counters
        self.rgb_count = 0
        self.depth_count = 0

        self.get_logger().info('Pipeline Verifier started - waiting for data...')

    def rgb_callback(self, msg):
        """Verify RGB image data"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')

            # Verify image properties
            height, width, channels = cv_image.shape
            if height == 480 and width == 640 and channels == 3:
                self.received_rgb = True
                self.rgb_count += 1

                # Log verification success
                avg_color = np.mean(cv_image)
                self.get_logger().info(f'✓ RGB verification: {width}x{height}x{channels}, avg color: {avg_color:.1f}')

                # Save first image for verification
                if self.rgb_count == 1:
                    import cv2
                    cv2.imwrite('/tmp/verified_rgb.png', cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR))
                    self.get_logger().info('Saved verification RGB image to /tmp/verified_rgb.png')
            else:
                self.get_logger().error(f'✗ RGB image has wrong dimensions: {cv_image.shape}')

        except Exception as e:
            self.get_logger().error(f'✗ Error processing RGB: {e}')

    def depth_callback(self, msg):
        """Verify depth image data"""
        try:
            cv_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='16UC1')

            # Verify depth image properties
            height, width = cv_depth.shape
            if height == 480 and width == 640:
                self.received_depth = True
                self.depth_count += 1

                # Check depth values (should be in reasonable range for synthetic data)
                valid_depths = cv_depth[cv_depth > 0]
                if len(valid_depths) > 0:
                    avg_depth = np.mean(valid_depths) / 1000.0  # Convert to meters
                    self.get_logger().info(f'✓ Depth verification: {width}x{height}, avg: {avg_depth:.2f}m')

                    # Save first depth image for verification
                    if self.depth_count == 1:
                        import cv2
                        cv2.imwrite('/tmp/verified_depth.png', cv_depth)
                        self.get_logger().info('Saved verification depth image to /tmp/verified_depth.png')
                else:
                    self.get_logger().warn('Depth image has no valid values')
            else:
                self.get_logger().error(f'✗ Depth image has wrong dimensions: {cv_depth.shape}')

        except Exception as e:
            self.get_logger().error(f'✗ Error processing depth: {e}')

    def verify_pipeline(self):
        """Verify that pipeline is receiving data"""
        current_time = time.time()

        # Check if we've received data within timeout
        if current_time - self.start_time > self.timeout:
            self.get_logger().info(f'Verification timeout after {self.timeout}s')
            return False

        # Check if we've received both RGB and depth data
        if self.received_rgb and self.received_depth:
            self.get_logger().info(f'✓ Pipeline verification successful!')
            self.get_logger().info(f'  RGB messages received: {self.rgb_count}')
            self.get_logger().info(f'  Depth messages received: {self.depth_count}')
            return True

        return False

def main(args=None):
    rclpy.init(args=args)
    verifier = PipelineVerifier()

    # Run verification for a period of time
    start_time = time.time()
    timeout = 30  # 30 seconds

    while time.time() - start_time < timeout:
        rclpy.spin_once(verifier, timeout_sec=0.1)

        if verifier.verify_pipeline():
            verifier.get_logger().info('Pipeline verification completed successfully!')
            break
    else:
        verifier.get_logger().info('Pipeline verification timed out.')

    # Print final results
    if verifier.received_rgb:
        verifier.get_logger().info('✓ RGB data verified')
    else:
        verifier.get_logger().info('✗ No RGB data received')

    if verifier.received_depth:
        verifier.get_logger().info('✓ Depth data verified')
    else:
        verifier.get_logger().info('✗ No depth data received')

    verifier.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Add the verification script to the setup.py entry points:

```python
entry_points={
    'console_scripts': [
        'perception_bridge = isaac_perception_pipeline.perception_bridge:main',
        'main_integration = isaac_perception_pipeline.main_integration:main',
        'object_detector = isaac_perception_pipeline.object_detector:main',
        'verify_pipeline = isaac_perception_pipeline.verify_pipeline:main',
    ],
},
```

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: Isaac Sim Scene Setup
- [ ] Perception scene with RGB-D camera and LiDAR loads successfully
- [ ] Test objects are properly placed in the scene
- [ ] All sensors are configured with correct parameters

### Verification 2: ROS Bridge Configuration
- [ ] Perception bridge node starts without errors
- [ ] RGB, depth, and camera info topics are published
- [ ] LiDAR data is published to appropriate topics

### Verification 3: Data Publication
- [ ] RGB images are published to `/perception/rgb/image_raw`
- [ ] Depth images are published to `/perception/depth/image_raw`
- [ ] Camera info is published to `/perception/rgb/camera_info`
- [ ] All topics have correct message types and frame IDs

### Verification 4: Perception Processing
- [ ] Object detection node receives and processes RGB data
- [ ] Depth data is properly interpreted
- [ ] Detection results are published and visualized

### Verification 5: Pipeline Verification
- [ ] Verification script confirms data flow
- [ ] RGB images have correct dimensions (640x480x3)
- [ ] Depth images have correct dimensions (640x480) with valid values
- [ ] Images are saved to `/tmp/` directory for inspection

## Expected Results

After completing this lab, you should have:

1. Created a complete perception pipeline in Isaac Sim with RGB-D camera and LiDAR
2. Established ROS bridge connection to stream sensor data to ROS 2
3. Implemented perception processing nodes that consume the sensor data
4. Verified that the complete pipeline functions correctly with proper data flow
5. Demonstrated integration between Isaac Sim simulation and ROS-based perception workflows

## Troubleshooting

### Common Issues

**No data being published:**
- Check that Isaac Sim is running and simulating
- Verify ROS bridge extension is enabled in Isaac Sim
- Confirm topic names match between publisher and subscriber

**Wrong image dimensions:**
- Check camera resolution settings in Isaac Sim
- Verify camera configuration parameters
- Confirm RGB/depth encoding matches expectations

**Performance issues:**
- Reduce simulation frequency if needed
- Check GPU utilization and memory usage
- Consider reducing scene complexity for testing

**Connection problems:**
- Verify Isaac Sim and ROS are properly configured
- Check network settings if using distributed setup
- Confirm Isaac Sim extension paths are correct

## Summary

This lab provided hands-on experience with building a complete perception pipeline that integrates Isaac Sim with ROS 2. You learned how to configure multiple sensors, bridge simulation data to ROS topics, and process perception data using ROS nodes. This foundation is essential for developing advanced robotics perception systems using synthetic data.

## Next Steps

In the next chapter, you'll explore how to use Isaac Sim for AI training integration, including creating synthetic datasets for machine learning and implementing sim-to-real transfer techniques.