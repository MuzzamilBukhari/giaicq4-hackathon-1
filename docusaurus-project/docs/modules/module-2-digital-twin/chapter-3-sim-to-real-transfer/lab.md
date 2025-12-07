---
title: Chapter 3 Lab - Domain Randomized Camera Simulation
sidebar_position: 4
description: Lab exercise to implement domain randomization for camera simulation and export a small synthetic data sample.
---

# Chapter 3 Lab: Domain Randomized Camera Simulation

## Objective

In this lab, you will implement domain randomization techniques for camera simulation and export a small synthetic dataset. This hands-on exercise will help you understand how to make simulated camera data more robust and realistic, bridging the gap between simulation and real-world applications.

## Prerequisites

- Ubuntu 22.04 with ROS 2 Humble installed
- Gazebo Classic installed
- Python 3.8+ with OpenCV and NumPy installed
- Completion of Chapter 1-3 theory content
- Basic understanding of computer vision concepts

## Estimated Time

90-120 minutes

## Lab Setup

### Step 1: Install Required Dependencies

Install the necessary Python packages:

```bash
pip3 install opencv-python numpy scikit-image matplotlib
```

### Step 2: Create Workspace

Create a new ROS 2 workspace for this lab:

```bash
mkdir -p ~/domain_rand_ws/src
cd ~/domain_rand_ws
colcon build
source install/setup.bash
```

### Step 3: Create Lab Package

Create a package for the domain randomization lab:

```bash
cd ~/domain_rand_ws/src
ros2 pkg create --build-type ament_python domain_rand_lab
```

Create the package structure:

```bash
mkdir -p ~/domain_rand_ws/src/domain_rand_lab/domain_rand_lab
mkdir -p ~/domain_rand_ws/src/domain_rand_lab/test
```

## Lab Exercises

### Exercise 1: Create Randomized Gazebo World

In this exercise, you'll create a Gazebo world with randomized elements that will be used for domain randomization.

#### Step 1: Create World File with Randomizable Elements

Create `~/domain_rand_ws/src/domain_rand_lab/worlds/randomized_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="randomized_world">
    <!-- Physics -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
    </physics>

    <!-- Sun with randomized properties -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground plane with randomized texture -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>20 20</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
            <specular>0.0 0.0 0.0 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- Randomized objects -->
    <model name="random_box_1">
      <pose>2 1 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
            <diffuse>0.8 0.2 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.1</iyy>
            <iyz>0.0</iyz>
            <izz>0.1</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="random_box_2">
      <pose>-2 -1 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.4 0.4 0.8</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.4 0.4 0.8</size>
            </box>
          </geometry>
          <material>
            <ambient>0.2 0.8 0.2 1</ambient>
            <diffuse>0.2 0.8 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.1</iyy>
            <iyz>0.0</iyz>
            <izz>0.1</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="random_cylinder">
      <pose>0 2 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <length>1.0</length>
              <radius>0.3</radius>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <length>1.0</length>
              <radius>0.3</radius>
            </cylinder>
          </geometry>
          <material>
            <ambient>0.2 0.2 0.8 1</ambient>
            <diffuse>0.2 0.2 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.1</iyy>
            <iyz>0.0</iyz>
            <izz>0.1</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Camera with realistic parameters -->
    <model name="camera_model">
      <pose>0 0 2 0 0 0</pose>
      <link name="camera_link">
        <visual name="visual">
          <geometry>
            <box>
              <size>0.1 0.1 0.1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.1 0.1 0.1</size>
            </box>
          </geometry>
        </collision>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.001</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.001</iyy>
            <iyz>0.0</iyz>
            <izz>0.001</izz>
          </inertia>
        </inertial>
      </link>

      <sensor name="camera" type="camera">
        <camera>
          <horizontal_fov>1.089</horizontal_fov> <!-- 62.4 degrees -->
          <image>
            <width>640</width>
            <height>480</height>
            <format>R8G8B8</format>
          </image>
          <clip>
            <near>0.1</near>
            <far>100</far>
          </clip>
        </camera>
        <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
          <frame_name>camera_link</frame_name>
          <topic_name>/domain_rand_camera/image_raw</topic_name>
          <hack_baseline>0.07</hack_baseline>
        </plugin>
      </sensor>
    </model>
  </world>
</sdf>
```

#### Step 2: Create Launch File

Create `~/domain_rand_ws/src/domain_rand_lab/launch/domain_rand_world.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package share directory
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_domain_rand = get_package_share_directory('domain_rand_lab')

    # Get world file path
    world_path = os.path.join(pkg_domain_rand, 'worlds', 'randomized_world.sdf')

    # Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_path,
            'verbose': 'true'
        }.items()
    )

    return LaunchDescription([
        gazebo,
    ])
```

### Exercise 2: Implement Domain Randomization Script

Now you'll create a Python script that implements domain randomization techniques for the camera simulation.

#### Step 1: Create Domain Randomization Node

Create `~/domain_rand_ws/src/domain_rand_lab/domain_rand_lab/domain_randomization_node.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np
import random
from datetime import datetime

class DomainRandomizationNode(Node):
    def __init__(self):
        super().__init__('domain_randomization_node')

        # Initialize CvBridge for image conversion
        self.bridge = CvBridge()

        # Create publisher for randomized images
        self.randomized_image_pub = self.create_publisher(
            Image, '/domain_rand_camera/randomized_image', 10)

        # Create subscriber for raw camera images
        self.image_sub = self.create_subscription(
            Image, '/domain_rand_camera/image_raw', self.image_callback, 10)

        # Create publisher for domain randomization parameters
        self.param_pub = self.create_publisher(
            String, '/domain_rand_params', 10)

        # Timer for periodic randomization updates
        self.timer = self.create_timer(5.0, self.randomize_parameters)

        # Initialize randomization parameters
        self.current_params = {
            'light_intensity': 1.0,
            'light_color': [1.0, 1.0, 1.0],
            'noise_level': 0.0,
            'blur_level': 0.0,
            'color_shift': [0.0, 0.0, 0.0],
            'brightness': 0.0,
            'contrast': 1.0
        }

        # Data collection for synthetic dataset
        self.dataset_counter = 0
        self.dataset_dir = '/tmp/domain_rand_dataset'
        import os
        os.makedirs(self.dataset_dir, exist_ok=True)

        self.get_logger().info('Domain Randomization Node initialized')

    def randomize_parameters(self):
        """Randomize domain parameters"""
        # Randomize lighting
        self.current_params['light_intensity'] = random.uniform(0.5, 1.5)
        self.current_params['light_color'] = [
            random.uniform(0.8, 1.2),
            random.uniform(0.8, 1.2),
            random.uniform(0.8, 1.2)
        ]

        # Randomize noise
        self.current_params['noise_level'] = random.uniform(0.0, 0.1)

        # Randomize blur
        self.current_params['blur_level'] = random.uniform(0.0, 1.0)

        # Randomize color shift
        self.current_params['color_shift'] = [
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1),
            random.uniform(-0.1, 0.1)
        ]

        # Randomize brightness and contrast
        self.current_params['brightness'] = random.uniform(-0.2, 0.2)
        self.current_params['contrast'] = random.uniform(0.8, 1.2)

        # Publish current parameters
        param_msg = String()
        param_str = f"Light: {self.current_params['light_intensity']:.2f}, " \
                   f"Noise: {self.current_params['noise_level']:.2f}, " \
                   f"Blur: {self.current_params['blur_level']:.2f}"
        param_msg.data = param_str
        self.param_pub.publish(param_msg)

        self.get_logger().info(f'Randomized parameters: {param_str}')

    def image_callback(self, msg):
        """Process incoming camera images with domain randomization"""
        try:
            # Convert ROS image to OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Apply domain randomization
            randomized_image = self.apply_domain_randomization(cv_image)

            # Convert back to ROS image
            randomized_msg = self.bridge.cv2_to_imgmsg(randomized_image, encoding='bgr8')
            randomized_msg.header = msg.header

            # Publish randomized image
            self.randomized_image_pub.publish(randomized_msg)

            # Export to synthetic dataset periodically
            if self.dataset_counter % 10 == 0:  # Export every 10th image
                self.export_to_dataset(randomized_image)

            self.dataset_counter += 1

        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

    def apply_domain_randomization(self, image):
        """Apply domain randomization techniques to image"""
        # Make a copy to avoid modifying original
        result = image.copy().astype(np.float32)

        # Apply brightness adjustment
        brightness = self.current_params['brightness']
        result = result + (brightness * 255.0)

        # Apply contrast adjustment
        contrast = self.current_params['contrast']
        result = (result - 127.5) * contrast + 127.5

        # Apply color shift
        color_shift = self.current_params['color_shift']
        result[:, :, 0] = result[:, :, 0] + (color_shift[0] * 255.0)  # Blue channel
        result[:, :, 1] = result[:, :, 1] + (color_shift[1] * 255.0)  # Green channel
        result[:, :, 2] = result[:, :, 2] + (color_shift[2] * 255.0)  # Red channel

        # Apply blur
        blur_level = int(self.current_params['blur_level'] * 5)
        if blur_level > 0:
            kernel_size = blur_level * 2 + 1
            result = cv2.GaussianBlur(result, (kernel_size, kernel_size), 0)

        # Apply noise
        noise_level = self.current_params['noise_level']
        if noise_level > 0:
            noise = np.random.normal(0, noise_level * 255.0, result.shape)
            result = result + noise

        # Clip values to valid range [0, 255]
        result = np.clip(result, 0, 255)

        return result.astype(np.uint8)

    def export_to_dataset(self, image):
        """Export image to synthetic dataset"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{self.dataset_dir}/synthetic_{self.dataset_counter:06d}_{timestamp}.png"

        # Save image
        cv2.imwrite(filename, image)

        # Save metadata
        metadata_filename = f"{self.dataset_dir}/metadata_{self.dataset_counter:06d}_{timestamp}.txt"
        with open(metadata_filename, 'w') as f:
            f.write(f"Image: synthetic_{self.dataset_counter:06d}_{timestamp}.png\n")
            f.write(f"Counter: {self.dataset_counter}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Parameters:\n")
            for key, value in self.current_params.items():
                f.write(f"  {key}: {value}\n")

        self.get_logger().info(f'Exported synthetic image {filename}')

def main(args=None):
    rclpy.init(args=args)
    node = DomainRandomizationNode()

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

#### Step 2: Create Image Analysis Script

Create `~/domain_rand_ws/src/domain_rand_lab/domain_rand_lab/image_analyzer.py`:

```python
#!/usr/bin/env python3
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os
import argparse

class ImageAnalyzer:
    def __init__(self):
        pass

    def calculate_ssim(self, img1, img2):
        """Calculate Structural Similarity Index"""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        return ssim(gray1, gray2)

    def calculate_mse(self, img1, img2):
        """Calculate Mean Squared Error"""
        return np.mean((img1 - img2) ** 2)

    def calculate_psnr(self, img1, img2):
        """Calculate Peak Signal-to-Noise Ratio"""
        mse = self.calculate_mse(img1, img2)
        if mse == 0:
            return float('inf')
        max_pixel = 255.0
        return 20 * np.log10(max_pixel / np.sqrt(mse))

    def analyze_dataset(self, dataset_dir):
        """Analyze the synthetic dataset"""
        image_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        image_files.sort()

        if len(image_files) < 2:
            print("Need at least 2 images for comparison")
            return

        print(f"Analyzing {len(image_files)} images in dataset")

        # Calculate statistics across all images
        brightness_values = []
        contrast_values = []
        color_stats = []

        for img_file in image_files:
            img_path = os.path.join(dataset_dir, img_file)
            img = cv2.imread(img_path)

            if img is not None:
                # Calculate brightness (mean of all pixels)
                brightness = np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                brightness_values.append(brightness)

                # Calculate contrast (standard deviation of grayscale)
                contrast = np.std(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                contrast_values.append(contrast)

                # Calculate color statistics
                color_mean = [np.mean(img[:,:,i]) for i in range(3)]
                color_std = [np.std(img[:,:,i]) for i in range(3)]
                color_stats.append((color_mean, color_std))

        # Print statistics
        print(f"Dataset Statistics:")
        print(f"  Number of images: {len(image_files)}")
        print(f"  Brightness range: {min(brightness_values):.2f} - {max(brightness_values):.2f}")
        print(f"  Average brightness: {np.mean(brightness_values):.2f}")
        print(f"  Contrast range: {min(contrast_values):.2f} - {max(contrast_values):.2f}")
        print(f"  Average contrast: {np.mean(contrast_values):.2f}")

        # Analyze diversity
        if len(image_files) > 1:
            # Compare first few images to check diversity
            img1 = cv2.imread(os.path.join(dataset_dir, image_files[0]))
            img2 = cv2.imread(os.path.join(dataset_dir, image_files[1]))

            if img1 is not None and img2 is not None:
                ssim_score = self.calculate_ssim(img1, img2)
                mse_score = self.calculate_mse(img1, img2)
                psnr_score = self.calculate_psnr(img1, img2)

                print(f"\nDiversity Analysis (between first two images):")
                print(f"  SSIM: {ssim_score:.3f}")
                print(f"  MSE: {mse_score:.3f}")
                print(f"  PSNR: {psnr_score:.3f}")

    def visualize_dataset(self, dataset_dir, num_samples=5):
        """Visualize sample images from the dataset"""
        image_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        image_files.sort()

        if len(image_files) == 0:
            print("No images found in dataset directory")
            return

        # Select sample images evenly spaced through the dataset
        step = max(1, len(image_files) // num_samples)
        sample_files = image_files[::step][:num_samples]

        fig, axes = plt.subplots(1, len(sample_files), figsize=(15, 3))
        if len(sample_files) == 1:
            axes = [axes]

        for i, img_file in enumerate(sample_files):
            img_path = os.path.join(dataset_dir, img_file)
            img = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) if img is not None else np.zeros((100, 100, 3))

            axes[i].imshow(img_rgb)
            axes[i].set_title(f'Sample {i+1}\n{img_file[:20]}...')
            axes[i].axis('off')

        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analyze synthetic dataset from domain randomization')
    parser.add_argument('--dataset_dir', type=str, default='/tmp/domain_rand_dataset',
                        help='Directory containing synthetic dataset')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze the dataset statistics')
    parser.add_argument('--visualize', action='store_true',
                        help='Visualize sample images from the dataset')

    args = parser.parse_args()

    analyzer = ImageAnalyzer()

    if args.analyze:
        analyzer.analyze_dataset(args.dataset_dir)

    if args.visualize:
        analyzer.visualize_dataset(args.dataset_dir)

if __name__ == '__main__':
    main()
```

### Exercise 3: Test Domain Randomization

Now you'll test the domain randomization system and collect a synthetic dataset.

#### Step 1: Update Package Configuration

Update the `setup.py` file in `~/domain_rand_ws/src/domain_rand_lab/`:

```python
from setuptools import setup

package_name = 'domain_rand_lab'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/worlds', ['worlds/randomized_world.sdf']),
        ('share/' + package_name + '/launch', ['launch/domain_rand_world.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Package for domain randomization lab',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'domain_randomization_node = domain_rand_lab.domain_randomization_node:main',
            'image_analyzer = domain_rand_lab.image_analyzer:main',
        ],
    },
)
```

Update the `package.xml` file:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>domain_rand_lab</name>
  <version>0.0.0</version>
  <description>Package for domain randomization lab</description>
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

#### Step 2: Build and Run the System

Build your workspace:

```bash
cd ~/domain_rand_ws
colcon build --packages-select domain_rand_lab
source install/setup.bash
```

First, launch Gazebo with the randomized world:

```bash
source ~/domain_rand_ws/install/setup.bash
ros2 launch domain_rand_lab domain_rand_world.launch.py
```

In another terminal, start the domain randomization node:

```bash
source ~/domain_rand_ws/install/setup.bash
ros2 run domain_rand_lab domain_randomization_node
```

#### Step 3: Collect and Analyze Data

Let the system run for a few minutes to collect synthetic data. Then, in another terminal, analyze the collected dataset:

```bash
source ~/domain_rand_ws/install/setup.bash
ros2 run domain_rand_lab image_analyzer --analyze --visualize
```

### Exercise 4: Compare Original and Randomized Images

Create a comparison script to validate the domain randomization effects.

#### Step 1: Create Comparison Script

Create `~/domain_rand_ws/src/domain_rand_lab/domain_rand_lab/comparison_script.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class ImageComparisonNode(Node):
    def __init__(self):
        super().__init__('image_comparison_node')

        # Initialize CvBridge
        self.bridge = CvBridge()

        # Store the last original and randomized images
        self.original_image = None
        self.randomized_image = None
        self.original_timestamp = None
        self.randomized_timestamp = None

        # Create subscribers
        self.original_sub = self.create_subscription(
            Image, '/domain_rand_camera/image_raw', self.original_callback, 10)

        self.randomized_sub = self.create_subscription(
            Image, '/domain_rand_camera/randomized_image', self.randomized_callback, 10)

        # Timer to periodically save comparison images
        self.timer = self.create_timer(10.0, self.save_comparison)

        # Directory for saving comparisons
        self.comparison_dir = '/tmp/domain_rand_comparisons'
        import os
        os.makedirs(self.comparison_dir, exist_ok=True)

        self.comparison_counter = 0

        self.get_logger().info('Image Comparison Node initialized')

    def original_callback(self, msg):
        """Store original image"""
        try:
            self.original_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.original_timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        except Exception as e:
            self.get_logger().error(f'Error processing original image: {str(e)}')

    def randomized_callback(self, msg):
        """Store randomized image"""
        try:
            self.randomized_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            self.randomized_timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        except Exception as e:
            self.get_logger().error(f'Error processing randomized image: {str(e)}')

    def save_comparison(self):
        """Save comparison of original and randomized images"""
        if self.original_image is not None and self.randomized_image is not None:
            # Create a side-by-side comparison
            comparison_img = np.hstack((self.original_image, self.randomized_image))

            # Add text labels
            cv2.putText(comparison_img, 'Original', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(comparison_img, 'Randomized', (self.original_image.shape[1] + 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Save the comparison image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.comparison_dir}/comparison_{self.comparison_counter:04d}_{timestamp}.png"
            cv2.imwrite(filename, comparison_img)

            self.get_logger().info(f'Saved comparison image: {filename}')
            self.comparison_counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = ImageComparisonNode()

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

#### Step 2: Run the Comparison

In another terminal, run the comparison node:

```bash
source ~/domain_rand_ws/install/setup.bash
ros2 run domain_rand_lab comparison_script
```

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: Gazebo World Setup
- [ ] Randomized world loads successfully in Gazebo
- [ ] Camera model is present and publishing images
- [ ] Objects with randomized colors are visible

### Verification 2: Domain Randomization Node
- [ ] Domain randomization node starts without errors
- [ ] Node publishes randomized images to `/domain_rand_camera/randomized_image`
- [ ] Parameters are randomized periodically

### Verification 3: Dataset Export
- [ ] Synthetic images are saved to `/tmp/domain_rand_dataset`
- [ ] Metadata files are created with randomization parameters
- [ ] Images show visible domain randomization effects

### Verification 4: Image Comparison
- [ ] Comparison images show differences between original and randomized versions
- [ ] Randomization effects (brightness, color, blur, noise) are visible
- [ ] Comparison images are saved to `/tmp/domain_rand_comparisons`

## Expected Results

After completing this lab, you should have:

1. Successfully created a Gazebo world with randomizable elements
2. Implemented domain randomization techniques for camera simulation
3. Generated a synthetic dataset with randomized visual properties
4. Validated the domain randomization effects through image comparison
5. Demonstrated the effectiveness of domain randomization in simulation

## Troubleshooting

### Common Issues

**Gazebo fails to launch:**
- Check that the world file path is correct
- Verify Gazebo Classic is installed properly
- Ensure the SDF file is properly formatted

**No images being published:**
- Check that the camera plugin is properly configured
- Verify ROS topics are being published (`ros2 topic list`)
- Confirm camera model pose and configuration

**Domain randomization not visible:**
- Verify the domain randomization node is running
- Check that image processing is working correctly
- Ensure randomization parameters are being applied

**Dataset not being saved:**
- Check write permissions to the dataset directory
- Verify the image analyzer is working correctly
- Confirm the export function is being called

## Summary

This lab provided hands-on experience with domain randomization techniques for camera simulation. You learned how to create randomized environments in Gazebo, implement domain randomization algorithms in ROS 2, and generate synthetic datasets that are more robust to real-world variations. These techniques are essential for bridging the sim-to-real gap in robotics applications.

## Next Steps

With the completion of Module 2, you now have a comprehensive understanding of digital twin and simulation technologies. Module 3 will introduce you to NVIDIA Isaac Sim, which provides GPU-accelerated simulation capabilities and advanced perception pipelines for robotics applications.