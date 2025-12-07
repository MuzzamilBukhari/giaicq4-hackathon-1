---
id: chapter-3-bipedal-locomotion-lab
title: Lab - Simulate a Simple Biped Balance or Walking Sequence in Gazebo/Isaac
sidebar_label: "Lab: Biped Balance & Walking Simulation"
---

# Lab: Simulate a Simple Biped Balance or Walking Sequence in Gazebo/Isaac

## Overview

In this lab, you will simulate a simple bipedal walking and balance control system using the Zero-Moment Point (ZMP) theory. You'll implement a basic walking pattern generator and balance controller that maintains stability during locomotion. The simulation will be performed in either Gazebo or Isaac Sim.

## Learning Objectives

- Implement basic ZMP-based balance control
- Generate stable walking patterns using simplified MPC concepts
- Simulate bipedal locomotion in a physics environment
- Understand the relationship between ZMP and robot stability

## Prerequisites

- ROS 2 Humble installed and configured
- Gazebo Classic or Isaac Sim installed
- Basic understanding of physics simulation
- Python programming experience
- Understanding of ZMP theory from the chapter content

## Estimated Time

120-150 minutes

## Setup

1. Create a new workspace for the biped simulation:
   ```bash
   mkdir -p ~/biped_locomotion_ws/src
   cd ~/biped_locomotion_ws
   ```

2. Create a package for our locomotion controller:
   ```bash
   cd src
   ros2 pkg create --build-type ament_python biped_controller
   ```

## Step 1: Create the Biped Robot Model

First, let's create a simple URDF model for our biped robot:

1. Create the URDF directory and file:
   ```bash
   mkdir -p biped_controller/urdf
   touch biped_controller/urdf/simple_biped.urdf
   ```

2. Add the following URDF content to `simple_biped.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_biped">
  <!-- Base/Floating body -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.3"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.4"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.5"/>
    </inertial>
  </link>

  <!-- Left Hip -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_thigh"/>
    <origin xyz="0 0.1 -0.2"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="3.0"/>
  </joint>

  <link name="left_thigh">
    <visual>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Left Knee -->
  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 0 1"/>
    <limit lower="0" upper="1.57" effort="100" velocity="3.0"/>
  </joint>

  <link name="left_shin">
    <visual>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
      <material name="yellow">
        <color rgba="1 1 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.08" ixy="0.0" ixz="0.0" iyy="0.08" iyz="0.0" izz="0.08"/>
    </inertial>
  </link>

  <!-- Left Foot -->
  <joint name="left_ankle_joint" type="revolute">
    <parent link="left_shin"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.785" upper="0.785" effort="100" velocity="3.0"/>
  </joint>

  <link name="left_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
      <material name="purple">
        <color rgba="1 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Right Hip -->
  <joint name="right_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_thigh"/>
    <origin xyz="0 -0.1 -0.2"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="3.0"/>
  </joint>

  <link name="right_thigh">
    <visual>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Right Knee -->
  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh"/>
    <child link="right_shin"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 0 1"/>
    <limit lower="0" upper="1.57" effort="100" velocity="3.0"/>
  </joint>

  <link name="right_shin">
    <visual>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
      <material name="yellow">
        <color rgba="1 1 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.08 0.08 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <inertia ixx="0.08" ixy="0.0" ixz="0.0" iyy="0.08" iyz="0.0" izz="0.08"/>
    </inertial>
  </link>

  <!-- Right Foot -->
  <joint name="right_ankle_joint" type="revolute">
    <parent link="right_shin"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.785" upper="0.785" effort="100" velocity="3.0"/>
  </joint>

  <link name="right_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
      <material name="purple">
        <color rgba="1 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>

  <!-- Gazebo plugin for control -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/simple_biped</robotNamespace>
    </plugin>
  </gazebo>

  <!-- Joint state publisher -->
  <gazebo>
    <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
      <robotNamespace>/simple_biped</robotNamespace>
      <jointName>left_hip_joint, left_knee_joint, left_ankle_joint, right_hip_joint, right_knee_joint, right_ankle_joint</jointName>
    </plugin>
  </gazebo>
</robot>
```

## Step 2: Create the ZMP Controller

Now, let's implement the ZMP-based balance controller:

1. Create the controller file `biped_controller/biped_zmp_controller.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Point
import numpy as np
import math
from collections import deque

class ZMPController(Node):
    """ZMP-based balance controller for bipedal robot"""

    def __init__(self):
        super().__init__('zmp_controller')

        # Robot parameters
        self.com_height = 0.7  # Center of mass height (m)
        self.gravity = 9.81    # Gravity (m/s^2)

        # Control parameters
        self.dt = 0.01  # Control timestep (s)
        self.zmp_tolerance = 0.05  # ZMP error tolerance (m)

        # Walking parameters
        self.step_length = 0.3  # Step length (m)
        self.step_height = 0.1  # Step height (m)
        self.step_duration = 1.0  # Step duration (s)

        # Internal state
        self.current_joint_positions = {}
        self.support_foot = 'left'  # Which foot is currently supporting
        self.walk_phase = 0.0  # Current phase in walking cycle (0.0 to 1.0)
        self.com_x = 0.0  # Current center of mass x position
        self.com_y = 0.0  # Current center of mass y position
        self.zmp_x = 0.0  # Current ZMP x position
        self.zmp_y = 0.0  # Current ZMP y position

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Publishers
        self.joint_command_pub = self.create_publisher(
            Float64MultiArray,
            '/joint_commands',
            10
        )

        self.zmp_pub = self.create_publisher(
            Point,
            '/zmp',
            10
        )

        # Timer for control loop
        self.control_timer = self.create_timer(self.dt, self.control_loop)

        self.get_logger().info('ZMP Controller initialized')

    def joint_state_callback(self, msg):
        """Update current joint positions"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.current_joint_positions[name] = msg.position[i]

    def calculate_zmp(self):
        """Calculate ZMP from current CoM position and acceleration"""
        # For simplicity, we'll use a basic ZMP calculation
        # ZMP_x = CoM_x - (CoM_height / gravity) * CoM_acc_x
        # ZMP_y = CoM_y - (CoM_height / gravity) * CoM_acc_y

        # In this simplified version, we'll estimate ZMP based on foot positions
        # and CoM position

        # For a statically stable biped, ZMP should be within the support polygon
        # which is typically the area between the feet

        if self.support_foot == 'left':
            # If left foot is supporting, ZMP should be near left foot
            zmp_y = -0.1  # Approximate left foot Y position
        else:
            # If right foot is supporting, ZMP should be near right foot
            zmp_y = 0.1   # Approximate right foot Y position

        return self.com_x, zmp_y

    def balance_control(self):
        """Simple balance control to keep ZMP within support polygon"""
        desired_zmp_x, desired_zmp_y = self.calculate_zmp()

        # Calculate errors
        zmp_error_x = desired_zmp_x - self.zmp_x
        zmp_error_y = desired_zmp_y - self.zmp_y

        # Simple PD control to adjust CoM position
        kp = 10.0  # Proportional gain
        kd = 2.0   # Derivative gain

        # Adjust joint angles to move CoM toward desired ZMP
        joint_adjustments = {}

        # Hip adjustments to control CoM position
        if abs(zmp_error_x) > self.zmp_tolerance:
            # Adjust hip joints to move CoM in X direction
            hip_adjustment = kp * zmp_error_x
            joint_adjustments['left_hip_joint'] = hip_adjustment
            joint_adjustments['right_hip_joint'] = hip_adjustment

        if abs(zmp_error_y) > self.zmp_tolerance:
            # Adjust hip joints to move CoM in Y direction
            left_hip_adj = kp * zmp_error_y * 0.5  # Different adjustment for each leg
            right_hip_adj = -kp * zmp_error_y * 0.5
            joint_adjustments['left_hip_joint'] = joint_adjustments.get('left_hip_joint', 0) + left_hip_adj
            joint_adjustments['right_hip_joint'] = joint_adjustments.get('right_hip_joint', 0) + right_hip_adj

        return joint_adjustments

    def walking_pattern_generator(self):
        """Generate walking pattern using simplified approach"""
        # Update walking phase
        self.walk_phase += self.dt / self.step_duration
        if self.walk_phase > 1.0:
            self.walk_phase = 0.0
            # Switch support foot
            self.support_foot = 'right' if self.support_foot == 'left' else 'left'

        # Calculate foot trajectory based on phase
        phase = self.walk_phase

        if self.support_foot == 'left':
            # Left foot is supporting, right foot is swinging
            # Generate swing trajectory for right foot
            if phase < 0.5:
                # Lift foot
                right_ankle_target = math.sin(phase * 2 * math.pi) * self.step_height
            else:
                # Lower foot
                right_ankle_target = math.sin(phase * 2 * math.pi) * self.step_height
        else:
            # Right foot is supporting, left foot is swinging
            # Generate swing trajectory for left foot
            if phase < 0.5:
                # Lift foot
                left_ankle_target = math.sin(phase * 2 * math.pi) * self.step_height
            else:
                # Lower foot
                left_ankle_target = math.sin(phase * 2 * math.pi) * self.step_height

        # Move CoM forward gradually
        self.com_x += (self.step_length / self.step_duration) * self.dt

        return {}

    def control_loop(self):
        """Main control loop"""
        # Calculate current ZMP
        self.zmp_x, self.zmp_y = self.calculate_zmp()

        # Publish current ZMP
        zmp_msg = Point()
        zmp_msg.x = self.zmp_x
        zmp_msg.y = self.zmp_y
        zmp_msg.z = 0.0  # ZMP is on ground plane
        self.zmp_pub.publish(zmp_msg)

        # Get balance adjustments
        balance_adjustments = self.balance_control()

        # Get walking pattern
        walking_adjustments = self.walking_pattern_generator()

        # Combine adjustments
        all_adjustments = balance_adjustments.copy()
        for joint, adjustment in walking_adjustments.items():
            all_adjustments[joint] = all_adjustments.get(joint, 0) + adjustment

        # Create joint command message
        joint_cmd = Float64MultiArray()

        # Default joint positions (standing pose)
        default_positions = {
            'left_hip_joint': 0.0,
            'left_knee_joint': 0.0,
            'left_ankle_joint': 0.0,
            'right_hip_joint': 0.0,
            'right_knee_joint': 0.0,
            'right_ankle_joint': 0.0
        }

        # Apply adjustments
        for joint, pos in default_positions.items():
            if joint in all_adjustments:
                default_positions[joint] += all_adjustments[joint]

        joint_cmd.data = [
            default_positions['left_hip_joint'],
            default_positions['left_knee_joint'],
            default_positions['left_ankle_joint'],
            default_positions['right_hip_joint'],
            default_positions['right_knee_joint'],
            default_positions['right_ankle_joint']
        ]

        self.joint_command_pub.publish(joint_cmd)

        self.get_logger().debug(f'ZMP: ({self.zmp_x:.3f}, {self.zmp_y:.3f}), CoM: ({self.com_x:.3f}, {self.com_y:.3f})')

def main(args=None):
    rclpy.init(args=args)
    controller = ZMPController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        pass
    finally:
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 3: Create a Gazebo Launch File

Create a launch file to start the simulation:

1. Create the launch directory and file:
   ```bash
   mkdir -p biped_controller/launch
   touch biped_controller/launch/biped_simulation.launch.py
   ```

2. Add the following content to the launch file:

```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Paths
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_biped_controller = FindPackageShare('biped_controller')

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gazebo.launch.py'])
        )
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'simple_biped',
            '-x', '0', '-y', '0', '-z', '1.0'  # Start slightly above ground
        ],
        output='screen'
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': open(
                PathJoinSubstitution([pkg_biped_controller, 'urdf', 'simple_biped.urdf'])
            ).read()
        }]
    )

    # Joint state publisher (for visualization)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'rate': 50.0
        }]
    )

    # Our ZMP controller
    zmp_controller = Node(
        package='biped_controller',
        executable='biped_zmp_controller',
        name='zmp_controller',
        parameters=[{
            'use_sim_time': use_sim_time
        }],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        zmp_controller
    ])
```

## Step 4: Create the Package Configuration

Update the package configuration files:

1. Update `biped_controller/setup.py`:

```python
from setuptools import setup
from glob import glob
import os

package_name = 'biped_controller'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='Biped locomotion controller using ZMP',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'biped_zmp_controller = biped_controller.biped_zmp_controller:main',
        ],
    },
)
```

2. Update `biped_controller/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>biped_controller</name>
  <version>0.1.0</version>
  <description>Biped locomotion controller using ZMP</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>launch</depend>
  <depend>launch_ros</depend>
  <depend>robot_state_publisher</depend>
  <depend>joint_state_publisher</depend>
  <depend>gazebo_ros</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

## Step 5: Test the Simulation

1. Build the package:
   ```bash
   cd ~/biped_locomotion_ws
   colcon build --packages-select biped_controller
   source install/setup.bash
   ```

2. Run the simulation:
   ```bash
   ros2 launch biped_controller biped_simulation.launch.py
   ```

## Step 6: Create a Simplified Simulation Alternative

If Gazebo is not available or you prefer a simpler approach, create a Python-based simulation:

1. Create `biped_simulation.py`:

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon
import time

class SimpleBipedSimulator:
    """Simple 2D biped simulation for understanding ZMP concepts"""

    def __init__(self):
        # Robot parameters
        self.com_height = 0.8  # Center of mass height (m)
        self.leg_length = 0.6  # Leg length (m)

        # Initial state
        self.com_x = 0.0
        self.com_y = 0.0
        self.left_foot_x = -0.1
        self.left_foot_y = -self.leg_length
        self.right_foot_x = 0.1
        self.right_foot_y = -self.leg_length

        # Walking parameters
        self.step_length = 0.3
        self.step_height = 0.1
        self.step_duration = 1.0
        self.dt = 0.02
        self.time = 0.0

        # Support polygon (area between feet)
        self.support_polygon = self.calculate_support_polygon()

        # Data for plotting
        self.com_trajectory = []
        self.zmp_trajectory = []

    def calculate_zmp(self):
        """Calculate ZMP (simplified - in this 2D case, ZMP is at foot if balanced)"""
        # For a statically stable biped, ZMP should be within the support polygon
        # In this simple model, we'll calculate it based on CoM position relative to feet

        # If both feet are on ground, ZMP is somewhere between them
        # If one foot is lifted, ZMP is under the supporting foot
        if self.time % (2 * self.step_duration) < self.step_duration:
            # Left foot support phase
            zmp_x = self.left_foot_x
            zmp_y = self.left_foot_y
        else:
            # Right foot support phase
            zmp_x = self.right_foot_x
            zmp_y = self.right_foot_y

        return zmp_x, zmp_y

    def calculate_support_polygon(self):
        """Calculate the support polygon (convex hull of contact points)"""
        # For a biped, support polygon is the area between the feet
        x_coords = [self.left_foot_x, self.right_foot_x]
        y_coords = [self.left_foot_y, self.right_foot_y]

        # Add some width to the feet
        vertices = [
            (self.left_foot_x - 0.05, self.left_foot_y - 0.02),
            (self.left_foot_x + 0.05, self.left_foot_y - 0.02),
            (self.right_foot_x + 0.05, self.right_foot_y - 0.02),
            (self.right_foot_x - 0.05, self.right_foot_y - 0.02)
        ]
        return vertices

    def step_simulation(self):
        """Advance the simulation by one time step"""
        self.time += self.dt

        # Simple walking pattern
        cycle_phase = (self.time % (2 * self.step_duration)) / self.step_duration

        if cycle_phase < 1.0:
            # Left foot support, right foot swing
            self.left_foot_x += (self.step_length / (2 * self.step_duration)) * self.dt
            # Right foot trajectory (circular arc for simplicity)
            swing_phase = cycle_phase
            self.right_foot_x = 0.1 + self.step_length * swing_phase
            self.right_foot_y = -self.leg_length + self.step_height * np.sin(np.pi * swing_phase)
        else:
            # Right foot support, left foot swing
            self.right_foot_x += (self.step_length / (2 * self.step_duration)) * self.dt
            # Left foot trajectory
            swing_phase = cycle_phase - 1.0
            self.left_foot_x = -0.1 + self.step_length * swing_phase
            self.left_foot_y = -self.leg_length + self.step_height * np.sin(np.pi * swing_phase)

        # Update CoM to follow feet approximately
        self.com_x = (self.left_foot_x + self.right_foot_x) / 2 + 0.1 * np.sin(2 * np.pi * self.time * 0.5)
        self.com_y = self.com_height

        # Calculate ZMP
        zmp_x, zmp_y = self.calculate_zmp()

        # Store trajectory data
        self.com_trajectory.append((self.com_x, self.com_y))
        self.zmp_trajectory.append((zmp_x, zmp_y))

        # Update support polygon
        self.support_polygon = self.calculate_support_polygon()

    def is_stable(self):
        """Check if the robot is stable (CoM projection is within support polygon)"""
        zmp_x, zmp_y = self.calculate_zmp()

        # Simple check: is CoM x between feet x positions?
        min_x = min(self.left_foot_x, self.right_foot_x)
        max_x = max(self.left_foot_x, self.right_foot_x)

        return min_x <= self.com_x <= max_x

def run_simulation():
    """Run the biped simulation with visualization"""
    sim = SimpleBipedSimulator()

    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-0.5, 1.0)
    ax.set_ylim(-0.8, 1.0)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title('Simple Biped Simulation - ZMP and Balance Control')

    # Initialize plot elements
    com_point, = ax.plot([], [], 'ro', markersize=10, label='CoM')
    zmp_point, = ax.plot([], [], 'bo', markersize=8, label='ZMP')
    robot_lines, = ax.plot([], [], 'k-', linewidth=2)
    support_polygon_patch = Polygon([], closed=True, alpha=0.3, color='green', label='Support Polygon')
    ax.add_patch(support_polygon_patch)

    # Trajectory lines
    com_traj_line, = ax.plot([], [], 'r--', alpha=0.5, label='CoM Trajectory')
    zmp_traj_line, = ax.plot([], [], 'b--', alpha=0.5, label='ZMP Trajectory')

    ax.legend()

    def animate(frame):
        # Run multiple simulation steps per frame for smoother animation
        for _ in range(5):
            sim.step_simulation()

        # Update robot visualization (simple stick figure)
        robot_x = [sim.left_foot_x, sim.com_x, sim.right_foot_x]  # feet and body
        robot_y = [sim.left_foot_y, sim.com_y, sim.right_foot_y]

        # Update plot elements
        com_point.set_data([sim.com_x], [sim.com_y])
        zmp_point.set_data([sim.zmp_trajectory[-1][0]], [sim.zmp_trajectory[-1][1]])
        robot_lines.set_data(robot_x, robot_y)

        # Update support polygon
        support_polygon_patch.set_xy(sim.support_polygon)

        # Update trajectories
        if len(sim.com_trajectory) > 1:
            com_x_traj, com_y_traj = zip(*sim.com_trajectory)
            com_traj_line.set_data(com_x_traj, com_y_traj)

        if len(sim.zmp_trajectory) > 1:
            zmp_x_traj, zmp_y_traj = zip(*sim.zmp_trajectory)
            zmp_traj_line.set_data(zmp_x_traj, zmp_y_traj)

        # Check stability and update title
        stable = sim.is_stable()
        status = "STABLE" if stable else "UNSTABLE"
        ax.set_title(f'Simple Biped Simulation - ZMP and Balance Control - Status: {status}')

        # Change color based on stability
        robot_lines.set_color('green' if stable else 'red')

        return com_point, zmp_point, robot_lines, support_polygon_patch, com_traj_line, zmp_traj_line

    # Create animation
    ani = animation.FuncAnimation(fig, animate, frames=1000, interval=50, blit=True)

    plt.show()

    return sim

def main():
    print("Starting biped simulation...")
    print("Red circle: Center of Mass (CoM)")
    print("Blue circle: Zero Moment Point (ZMP)")
    print("Green area: Support polygon")
    print("Robot is stable when CoM projection is within support polygon")

    sim = run_simulation()
    print("Simulation completed.")

if __name__ == "__main__":
    main()
```

## Step 7: Test the Simulation

1. Run the simplified simulation:
   ```bash
   python biped_simulation.py
   ```

## Step 8: Extend the Implementation

Try extending the basic implementation with additional features:

1. Implement a more sophisticated ZMP controller using Model Predictive Control (MPC) concepts
2. Add disturbance rejection to the balance controller
3. Implement a more realistic walking pattern with double support phases
4. Add visualization of the ZMP error and stability margins

## Verification

To verify your implementation:

1. Confirm that the robot model loads correctly in Gazebo
2. Verify that the ZMP calculation is mathematically correct
3. Check that the walking pattern generator produces stable gaits
4. Ensure that the balance controller maintains stability during walking
5. Validate that the ZMP remains within the support polygon during stable phases

## Troubleshooting

- If the robot falls over immediately, check the initial pose and CoM height
- If ZMP calculations are incorrect, verify the physics model and force calculations
- If walking is unstable, adjust the control gains or step parameters
- If simulation runs too slowly, reduce the control frequency or simplify calculations

## Next Steps

In the next lab, you'll integrate all the concepts learned in this module into a complete VLA system that connects high-level instructions to humanoid robot behaviors, incorporating perception, planning, and control in a unified pipeline.