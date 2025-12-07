---
title: Chapter 2 Lab - Unity ROS Visualization
sidebar_position: 3
description: Lab exercise to visualize ROS 2 robot movement in Unity using a URDF prefab and establish ROS-Unity communication.
---

# Chapter 2 Lab: Unity ROS Visualization

## Objective

In this lab, you will learn how to visualize ROS 2 robot movement in Unity using a URDF prefab and establish communication between ROS 2 and Unity. This hands-on exercise will help you understand the Unity Robotics Hub setup, URDF import process, and real-time ROS data visualization.

## Prerequisites

- Ubuntu 22.04 with ROS 2 Humble installed
- Unity Hub and Unity Editor (2021.3 LTS or later) installed
- Unity Robotics Hub packages installed
- Completion of Chapter 1 and 2 theory content
- Basic understanding of C# programming for Unity

## Estimated Time

90-120 minutes

## Lab Setup

### Step 1: Install Unity Robotics Hub

If you haven't already, install Unity Robotics Hub:

1. Download and install Unity Hub from [Unity's website](https://unity.com/)
2. Install Unity Editor 2021.3 LTS or later
3. Clone the Unity Robotics Hub repository:

```bash
git clone https://github.com/Unity-Technologies/Unity-Robotics-Hub.git
cd Unity-Robotics-Hub
git lfs install
git lfs pull
```

### Step 2: Create ROS 2 Workspace

Create a new ROS 2 workspace for this lab:

```bash
mkdir -p ~/unity_robot_ws/src
cd ~/unity_robot_ws
colcon build
source install/setup.bash
```

### Step 3: Create Simple Robot Package

Create a simple robot package with URDF files:

```bash
cd ~/unity_robot_ws/src
ros2 pkg create --build-type ament_cmake unity_robot_description
```

Create the URDF directory structure:

```bash
mkdir -p ~/unity_robot_ws/src/unity_robot_description/urdf
mkdir -p ~/unity_robot_ws/src/unity_robot_description/meshes
```

## Lab Exercises

### Exercise 1: Create Robot URDF Model

In this exercise, you'll create a simple robot model in URDF format that can be imported into Unity.

#### Step 1: Create Robot URDF

Create `~/unity_robot_ws/src/unity_robot_description/urdf/simple_arm.urdf`:

```xml
<?xml version="1.0"?>
<robot name="simple_arm">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.2" radius="0.15"/>
      </geometry>
      <material name="blue">
        <color rgba="0.1 0.1 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.2" radius="0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- First link (shoulder) -->
  <link name="shoulder_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.3"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0.1 0.1 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Second link (elbow) -->
  <link name="elbow_link">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.25"/>
      </geometry>
      <material name="green">
        <color rgba="0.1 0.8 0.1 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.1 0.1 0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.4"/>
      <inertia ixx="0.004" ixy="0.0" ixz="0.0" iyy="0.004" iyz="0.0" izz="0.004"/>
    </inertial>
  </link>

  <!-- Third link (wrist) -->
  <link name="wrist_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.05"/>
      </geometry>
      <material name="yellow">
        <color rgba="0.8 0.8 0.1 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.1" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="base_to_shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <joint name="shoulder_to_elbow" type="revolute">
    <parent link="shoulder_link"/>
    <child link="elbow_link"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <joint name="elbow_to_wrist" type="revolute">
    <parent link="elbow_link"/>
    <child link="wrist_link"/>
    <origin xyz="0 0 0.15" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Gazebo plugins -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
  </gazebo>

  <gazebo reference="shoulder_link">
    <material>Gazebo/Red</material>
  </gazebo>

  <gazebo reference="elbow_link">
    <material>Gazebo/Green</material>
  </gazebo>

  <gazebo reference="wrist_link">
    <material>Gazebo/Yellow</material>
  </gazebo>
</robot>
```

#### Step 2: Create Robot Launch File

Create `~/unity_robot_ws/src/unity_robot_description/launch/display.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the package share directory
    pkg_share = get_package_share_directory('unity_robot_description')

    # URDF path
    urdf_path = os.path.join(pkg_share, 'urdf', 'simple_arm.urdf')

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': open(urdf_path).read()
        }]
    )

    # Joint State Publisher (GUI)
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # RViz2 for visualization
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'display.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path] if os.path.exists(rviz_config_path) else []
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        # rviz_node  # Commented out for Unity visualization
    ])
```

#### Step 3: Create Package Configuration

Update the package.xml file:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>unity_robot_description</name>
  <version>0.0.0</version>
  <description>Simple robot description for Unity ROS visualization lab</description>
  <maintainer email="user@todo.todo">user</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>xacro</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### Exercise 2: Import Robot into Unity

Now you'll import the robot model into Unity using the URDF Importer.

#### Step 1: Set up Unity Project

1. Open Unity Hub
2. Create a new 3D project or open the Unity-Robotics-Hub project
3. If creating a new project, install the required packages:
   - Go to **Window** → **Package Manager**
   - Install **ROS-TCP-Connector** via git URL: `https://github.com/Unity-Technologies/ROS-TCP-Connector.git`
   - Install **URDF Importer** via git URL: `https://github.com/Unity-Technologies/URDF-Importer.git?path=/com.unity.robotics.urdf-importer#v0.5.2`

#### Step 2: Prepare URDF for Import

Copy your URDF file to the Unity project:

1. In your Unity project, create an `Assets/URDF` folder
2. Copy the `simple_arm.urdf` file to this folder
3. Create a `meshes` folder in the same location (you can create simple placeholder files for now)

#### Step 3: Import Robot

1. In Unity, go to **Robotics** → **Import URDF**
2. Select your `simple_arm.urdf` file
3. Configure import settings:
   - Check "Import collision as visual" if you don't have collision meshes
   - Set appropriate axis conversion if needed
4. Click "Import"

The robot should now appear in your Unity scene with the proper joint hierarchy.

### Exercise 3: Create ROS-Unity Communication

In this exercise, you'll create a Unity script that communicates with ROS 2 to visualize robot movement.

#### Step 1: Create Unity ROS Communication Script

Create a new C# script in Unity called `RobotJointController.cs`:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Sensor;
using Unity.Robotics.ROSTCPConnector.MessageTypes.Std_msgs;

public class RobotJointController : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosIPAddress = "127.0.0.1";
    public int rosPort = 10000;

    [Header("Joint Configuration")]
    public List<ArticulationBody> jointArticulationBodies = new List<ArticulationBody>();
    public List<string> jointNames = new List<string>();

    [Header("ROS Topics")]
    public string jointStateTopic = "/joint_states";
    public string commandTopic = "/unity_robot_command";

    private ROSConnection ros;
    private bool isInitialized = false;

    void Start()
    {
        InitializeROSConnection();
        SubscribeToJointStates();
    }

    void InitializeROSConnection()
    {
        ros = ROSConnection.GetOrCreateInstance();
        ros.rosIPAddress = rosIPAddress;
        ros.rosPort = rosPort;
        isInitialized = true;
    }

    void SubscribeToJointStates()
    {
        ros.Subscribe<sensor_msgs.JointState>(jointStateTopic, OnJointStateReceived);
    }

    void OnJointStateReceived(sensor_msgs.JointState jointState)
    {
        if (!isInitialized) return;

        // Update each joint based on received joint states
        for (int i = 0; i < jointNames.Count; i++)
        {
            string jointName = jointNames[i];
            int jointIndex = jointState.name.IndexOf(jointName);

            if (jointIndex != -1 && jointIndex < jointState.position.Count)
            {
                // Convert radians to degrees for Unity ArticulationBody
                float targetAngle = Mathf.Rad2Deg * (float)jointState.position[jointIndex];

                if (i < jointArticulationBodies.Count)
                {
                    ArticulationBody jointBody = jointArticulationBodies[i];
                    ArticulationDrive drive = jointBody.xDrive;
                    drive.target = targetAngle;
                    jointBody.xDrive = drive;
                }
            }
        }
    }

    // Method to publish joint commands (optional)
    public void PublishJointCommand(string jointName, double position)
    {
        if (!isInitialized) return;

        var jointState = new sensor_msgs.JointState();
        jointState.name.Add(jointName);
        jointState.position.Add(position);
        jointState.header.stamp = new builtin_interfaces.Time();

        ros.Publish(jointStateTopic + "_out", jointState);
    }

    // Example method to send a command to ROS
    public void SendCommandToROS(string command)
    {
        if (!isInitialized) return;

        var stringMsg = new StringMsg();
        stringMsg.data = command;

        ros.Publish(commandTopic, stringMsg);
    }
}
```

#### Step 2: Set up Unity Scene

1. Create a new scene in Unity
2. Add the robot model to the scene
3. Select the robot root GameObject
4. Attach the `RobotJointController.cs` script to it
5. In the Inspector, configure:
   - Set `rosIPAddress` to "127.0.0.1"
   - Set `rosPort` to 10000
   - Set `jointStateTopic` to "/joint_states"
   - Set `commandTopic` to "/unity_robot_command"
   - Add the joint articulation bodies to the list in the same order as in your URDF
   - Add the corresponding joint names to the `jointNames` list

### Exercise 4: Test ROS-Unity Communication

Now you'll test the communication between ROS 2 and Unity.

#### Step 1: Build and Run ROS TCP Endpoint

First, build your ROS 2 workspace:

```bash
cd ~/unity_robot_ws
colcon build --packages-select unity_robot_description
source install/setup.bash
```

Launch the robot state publisher:

```bash
ros2 launch unity_robot_description display.launch.py
```

In another terminal, start the ROS TCP endpoint:

```bash
source ~/unity_robot_ws/install/setup.bash
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:="127.0.0.1" -p ROS_TCP_PORT:="10000"
```

#### Step 2: Run Unity Scene

1. In Unity, make sure your scene is set up with the robot and the `RobotJointController` script
2. Press Play in the Unity Editor
3. The Unity scene should connect to the ROS endpoint

#### Step 3: Test Joint State Visualization

In a new terminal, publish joint states to see the robot move in Unity:

```bash
source ~/unity_robot_ws/install/setup.bash
ros2 topic pub /joint_states sensor_msgs/JointState "{
  name: ['base_to_shoulder', 'shoulder_to_elbow', 'elbow_to_wrist'],
  position: [0.5, -0.3, 0.8],
  velocity: [],
  effort: []
}"
```

You should see the robot arm in Unity move according to the joint positions you published.

#### Step 4: Create Joint State Publisher Node

Create a more sophisticated ROS node to publish changing joint states. Create `~/unity_robot_ws/src/unity_robot_description/ros_nodes/unity_robot_controller.py`:

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import math
import time

class UnityRobotController(Node):
    def __init__(self):
        super().__init__('unity_robot_controller')

        # Publisher for joint states
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

        # Subscriber for Unity commands
        self.unity_sub = self.create_subscription(
            String, '/unity_robot_command', self.unity_command_callback, 10)

        # Timer for publishing joint states
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Initialize joint values
        self.joint_names = ['base_to_shoulder', 'shoulder_to_elbow', 'elbow_to_wrist']
        self.joint_positions = [0.0, 0.0, 0.0]
        self.time_offset = time.time()

        self.get_logger().info('Unity Robot Controller node started')

    def timer_callback(self):
        # Create joint state message
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_positions

        # Create a simple oscillating motion for demonstration
        current_time = time.time() - self.time_offset
        self.joint_positions[0] = 0.5 * math.sin(current_time * 0.5)  # Shoulder
        self.joint_positions[1] = 0.3 * math.sin(current_time * 0.3)  # Elbow
        self.joint_positions[2] = 0.4 * math.sin(current_time * 0.7)  # Wrist

        msg.position = self.joint_positions
        self.joint_pub.publish(msg)

    def unity_command_callback(self, msg):
        self.get_logger().info(f'Received command from Unity: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = UnityRobotController()

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

Make the script executable and add it to the package:

```bash
chmod +x ~/unity_robot_ws/src/unity_robot_description/ros_nodes/unity_robot_controller.py

# Add to setup.py or CMakeLists.txt to include the script
```

Update the package.xml to include the Python node:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>unity_robot_description</name>
  <version>0.0.0</version>
  <description>Simple robot description for Unity ROS visualization lab</description>
  <maintainer email="user@todo.todo">user</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>xacro</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

## Verification Checks

Complete the following verification steps to ensure you've successfully completed the lab:

### Verification 1: URDF Import
- [ ] Robot model successfully imported into Unity
- [ ] Joint hierarchy properly maintained
- [ ] Visual materials applied correctly

### Verification 2: ROS-Unity Connection
- [ ] Unity connects to ROS TCP endpoint successfully
- [ ] Connection status shows as established
- [ ] No connection errors in Unity console

### Verification 3: Joint State Visualization
- [ ] Robot joints move in Unity when joint states are published
- [ ] Joint movements correspond to published values
- [ ] Smooth and responsive visualization

### Verification 4: Bidirectional Communication
- [ ] Unity can receive joint state messages from ROS
- [ ] Unity can send command messages to ROS
- [ ] Communication is stable and reliable

## Expected Results

After completing this lab, you should have:

1. Successfully imported a URDF robot model into Unity
2. Established communication between ROS 2 and Unity
3. Visualized real-time robot joint movements in Unity
4. Demonstrated bidirectional communication between the systems
5. Created a functional Unity scene that responds to ROS joint state messages

## Troubleshooting

### Common Issues

**Unity cannot connect to ROS:**
- Check that the ROS TCP endpoint is running
- Verify IP address and port match between ROS and Unity
- Ensure firewall is not blocking the connection
- Check that both systems are on the same network

**Robot joints don't move in Unity:**
- Verify that joint names match between ROS and Unity
- Check that ArticulationBody components are properly assigned
- Confirm that joint position values are being received correctly

**URDF import fails:**
- Check that URDF file is properly formatted
- Ensure mesh files are accessible (create placeholder files if needed)
- Verify that Unity URDF Importer package is installed

**Performance issues:**
- Reduce the complexity of visual meshes
- Use fewer ArticulationBody components if possible
- Consider using simplified collision meshes

## Summary

This lab provided hands-on experience with Unity-ROS integration for robotics visualization. You learned how to import URDF models into Unity, establish communication between ROS 2 and Unity, and visualize real-time robot movements. These skills enable powerful visualization capabilities for robotics development and testing.

## Next Steps

In the next chapter, you'll learn about sim-to-real transfer techniques, including domain randomization and sensor calibration, which are essential for bridging the gap between simulation and real-world robotics applications.