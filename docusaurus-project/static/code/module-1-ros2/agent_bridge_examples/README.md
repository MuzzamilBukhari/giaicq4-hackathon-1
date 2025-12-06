# ROS 2 Agent to ROS Bridge Example

This example demonstrates how a simple Python agent, operating outside the ROS 2 graph, can send commands to a ROS 2 action server.

## Structure

- `text_command_agent.py`: A Python script that acts as a basic agent, taking integer commands from user input and sending them as goals to a ROS 2 action server (using the `Fibonacci` action type from `example_interfaces` for demonstration).

## Dependencies

- `rclpy`
- `example_interfaces` (for `Fibonacci` action)

This example assumes you have a ROS 2 action server running that can process `Fibonacci` action goals on the `robot_command_action` topic. You can adapt the `minimal_action_server.py` from the `service_action_demo` package (Lesson 2 examples) for this purpose by changing its action topic name.

## Build Instructions (for a companion ROS 2 package)

If you adapt the `service_action_demo` as a companion, ensure it's built:

1.  Navigate to your ROS 2 workspace (e.g., `~/ros2_ws`).
2.  Place the modified `service_action_demo` package (with the action topic renamed) into the `src` directory.
3.  Build the package:
    ```bash
    colcon build --packages-select service_action_demo
    ```
4.  Source your workspace:
    ```bash
    source install/setup.bash
    ```

## Run Instructions

1.  **Start the ROS 2 Action Server** (e.g., modified `minimal_action_server.py` from `service_action_demo`) in one terminal:
    ```bash
    source install/setup.bash
    ros2 run <your_action_package_name> minimal_action_server # Ensure this server listens on 'robot_command_action'
    ```
    (Replace `<your_action_package_name>` with the name of the package where your action server resides.)

2.  **Run the Text Command Agent** in a separate terminal:
    ```bash
    source install/setup.bash # Source ROS 2 environment for rclpy to find libraries
    python3 static/code/module-1-ros2/agent_bridge_examples/text_command_agent.py
    ```

3.  **Enter commands** in the agent's terminal. For instance, entering `5` will send a goal to the action server to compute Fibonacci up to order 5.

## Expected Output

*Action Server Terminal (e.g., `minimal_action_server` output):*
```text
[INFO] [minimal_action_server]: Executing goal...
[INFO] [minimal_action_server]: Publishing feedback: [0, 1]
...
[INFO] [minimal_action_server]: Goal succeeded. Result: [0, 1, 1, 2, 3, 5]
```

*Agent Terminal (`text_command_agent.py` output):*
```text
Enter command value (e.g., 5, 'quit' to exit): 5
[INFO] [text_command_agent]: Sending goal: 5
[INFO] [text_command_agent]: Goal accepted :)
[INFO] [text_command_agent]: Received feedback: [0, 1]
[INFO] [text_command_agent]: Received feedback: [0, 1, 1]
...
[INFO] [text_command_agent]: Action completed. Result: [0, 1, 1, 2, 3, 5]
```

## Further Exploration

-   Implement a more realistic action server that controls a simulated robot (e.g., `MoveRobot` action).
-   Modify the `text_command_agent.py` to parse more complex natural language commands.
-   Explore sending feedback from the ROS 2 system back to the agent (e.g., sensor readings).
