---
sidebar_position: 8
sidebar_label: "Capstone Project: Voice Command Robot"
id: module-1-ros2-capstone
---

# Capstone Project: Voice Command Robot

## Project Goal

Implement a basic system where a Python-based agent interprets a voice command (simulated via text input) and translates it into a ROS 2 action goal to control a simulated robot's behavior (e.g., movement, simple task execution).

This project integrates concepts from all previous lessons: ROS 2 topics, services, actions, URDF, launch files, and agent-ROS bridging.

## Scaffold Steps

1.  **Review Core Concepts:** Ensure a solid understanding of ROS 2 communication patterns, especially actions, and the agent-ROS bridge architecture from Lesson 6.
2.  **Define Robot Action:** Create a custom ROS 2 action definition (`.action` file) for robot movement (e.g., `MoveDistance` or `TurnAngle`). This will be part of a new ROS 2 Python package.
3.  **Implement Action Server:** Develop a ROS 2 node that acts as the action server for your custom `MoveDistance` (or similar) action. This server will simulate robot movement (e.g., by printing messages or updating a simple state).
4.  **Develop Voice Command Agent:** Create a Python script that:
    -   Takes text input simulating a voice command (e.g., "move forward 2 meters", "turn left 90 degrees").
    -   Parses the text command to extract the intended action and parameters (e.g., "move forward", distance `2`).
    -   Uses `rclpy` to act as an action client, sending the parsed command as a goal to your robot action server.
5.  **Integrate with Launch File:** Create a new ROS 2 launch file that:
    -   Starts your custom robot action server.
    -   (Optional but recommended) Launches Gazebo and spawns a simple robot (e.g., the two-link arm, or a differential drive robot if you extend the URDF examples).
    -   (Optional) Includes any other necessary nodes or parameters.
6.  **Testing and Verification:**
    -   Run the launch file.
    -   Execute the voice command agent.
    -   Verify that the robot action server receives and processes the goals, and that feedback/results are communicated back to the agent.

## Expected Deliverables

-   A new ROS 2 Python package containing:
    -   Custom `.action` definition.
    -   Robot action server node (`.py`).
-   Python script for the voice command agent (`.py`).
-   ROS 2 Python launch file (`.launch.py`).
-   (Optional) Updated URDF model or a new simple robot URDF.
-   A `README.md` in the new package explaining build/run instructions and expected behavior.

## Reference Files

-   `docs/module-1-ros2/lesson-2-services-actions.md` (for action client/server patterns)
-   `docs/module-1-ros2/lesson-6-agent-to-ros-bridge.md` (for agent integration)
-   `static/code/module-1-ros2/service_examples/` (example action server/client)
-   `static/code/module-1-ros2/agent_bridge_examples/text_command_agent.py` (example agent framework)
-   `static/code/module-1-ros2/urdf_examples/` (for robot description and Gazebo spawning)
-   `static/code/module-1-ros2/launch_examples/` (for launch file structure)
