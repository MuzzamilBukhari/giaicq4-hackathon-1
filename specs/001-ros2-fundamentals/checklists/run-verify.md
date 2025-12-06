# Module 1: ROS 2 Fundamentals - Run and Verification Checklist

This checklist outlines the steps to run and verify the functionality of all ROS 2 example applications developed in Module 1.

## Prerequisites

-   All ROS 2 example packages for Module 1 must be successfully built and sourced (refer to `build-validate.md`).
-   ROS 2 Humble Hawksbill environment sourced.
-   Gazebo Classic installed and configured (for URDF/Gazebo examples).

## Verification Steps

Ensure that a ROS 2 environment is sourced in each new terminal window:
```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

### 1. Nodes & Topics (Lesson 1 - `rclpy_examples`)

-   [ ] **Publisher/Subscriber Communication:**
    1.  In Terminal 1: `ros2 run pub_sub_demo minimal_publisher`
    2.  In Terminal 2: `ros2 run pub_sub_demo minimal_subscriber`
    3.  *Verification:* Both terminals show messages being exchanged. `ros2 topic echo /topic` in a third terminal shows messages.
-   [ ] **Topic Info:**
    1.  While nodes are running: `ros2 topic info /topic --verbose`
    2.  *Verification:* Shows publisher/subscriber nodes, message type (`std_msgs/msg/String`), and QoS profile.

### 2. Services & Actions (Lesson 2 - `service_examples`)

-   [ ] **Service (AddTwoInts):**
    1.  In Terminal 1: `ros2 run service_action_demo minimal_service`
    2.  In Terminal 2: `ros2 run service_action_demo minimal_client 5 3`
    3.  *Verification:* Server logs incoming request and response. Client logs the sum `8`.
-   [ ] **Action (Fibonacci):**
    1.  In Terminal 1: `ros2 run service_action_demo minimal_action_server`
    2.  In Terminal 2: `ros2 run service_action_demo minimal_action_client`
    3.  *Verification:* Server logs goal execution and feedback. Client logs goal acceptance, feedback, and final result (Fibonacci sequence).

### 3. rclpy Patterns (Lesson 3 - `rclpy_patterns`)

-   [ ] **QoS (Transient Local Durability):**
    1.  In Terminal 1: `ros2 run qos_demo qos_publisher` (let publish a few messages)
    2.  In Terminal 2: `ros2 run qos_demo qos_subscriber` (start subscriber *after* publisher)
    3.  *Verification:* Subscriber receives the last published message immediately, then subsequent messages.

### 4. URDF & Robot Description (Lesson 4 - `urdf_examples`)

-   [ ] **Spawn Robot in Gazebo:**
    1.  In Terminal 1: `gazebo` (starts Gazebo GUI)
    2.  In Terminal 2: `ros2 run gazebo_ros spawn_entity.py -entity two_link_arm -file install/urdf_examples/share/urdf_examples/urdf/two_link_arm.urdf -x 0 -y 0 -z 0`
    3.  *Verification:* The two-link arm model appears in the Gazebo simulation. No errors in terminals.
-   [ ] **TF and Joint States:**
    1.  While robot is spawned: `ros2 topic echo /tf` and `ros2 topic echo /joint_states` (if `joint_state_publisher_gui` is running or a controller is publishing)
    2.  *Verification:* Relevant transformation data (`/tf`) and joint state data (`/joint_states`) are being published.

### 5. Launch Files & Parameter Management (Lesson 5 - `launch_examples`)

-   [ ] **Combined Launch File:**
    1.  In Terminal 1: `ros2 launch launch_examples combined_launch.launch.py`
    2.  *Verification:* Publisher/subscriber messages appear. Gazebo launches with the two-link arm. All components start without errors.

### 6. Agent → ROS Bridge (Lesson 6 - `agent_bridge_examples`)

-   [ ] **Text Command Agent to Action:**
    1.  In Terminal 1: Start your modified action server (e.g., `ros2 run service_action_demo minimal_action_server` with action topic renamed to `robot_command_action`).
    2.  In Terminal 2: `python3 static/code/module-1-ros2/agent_bridge_examples/text_command_agent.py`
    3.  *Verification:* Enter a number (e.g., `5`). Agent sends goal, server executes, feedback/result are shown in both terminals.

## Troubleshooting Runtime Issues

-   **Nodes not found / commands fail**: Ensure your workspace is sourced (`source install/setup.bash`) and all package dependencies are met.
-   **Communication failures**: Verify topic/service/action names are correct. Use `ros2 graph` to visualize the active ROS 2 graph and ensure connections are formed.
-   **Gazebo issues**: Check Gazebo logs for errors. Ensure `gazebo_ros` is installed and correctly configured.
