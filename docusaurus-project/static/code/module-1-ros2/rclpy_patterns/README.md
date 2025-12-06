# ROS 2 rclpy Patterns Examples

This package provides examples demonstrating QoS settings and proper shutdown in ROS 2 `rclpy` nodes.

## Structure

- `src/qos_demo/qos_publisher.py`: A publisher node configured with `RELIABLE` reliability and `TRANSIENT_LOCAL` durability.
- `src/qos_demo/qos_subscriber.py`: A subscriber node configured with the same QoS profile to ensure compatibility and demonstrate `TRANSIENT_LOCAL` behavior.

## Build Instructions

1.  Navigate to your ROS 2 workspace (e.g., `~/ros2_ws`).
2.  Place the `rclpy_patterns` folder into the `src` directory of your workspace.
3.  Build the package:
    ```bash
    colcon build --packages-select qos_demo
    ```
4.  Source your workspace:
    ```bash
    source install/setup.bash
    ```

## Run Instructions

### 1. QoS with `TRANSIENT_LOCAL` Durability

This demonstrates that a late-joining subscriber will receive the last message published.

1.  **Run the publisher** in one terminal. Let it publish a few messages:
    ```bash
    ros2 run qos_demo qos_publisher
    ```
    *Expected Output (Publisher):*
    ```text
    [INFO] [qos_publisher]: Publishing: "Hello QoS: 0"
    [INFO] [qos_publisher]: Publishing: "Hello QoS: 1"
    ...
    ```

2.  **Run the subscriber** in a second terminal *after* some messages have been published by the publisher:
    ```bash
    ros2 run qos_demo qos_subscriber
    ```
    *Expected Output (Subscriber):*
    ```text
    [INFO] [qos_subscriber]: Subscriber created with QoS profile
    [INFO] [qos_subscriber]: I heard: "Hello QoS: N"  (where N is the last message published)
    [INFO] [qos_subscriber]: I heard: "Hello QoS: N+1"
    ...
    ```

### 2. QoS with `VOLATILE` Durability (Conceptual)

If you were to change `DurabilityPolicy.TRANSIENT_LOCAL` to `DurabilityPolicy.VOLATILE` in both nodes, a late-joining subscriber would *not* receive any prior messages. Only messages published *after* the subscriber starts would be received.

## Expected Outcome

-   The `qos_publisher` and `qos_subscriber` nodes will communicate according to the defined QoS profiles.
-   When `TRANSIENT_LOCAL` durability is used, late-joining subscribers will receive the last message published.

## Further Exploration

-   Experiment with different `ReliabilityPolicy` (`BEST_EFFORT` vs. `RELIABLE`) and `DurabilityPolicy` (`VOLATILE` vs. `TRANSIENT_LOCAL`) combinations and observe their impact on message delivery, especially under network congestion or when nodes join at different times.
-   Implement a basic ROS 2 Lifecycle Node and observe its state transitions.
