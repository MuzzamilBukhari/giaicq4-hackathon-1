---
title: Chapter 2 - Unity for Robotics
sidebar_position: 2
description: Learn how to set up Unity Robotics Hub, import URDF models, visualize ROS data in real-time, and establish ROS-Unity communication.
---

# Chapter 2: Unity for Robotics

## Overview

This chapter introduces Unity as a powerful visualization platform for robotics applications. You'll learn how to set up Unity Robotics Hub, import robot models from URDF, visualize ROS data in real-time, and establish communication between ROS 2 and Unity using TCP/UDP bridges.

## Learning Objectives

By the end of this chapter, you will be able to:
- Install and configure Unity Robotics Hub
- Import robot models using the URDF importer pipeline
- Visualize real-time ROS data within Unity
- Establish and manage ROS-Unity communication via TCP/UDP bridges
- Create immersive visualization experiences for robotics applications

## 2.1 Unity Robotics Hub Setup

Unity Robotics Hub is a collection of tools, samples, and documentation that enables robotics developers to leverage Unity's real-time 3D capabilities for simulation, visualization, and testing.

### Prerequisites

Before installing Unity Robotics Hub, ensure you have:

1. **Unity Hub**: Download and install from [Unity's official website](https://unity.com/)
2. **Unity Editor**: Version 2021.3 LTS or later recommended
3. **Git LFS**: For handling large binary files in Unity packages
4. **ROS 2**: Installed and properly configured (Humble Hawksbill recommended)

### Installation Steps

1. **Install Git LFS** (if not already installed):
   ```bash
   git lfs install
   ```

2. **Clone Unity Robotics Hub**:
   ```bash
   git clone https://github.com/Unity-Technologies/Unity-Robotics-Hub.git
   cd Unity-Robotics-Hub
   git lfs pull
   ```

3. **Open Unity Project**: Launch Unity Hub and open the `Unity-Robotics-Hub` folder as a Unity project.

4. **Install Required Packages**: Through Unity's Package Manager, install:
   - ROS-TCP-Connector
   - ROS-TCP-Endpoint
   - Unity-Robotics-Visualization

### Unity Robotics Package Manager

Unity Robotics provides several packages that facilitate ROS integration:

- **ROS-TCP-Connector**: Enables communication between Unity and ROS
- **ROS-TCP-Endpoint**: Provides a bridge for ROS communication
- **Unity-Robotics-Visualization**: Tools for visualizing robotics data in Unity

## 2.2 URDF Import Pipeline

The URDF Importer is a Unity package that allows you to import robot models defined in URDF (Unified Robot Description Format) directly into Unity.

### Installation

1. In Unity, go to **Window** → **Package Manager**
2. Click the **+** button → **Add package from git URL...**
3. Enter: `https://github.com/Unity-Technologies/URDF-Importer.git?path=/com.unity.robotics.urdf-importer#v0.5.2`

### Import Process

1. **Prepare URDF Files**: Ensure your URDF files have proper mesh references and are organized in a standard ROS package structure.

2. **Import Robot**:
   - Create a new scene or use an existing one
   - Go to **Robotics** → **Import URDF**
   - Select your URDF file
   - The importer will automatically create the robot hierarchy in Unity

### URDF Import Configuration

The URDF Importer supports various configuration options:

- **Invert Axis**: Adjust coordinate system differences between ROS and Unity
- **Import Collision as Visual**: Use collision geometry for visualization when visual meshes are unavailable
- **Merge Links**: Combine multiple URDF links into single Unity objects for performance
- **Import Inertial**: Import inertial properties (for physics simulation)

### Example URDF Structure for Unity

For optimal import results, structure your URDF with Unity in mind:

```xml
<?xml version="1.0"?>
<robot name="unity_robot">
  <!-- Base link with visual and collision -->
  <link name="base_link">
    <visual>
      <geometry>
        <mesh filename="package://robot_description/meshes/base_link.stl"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="package://robot_description/meshes/base_link_collision.stl"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Joint with proper limits -->
  <joint name="joint_1" type="revolute">
    <parent link="base_link"/>
    <child link="link_1"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="link_1">
    <visual>
      <geometry>
        <mesh filename="package://robot_description/meshes/link_1.stl"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <mesh filename="package://robot_description/meshes/link_1_collision.stl"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05"/>
    </inertial>
  </link>
</robot>
```

## 2.3 Real-time Visualization of ROS Data

Unity can visualize various types of ROS data in real-time, including sensor data, robot states, and simulation information.

### Sensor Data Visualization

Unity can visualize different types of sensor data:

1. **Camera Data**: RGB, depth, and semantic segmentation images
2. **LiDAR Data**: Point clouds and laser scan visualizations
3. **IMU Data**: Orientation and acceleration information
4. **Joint States**: Real-time joint position visualization

### Setting up ROS Communication in Unity

1. **Add ROS Connection Component**: Attach the `ROSConnection` component to a GameObject in your scene.

2. **Configure Connection Settings**:
   ```csharp
   public class UnityRobotController : MonoBehaviour
   {
       public string rosIPAddress = "127.0.0.1";
       public int rosPort = 10000;

       ROSConnection ros;

       void Start()
       {
           ros = ROSConnection.GetOrCreateInstance();
           ros.rosIPAddress = rosIPAddress;
           ros.rosPort = rosPort;
       }
   }
   ```

3. **Subscribe to ROS Topics**: Use Unity's ROS-TCP-Connector to subscribe to ROS topics and update Unity objects accordingly.

### Example: Visualizing Joint States

Here's an example of how to visualize joint states in Unity:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Sensor;

public class JointStateSubscriber : MonoBehaviour
{
    [SerializeField] private List<ArticulationBody> jointArticulationBodies = new List<ArticulationBody>();
    [SerializeField] private string topicName = "/joint_states";

    private ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<sensor_msgs.JointState>(topicName, OnJointStateReceived);
    }

    void OnJointStateReceived(sensor_msgs.JointState jointState)
    {
        for (int i = 0; i < jointState.name.Count && i < jointArticulationBodies.Count; i++)
        {
            if (jointState.position.Count > i)
            {
                ArticulationBody body = jointArticulationBodies[i];
                ArticulationDrive drive = body.xDrive;
                drive.target = Mathf.Rad2Deg * (float)jointState.position[i];
                body.xDrive = drive;
            }
        }
    }
}
```

### Visualization Techniques

Unity offers several visualization techniques for robotics data:

1. **Point Cloud Visualization**: Convert ROS PointCloud2 messages to Unity particle systems
2. **Path Visualization**: Visualize planned paths using Unity line renderers
3. **Sensor Range Visualization**: Show sensor fields of view and ranges
4. **Trajectory Tracking**: Display robot movement history

## 2.4 ROS-Unity TCP/UDP Bridge Basics

The communication between ROS and Unity is typically handled through TCP or UDP bridges that convert ROS messages to Unity-compatible formats.

### TCP Bridge Architecture

The typical architecture includes:

1. **ROS TCP Endpoint**: A ROS node that acts as a server to receive and send messages
2. **Unity TCP Connector**: A Unity component that connects to the ROS endpoint
3. **Message Translation**: Conversion between ROS message formats and Unity data structures

### Setting up TCP Communication

1. **Launch ROS TCP Endpoint**:
   ```bash
   roslaunch unity_robotics_demo tcp_endpoint.launch.py
   ```

2. **Configure Unity Connection**: Set the IP address and port in Unity's ROSConnection component

3. **Publish and Subscribe**: Use Unity scripts to publish to ROS topics and subscribe to them

### Example Communication Flow

Here's a complete example of bidirectional communication:

**ROS Side (Python)**:
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String

class UnityBridgeNode(Node):
    def __init__(self):
        super().__init__('unity_bridge_node')

        # Publisher for Unity commands
        self.unity_cmd_pub = self.create_publisher(String, '/unity_commands', 10)

        # Subscriber for joint states from Unity
        self.joint_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_callback, 10)

        # Timer for sending commands to Unity
        self.timer = self.create_timer(0.1, self.timer_callback)

    def joint_callback(self, msg):
        # Process joint states from Unity
        self.get_logger().info(f'Received joint states: {len(msg.name)} joints')

    def timer_callback(self):
        # Send commands to Unity
        cmd_msg = String()
        cmd_msg.data = "Hello Unity!"
        self.unity_cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    node = UnityBridgeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Unity Side (C#)**:
```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Std_msgs;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Sensor;

public class UnityROSBridge : MonoBehaviour
{
    ROSConnection ros;
    string unityCommandsTopic = "/unity_commands";
    string jointStatesTopic = "/joint_states";

    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<StringMsg>(unityCommandsTopic, OnUnityCommandReceived);
    }

    void Update()
    {
        // Publish joint states periodically
        PublishJointStates();
    }

    void OnUnityCommandReceived(StringMsg msg)
    {
        Debug.Log("Received from ROS: " + msg.data);
    }

    void PublishJointStates()
    {
        var jointState = new sensor_msgs.JointState()
        {
            name = new List<string> { "joint1", "joint2" },
            position = new List<double> { 0.0, 0.0 }
        };

        ros.Publish(jointStatesTopic, jointState);
    }
}
```

### UDP Communication (Alternative)

For real-time applications where lower latency is critical, UDP can be used:

- **Advantages**: Lower latency, no connection overhead
- **Disadvantages**: No guaranteed delivery, potential packet loss
- **Use Cases**: Real-time visualization, control commands with high frequency

## Summary

This chapter covered the fundamentals of integrating Unity with ROS for robotics visualization. You learned how to set up Unity Robotics Hub, import URDF models, visualize ROS data in real-time, and establish communication bridges between ROS and Unity. These capabilities enable powerful visualization and simulation environments for robotics development.

## Next Steps

In the next chapter, we'll explore sim-to-real transfer techniques, including domain randomization and sensor calibration, which are crucial for bridging the gap between simulation and real-world robotics applications.

## External Resources

- [Unity Robotics Hub Documentation](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
- [ROS-TCP-Connector Documentation](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [URDF Importer Documentation](https://github.com/Unity-Technologies/URDF-Importer)
- [Unity Robotics Visualization](https://github.com/Unity-Technologies/Unity-Robotics-Visualization)