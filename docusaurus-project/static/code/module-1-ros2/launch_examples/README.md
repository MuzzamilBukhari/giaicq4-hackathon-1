# ROS 2 Launch File Examples

This package provides examples of ROS 2 launch files to orchestrate multiple nodes and manage parameters.

## Structure

- `combined_launch.launch.py`: A Python launch file that starts the `minimal_publisher` and `minimal_subscriber` nodes (from `pub_sub_demo` package) and spawns the `two_link_arm` URDF model in Gazebo (from `urdf_examples` package).
- `simple_params.yaml`: A YAML file demonstrating how to define parameters that can be loaded by ROS 2 nodes.

## Dependencies

This package depends on:
- `pub_sub_demo` (from `rclpy_examples`)
- `urdf_examples` (from `urdf_examples`)
- `ros-humble-gazebo-ros-pkgs`
- `ros-humble-robot-state-publisher`
- `ros-humble-joint-state-publisher-gui`
- `ros-humble-xacro`

Ensure these packages are built and their dependencies installed.

## Build Instructions

1.  Navigate to your ROS 2 workspace (e.g., `~/ros2_ws`).
2.  Place the `launch_examples` folder into the `src` directory of your workspace.
3.  Build the package:
    ```bash
    colcon build --packages-select launch_examples
    ```
4.  Source your workspace:
    ```bash
    source install/setup.bash
    ```

## Run Instructions

### 1. Run the Combined Launch File

This launch file will start the publisher, subscriber, robot state publisher, Gazebo, and spawn the two-link arm.

```bash
ros2 launch launch_examples combined_launch.launch.py
```

**Expected Outcome:**

-   You should see messages from the `minimal_publisher` and `minimal_subscriber` in the terminal.
-   A Gazebo window will open with the `two_link_arm` spawned.
-   You can verify ROS 2 topics like `/topic` and `/tf` are active using `ros2 topic list` and `ros2 topic echo`.

### 2. Loading Parameters from YAML (Conceptual)

To load parameters from `simple_params.yaml` into a node, you would typically include it in your launch file using `SetParameter` or `DeclareLaunchArgument` with `LaunchConfiguration`.

For example, if you had a node that could accept `qos_depth` as a parameter:

```python
# Snippet from a launch file
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# ...

# Declare launch argument for parameter file
param_file_arg = DeclareLaunchArgument(
    'param_file',
    default_value=os.path.join(
        get_package_share_directory('launch_examples'),
        'simple_params.yaml'
    )
)

my_parameter_node = Node(
    package='my_package',
    executable='my_node',
    name='my_node',
    parameters=[LaunchConfiguration('param_file')]
)

# ... add param_file_arg and my_parameter_node to LaunchDescription
```

Then, you could run it:

```bash
ros2 launch <your_launch_package_name> your_launch_file.launch.py param_file:=path/to/simple_params.yaml
```
