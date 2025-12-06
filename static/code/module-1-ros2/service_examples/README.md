# ROS 2 Services and Actions Examples

This package provides minimal examples of ROS 2 services and actions using `rclpy`.

## Structure

- `src/service_action_demo/minimal_service.py`: A service server that adds two integers.
- `src/service_action_demo/minimal_client.py`: A service client that requests two integers to be added.
- `src/service_action_demo/minimal_action_server.py`: An action server that computes a Fibonacci sequence.
- `src/service_action_demo/minimal_action_client.py`: An action client that requests a Fibonacci sequence.

## Build Instructions

1.  Navigate to your ROS 2 workspace (e.g., `~/ros2_ws`).
2.  Place the `service_examples` folder into the `src` directory of your workspace.
3.  Build the package:
    ```bash
    colcon build --packages-select service_action_demo
    ```
4.  Source your workspace:
    ```bash
    source install/setup.bash
    ```

## Run Instructions

### Services (AddTwoInts)

1.  **Run the service server** in one terminal:
    ```bash
    ros2 run service_action_demo minimal_service
    ```
    *Expected Output (Server):*
    ```text
    [INFO] [minimal_service]: Incoming request: a=5, b=3
    [INFO] [minimal_service]: Sending response: sum=8
    ```

2.  **Run the service client** in a second terminal (e.g., to add 5 and 3):
    ```bash
    ros2 run service_action_demo minimal_client 5 3
    ```
    *Expected Output (Client):*
    ```text
    [INFO] [minimal_client_async]: Result of add_two_ints: for 5 + 3 = 8
    ```

### Actions (Fibonacci)

1.  **Run the action server** in one terminal:
    ```bash
    ros2 run service_action_demo minimal_action_server
    ```
    *Expected Output (Server):*
    ```text
    [INFO] [minimal_action_server]: Executing goal...
    [INFO] [minimal_action_server]: Publishing feedback: [0, 1]
    [INFO] [minimal_action_server]: Publishing feedback: [0, 1, 1]
    ...
    [INFO] [minimal_action_server]: Goal succeeded. Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    ```

2.  **Run the action client** in a second terminal:
    ```bash
    ros2 run service_action_demo minimal_action_client
    ```
    *Expected Output (Client):*
    ```text
    [INFO] [minimal_action_client]: Goal accepted :)
    [INFO] [minimal_action_client]: Received feedback: [0, 1]
    [INFO] [minimal_action_client]: Received feedback: [0, 1, 1]
    ...
    [INFO] [minimal_action_client]: Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    ```
