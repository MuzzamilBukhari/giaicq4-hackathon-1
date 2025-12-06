## ROS 2 URDF and Gazebo Integration Example

This package provides a minimal URDF model of a two-link arm and a launch file to spawn it in Gazebo.

## Structure

- `urdf/two_link_arm.urdf`: The URDF definition of a simple two-link arm.
- `launch/spawn_two_link_arm.launch.py`: A launch file to start `robot_state_publisher` and `joint_state_publisher_gui`. It also contains commented-out lines to directly launch Gazebo and spawn the robot.

## Dependencies

- `ros-humble-xacro`
- `ros-humble-robot-state-publisher`
- `ros-humble-joint-state-publisher-gui`
- `ros-humble-gazebo-ros-pkgs`

Install these dependencies using:
```bash
sudo apt update
sudo apt install ros-humble-xacro ros-humble-robot-state-publisher ros-humble-joint-state-publisher-gui ros-humble-gazebo-ros-pkgs
```

## Build Instructions

1.  Navigate to your ROS 2 workspace (e.g., `~/ros2_ws`).
2.  Place the `urdf_examples` folder into the `src` directory of your workspace.
3.  Build the package:
    ```bash
    colcon build --packages-select urdf_examples
    ```
4.  Source your workspace:
    ```bash
    source install/setup.bash
    ```

## Run Instructions

### 1. Launch Robot State Publisher and Joint State Publisher GUI

This will publish the robot's state and allow you to manipulate its joints manually.

```bash
ros2 launch urdf_examples spawn_two_link_arm.launch.py
```

### 2. Launch Gazebo and Spawn the Robot

To see the robot in Gazebo, you need to first launch Gazebo and then spawn the robot model.

1.  **Launch Gazebo** in one terminal:
    ```bash
    gazebo
    ```

2.  **Spawn the robot** in a second terminal (ensure your workspace is sourced):
    ```bash
    ros2 run gazebo_ros spawn_entity.py -entity two_link_arm -file install/urdf_examples/share/urdf_examples/urdf/two_link_arm.urdf -x 0 -y 0 -z 0
    ```
    *Note: The path to the URDF file in the `spawn_entity.py` command refers to its installation location after `colcon build`.*

### Verify Topics

After spawning the robot, you can verify that ROS 2 topics related to the robot's state are being published:

-   **Check TF (Transformations):**
    ```bash
    ros2 topic echo /tf
    ```
-   **Check Joint States (if `joint_state_publisher_gui` is running):**
    ```bash
    ros2 topic echo /joint_states
    ```

## Expected Outcome

-   The two-link arm model should appear in the Gazebo simulation environment.
-   You should be able to see `tf` messages and `joint_states` messages (if `joint_state_publisher_gui` is active) being published.
