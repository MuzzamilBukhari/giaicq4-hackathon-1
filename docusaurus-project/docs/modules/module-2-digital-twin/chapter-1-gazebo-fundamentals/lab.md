---
title: Chapter 1 Lab - Gazebo Robot Simulation
sidebar_position: 2
description: Lab exercise to spawn a robot in Gazebo, inspect joint states, and simulate collisions.
---

# Chapter 1 Lab: Gazebo Robot Simulation

## Objective

In this lab, you will learn how to spawn a robot in Gazebo, inspect joint states, and simulate collisions. This hands-on exercise will help you understand the fundamentals of Gazebo simulation and how to interact with simulated robots.

## Prerequisites

- Ubuntu 22.04 with ROS 2 Humble installed
- Gazebo Classic installed
- Basic understanding of ROS 2 concepts (topics, messages)
- Completion of Chapter 1 theory content

## Estimated Time

60-90 minutes

## Lab Setup

### Step 1: Verify Installation

First, ensure that Gazebo is properly installed and working:

```bash
gazebo --version
```

You should see the version information for Gazebo Classic.

### Step 2: Create Workspace

Create a new ROS 2 workspace for this lab:

```bash
mkdir -p ~/gazebo_lab_ws/src
cd ~/gazebo_lab_ws
colcon build
source install/setup.bash
```

### Step 3: Launch Gazebo

Start Gazebo with an empty world:

```bash
gazebo
```

## Lab Exercises

### Exercise 1: Spawn a Simple Robot Model

In this exercise, you'll spawn a simple robot model in Gazebo and observe its behavior.

#### Step 1: Create Robot Description

Create a simple URDF file for a wheeled robot:

```bash
mkdir -p ~/gazebo_lab_ws/src/gazebo_lab/config
```

Create `~/gazebo_lab_ws/src/gazebo_lab/config/simple_robot.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Left wheel -->
  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
      <origin rpy="1.5708 0 0"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
      <origin rpy="1.5708 0 0"/>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Right wheel -->
  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
      <origin rpy="1.5708 0 0"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
      <origin rpy="1.5708 0 0"/>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="-0.2 0.2 -0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="-0.2 -0.2 -0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <!-- Gazebo plugins -->
  <gazebo reference="base_link">
    <material>Gazebo/Grey</material>
  </gazebo>

  <gazebo reference="left_wheel">
    <material>Gazebo/Black</material>
  </gazebo>

  <gazebo reference="right_wheel">
    <material>Gazebo/Black</material>
  </gazebo>
</robot>
```

#### Step 2: Create Launch Script

Create a launch script to spawn the robot in Gazebo:

```bash
mkdir -p ~/gazebo_lab_ws/src/gazebo_lab/launch
```

Create `~/gazebo_lab_ws/src/gazebo_lab/launch/spawn_robot.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package share directory
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_gazebo_lab = get_package_share_directory('gazebo_lab')

    # Get URDF file path
    urdf_path = os.path.join(pkg_gazebo_lab, 'config', 'simple_robot.urdf')

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        )
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', urdf_path,
            '-entity', 'simple_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0.5'
        ],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_path).read()
        }]
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
        robot_state_publisher
    ])
```

### Exercise 2: Inspect Joint States

Now you'll learn how to inspect the joint states of your robot in Gazebo.

#### Step 1: Launch the Robot

First, build your workspace:

```bash
cd ~/gazebo_lab_ws
colcon build --packages-select gazebo_lab
source install/setup.bash
```

Launch the robot:

```bash
ros2 launch gazebo_lab spawn_robot.launch.py
```

#### Step 2: Check Joint States Topic

In a new terminal, check the available topics:

```bash
source ~/gazebo_lab_ws/install/setup.bash
ros2 topic list | grep joint
```

You should see a topic like `/joint_states`.

#### Step 3: Monitor Joint States

Monitor the joint states in real-time:

```bash
ros2 topic echo /joint_states
```

Observe the joint positions, velocities, and efforts for the left and right wheels. You should see the values change as the robot moves in Gazebo.

#### Step 4: Use Joint State Publisher GUI

Install and use the joint state publisher GUI to manually control joints:

```bash
sudo apt install ros-humble-joint-state-publisher-gui
```

Launch the GUI:

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

This will allow you to manually adjust joint positions and see the robot move in Gazebo.

### Exercise 3: Simulate Collisions

In this exercise, you'll set up scenarios to observe collision detection and response.

#### Step 1: Create Obstacle World

Create a simple world file with obstacles:

Create `~/gazebo_lab_ws/src/gazebo_lab/config/obstacle_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="obstacle_world">
    <!-- Physics -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
    </physics>

    <!-- Sun -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Ground -->
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
              <size>100 100</size>
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

    <!-- Obstacle 1 -->
    <model name="obstacle_1">
      <pose>2 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.2 0.2 1</ambient>
            <diffuse>0.8 0.2 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>10.0</mass>
          <inertia>
            <ixx>1.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>1.0</iyy>
            <iyz>0.0</iyz>
            <izz>1.0</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Obstacle 2 -->
    <model name="obstacle_2">
      <pose>-2 1 0.3 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <length>0.6</length>
              <radius>0.3</radius>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <length>0.6</length>
              <radius>0.3</radius>
            </cylinder>
          </geometry>
          <material>
            <ambient>0.2 0.8 0.2 1</ambient>
            <diffuse>0.2 0.8 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>10.0</mass>
          <inertia>
            <ixx>1.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>1.0</iyy>
            <iyz>0.0</iyz>
            <izz>1.0</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

#### Step 2: Create Collision Test Launch

Create a launch file that loads the obstacle world:

Create `~/gazebo_lab_ws/src/gazebo_lab/launch/collision_test.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package share directory
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_gazebo_lab = get_package_share_directory('gazebo_lab')

    # Get URDF file path
    urdf_path = os.path.join(pkg_gazebo_lab, 'config', 'simple_robot.urdf')
    world_path = os.path.join(pkg_gazebo_lab, 'config', 'obstacle_world.sdf')

    # Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_path
        }.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', urdf_path,
            '-entity', 'simple_robot',
            '-x', '0',
            '-y', '0',
            '-z', '0.5'
        ],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_path).read()
        }]
    )

    return LaunchDescription([
        gazebo,
        spawn_entity,
        robot_state_publisher
    ])
```

#### Step 3: Test Collisions

Build and launch the collision test:

```bash
cd ~/gazebo_lab_ws
colcon build --packages-select gazebo_lab
source install/setup.bash
ros2 launch gazebo_lab collision_test.launch.py
```

Use the joint state publisher GUI to move the robot's joints and observe how it interacts with the obstacles. Notice how the physics engine handles collisions and prevents the robot from passing through solid objects.

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: Robot Spawning
- [ ] Robot model appears in Gazebo simulation
- [ ] Robot maintains proper pose and orientation
- [ ] All visual elements display correctly

### Verification 2: Joint States Inspection
- [ ] `/joint_states` topic is available
- [ ] Joint position, velocity, and effort values update in real-time
- [ ] Joint names match those defined in the URDF file

### Verification 3: Collision Detection
- [ ] Robot collides with obstacles instead of passing through them
- [ ] Physics simulation behaves realistically
- [ ] Robot movement is constrained by collision boundaries

## Expected Results

After completing this lab, you should have:

1. Successfully spawned a custom robot model in Gazebo
2. Observed and monitored joint states through ROS 2 topics
3. Witnessed realistic collision detection and response in the simulation
4. Gained hands-on experience with Gazebo's physics engine

## Troubleshooting

### Common Issues

**Robot doesn't appear in Gazebo:**
- Check that the URDF file path is correct
- Verify that the package was built successfully
- Ensure Gazebo plugins are properly defined in the URDF

**Joint states topic not available:**
- Verify that robot_state_publisher is running
- Check that the URDF contains proper joint definitions
- Confirm that spawn_entity node executed successfully

**No collision response:**
- Ensure collision geometries are defined in the URDF
- Check that physics parameters are properly configured
- Verify that objects have appropriate mass and inertial properties

## Summary

This lab provided hands-on experience with Gazebo simulation fundamentals. You learned how to create and spawn robot models, inspect joint states, and observe collision dynamics. These skills form the foundation for more advanced simulation scenarios in robotics development.

## Next Steps

In the next chapter, you'll learn how to integrate Unity with ROS 2 for enhanced visualization capabilities.