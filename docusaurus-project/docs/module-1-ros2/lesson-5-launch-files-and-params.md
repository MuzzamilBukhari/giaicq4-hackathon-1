---
sidebar_position: 6
sidebar_label: "Launch Files & Parameter Management"
id: module-1-ros2-launch-files-params
---

# Lesson 5: Launch Files & Parameter Management

## Learning Objectives

- Understand the role of ROS 2 launch files in orchestrating multiple nodes and processes.
- Learn to compose complex robotic systems using Python launch files.
- Comprehend how to pass parameters to nodes and remap topic/service names.
- Be able to integrate existing URDF models and `rclpy` nodes within a single launch file.

## Introduction

As ROS 2 systems grow in complexity, manually starting each node and setting up configurations becomes cumbersome and error-prone. **Launch files** provide a structured way to define and manage the startup of an entire ROS 2 application, including multiple nodes, their parameters, and remappings. This lesson will focus on using Python-based launch files.

## Conceptual Explanation

**ROS 2 Launch Files:**

Launch files are Python scripts (or XML files, though Python is more flexible) that define a set of actions to be executed when the launch file is run. These actions can include:

-   **Node execution:** Starting one or more ROS 2 nodes.
-   **Parameter declaration:** Setting parameters for nodes.
-   **Remapping:** Changing the names of topics, services, or actions.
-   **Including other launch files:** Composing complex systems from smaller, reusable launch components.

**Parameters:** Nodes often require configuration values, known as parameters. Launch files provide a convenient way to set these parameters at startup, allowing for flexible configuration without modifying node code. Parameters can be specified directly in the launch file or loaded from YAML files.

**Remapping:** Remapping allows you to change the name of a topic, service, or action interface for a specific node. This is incredibly useful for connecting nodes that expect different naming conventions or for integrating multiple instances of the same node without name conflicts.

### Code Snippets/Examples

We will create a launch file that starts a publisher and subscriber (from Lesson 1) and also spawns our two-link arm in Gazebo (from Lesson 4).

### Example: Composing a System with a Launch File

This launch file demonstrates:
1.  Starting the `minimal_publisher` and `minimal_subscriber` nodes.
2.  Launching Gazebo and spawning the `two_link_arm` URDF model.

```python
# combined_launch.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Get paths
    pub_sub_share_dir = get_package_share_directory('pub_sub_demo')
    urdf_share_dir = get_package_share_directory('urdf_examples')
    gazebo_ros_share_dir = get_package_share_directory('gazebo_ros')

    # URDF file path
    urdf_file_name = 'two_link_arm.urdf'
    urdf_path = os.path.join(urdf_share_dir, 'urdf', urdf_file_name)

    # Gazebo launch file
    gazebo_launch_file = os.path.join(
        gazebo_ros_share_dir,
        'launch',
        'gazebo.launch.py'
    )

    # Nodes from pub_sub_demo package
    publisher_node = Node(
        package='pub_sub_demo',
        executable='minimal_publisher',
        name='publisher',
        output='screen',
    )

    subscriber_node = Node(
        package='pub_sub_demo',
        executable='minimal_subscriber',
        name='subscriber',
        output='screen',
    )

    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': Command(['xacro ', urdf_path])}
        ]
    )

    # Gazebo server
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={'verbose': 'false'}.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-file', urdf_path,
                                   '-entity', 'two_link_arm'],
                        output='screen')

    return LaunchDescription([
        publisher_node,
        subscriber_node,
        robot_state_publisher_node,
        gazebo_server,
        spawn_entity,
    ])

```

**Run Instructions:**

1.  Ensure both `pub_sub_demo` and `urdf_examples` packages are built and sourced in your workspace.
2.  Run the combined launch file:
    ```bash
    source install/setup.bash
    ros2 launch <your_launch_package_name> combined_launch.launch.py
    ```
    (Replace `<your_launch_package_name>` with the actual name of the ROS 2 package containing this launch file, which will be created in the next task.)

**Expected Output:**

-   You should see the `minimal_publisher` and `minimal_subscriber` nodes exchanging messages in the terminal.
-   A Gazebo window should open, displaying the two-link arm model.
-   You can verify topic communication using `ros2 topic echo /topic` and `ros2 topic echo /tf`.

## Exercises

1.  Modify the launch file to remap the `/topic` topic to `/my_custom_topic` for the `minimal_subscriber` node only.
2.  Add a parameter to the `minimal_publisher` node (e.g., `publish_frequency`) and demonstrate how to set it via the launch file or a YAML file.
3.  Create a separate small Python node that publishes a custom message type, and integrate it into the combined launch file.

## Summary

ROS 2 launch files are indispensable for starting and managing complex robotic applications. They allow you to orchestrate multiple nodes, set parameters, and remap interfaces, providing a robust and flexible framework for system composition and deployment.

## Troubleshooting

-   **Launch file not found**: Ensure your package is built and sourced. Verify the launch file name and package name are correct.
-   **Node errors within launch**: Check the output in the terminal for specific node-level error messages. Ensure all dependencies for nodes (e.g., `std_msgs`, `example_interfaces` in `package.xml`) are correctly specified and installed.
-   **Gazebo/URDF issues**: If the robot doesn't appear or Gazebo fails to launch, review the `urdf_examples` setup and Gazebo installation.
