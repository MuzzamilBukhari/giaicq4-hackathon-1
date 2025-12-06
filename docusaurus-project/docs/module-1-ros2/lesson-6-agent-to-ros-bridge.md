---
sidebar_position: 7
sidebar_label: "Agent → ROS Bridge"
id: module-1-ros2-agent-ros-bridge
---

# Lesson 6: Agent � ROS Bridge

## Learning Objectives

- Understand the architectural patterns for connecting high-level AI agents to ROS 2 robotic systems.
- Learn to design and implement a simple bridge between a Python agent and ROS 2 communication interfaces (services/actions).
- Comprehend how to send commands from a non-ROS Python script to control a simulated robot via ROS 2 actions.

## Introduction

In many advanced robotics applications, high-level decision-making is handled by sophisticated AI agents (e.g., in Python, using frameworks like OpenAI Gym, custom reinforcement learning setups, or even large language models). These agents need a way to issue commands to and receive feedback from the lower-level robotic controllers, which are often managed by ROS 2. This lesson explores how to build a **bridge** between a Python agent and ROS 2.

## Conceptual Explanation

**The Need for a Bridge:**

High-level AI agents typically operate outside the ROS 2 graph, focusing on complex reasoning, planning, or learning. They produce abstract commands (e.g., "move forward", "pick up item"). ROS 2, on the other hand, deals with concrete robot commands (e.g., publishing `Twist` messages to `/cmd_vel`, calling a `MoveToGoal` action).

A bridge component translates these high-level agent commands into ROS 2-compatible messages or service/action calls, and vice-versa for feedback or sensor data. This allows the agent to interact with the robot without needing to be a full ROS 2 node itself.

**Architectural Patterns:**

Common patterns for building such bridges include:

-   **ROS 2 Clients in Agent:** The agent directly uses `rclpy` (or `rclcpp` for C++) to act as a ROS 2 client (publisher, service client, action client). This is often the most straightforward approach for Python agents.
-   **Middleware/Gateway Node:** A dedicated ROS 2 node acts as an intermediary, communicating with the external agent via standard IPC (e.g., TCP sockets, REST API) and then translating to ROS 2. This provides greater decoupling.

### Code Snippets/Examples

We will create a simple Python script (`text_command_agent.py`) that acts as a basic agent, taking text commands and translating them into a ROS 2 action call to move a simulated robot.

### Example: Text Command Agent to ROS 2 Action Bridge

This example assumes a ROS 2 action server (like the Fibonacci one from Lesson 2, or a more realistic `MoveRobot` action) that can process a simple integer goal (e.g., representing a distance or a target ID).

```python
# text_command_agent.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci # Using Fibonacci for demonstration, imagine it's a 'MoveRobot' action
import time

class TextCommandAgent(Node):

    def __init__(self):
        super().__init__('text_command_agent')
        self._action_client = ActionClient(self, Fibonacci, 'robot_command_action') # Renamed action topic

    def send_goal(self, command_value):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = command_value # Interpreting command_value as 'order' for Fibonacci

        self._action_client.wait_for_server()

        self.get_logger().info(f'Sending goal: {command_value}')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Action completed. Result: {result.sequence}')
        # rclpy.shutdown() # Don't shutdown if agent is continuous

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')

def main(args=None):
    rclpy.init(args=args)

    agent = TextCommandAgent()

    # Simulate agent sending commands based on some logic or user input
    while rclpy.ok():
        user_input = input("Enter command value (e.g., 5, 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        try:
            command_value = int(user_input)
            agent.send_goal(command_value)
            time.sleep(1) # Give time for action to start
        except ValueError:
            agent.get_logger().warn('Invalid input. Please enter an integer.')

    agent.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run Instructions:**

1.  **Prepare the Action Server:** Start an action server that listens on the `robot_command_action` topic and accepts `Fibonacci` action goals. For this example, you would need to modify the `minimal_action_server.py` from Lesson 2 to use `robot_command_action` instead of `fibonacci`.
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_action_package_name> minimal_action_server
    ```
2.  **Run the Text Command Agent** in a separate terminal:
    ```bash
    source /opt/ros/humble/setup.bash
    python3 static/code/module-1-ros2/agent_bridge_examples/text_command_agent.py
    ```
    (Replace `<your_action_package_name>` with the actual name of the ROS 2 package containing your action server, which will be created in the next task.)

**Expected Output (Action Server Terminal):**
```text
[INFO] [minimal_action_server]: Executing goal...
[INFO] [minimal_action_server]: Publishing feedback: [0, 1]
...
[INFO] [minimal_action_server]: Goal succeeded. Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Expected Output (Agent Terminal):**
```text
Enter command value (e.g., 5, 'quit' to exit): 5
[INFO] [text_command_agent]: Sending goal: 5
[INFO] [text_command_agent]: Goal accepted :)
[INFO] [text_command_agent]: Received feedback: [0, 1]
[INFO] [text_command_agent]: Received feedback: [0, 1, 1]
...
[INFO] [text_command_agent]: Action completed. Result: [0, 1, 1, 2, 3, 5]
```

## Exercises

1.  **Implement a custom ROS 2 Action:** Define a `.action` file for `MoveRobot` that takes a target `(x, y)` coordinate as a goal, provides `current_position` as feedback, and returns `success` as a result.
2.  **Modify the Agent:** Update `text_command_agent.py` to use your custom `MoveRobot` action and parse text commands like "move to 10 5" into action goals.
3.  **Bidirectional Communication:** Extend the bridge to allow the ROS 2 system to send sensor feedback (e.g., object detected) back to the Python agent using topics.

## Summary

Bridging high-level AI agents to ROS 2 robotic systems is crucial for embodied AI. By leveraging ROS 2's client libraries, agents can seamlessly interact with robot controllers through topics, services, and actions, enabling sophisticated autonomy.

## Troubleshooting

-   **Action server not found**: Ensure the action server node is running and the action name in the client matches the server.
-   **Message/Action type mismatch**: If you create custom `.action` files, ensure they are built correctly within a ROS 2 package and that your Python scripts import the generated types correctly.
-   **Agent not shutting down**: If `rclpy.spin()` is used in a loop, ensure proper shutdown logic with `rclpy.ok()` checks.
