---
sidebar_position: 3
sidebar_label: "Services & Actions"
id: module-1-ros2-services-actions
---

# Lesson 2: Services & Actions

## Learning Objectives

- Understand the concept of ROS 2 services for synchronous, request-response communication.
- Comprehend ROS 2 actions for long-running, goal-oriented tasks with feedback.
- Learn to create simple ROS 2 service server/client and action server/client using `rclpy`.
- Be able to run and observe request-response and goal-feedback interactions.

## Introduction

Beyond topics, ROS 2 provides other powerful communication patterns for different use cases. **Services** are used for synchronous request-response interactions, similar to a function call. **Actions** are designed for long-running tasks that require feedback and the ability to be preempted.

## Conceptual Explanation

### ROS 2 Services

Services in ROS 2 enable synchronous communication where a client sends a request to a server, and the server processes the request and sends back a single response. This is useful for operations that complete quickly and require a direct result, like asking a robot arm to move to a specific joint angle and waiting for confirmation.

**Key characteristics of Services:**
-   **Synchronous:** The client waits for the server's response.
-   **Request-Response:** A single request triggers a single response.
-   **Blocking:** The client's execution typically blocks until a response is received or a timeout occurs.

### ROS 2 Actions

Actions are built on top of topics and services and provide a more complex communication pattern for long-running goals. They allow a client to send a goal to an action server, receive continuous feedback on the goal's progress, and eventually get a result. The client can also preempt (cancel) the goal.

**Key characteristics of Actions:**
-   **Asynchronous (for the overall task):** The client doesn't block completely, but gets feedback.
-   **Goal-Feedback-Result:** A client sends a goal, receives feedback on progress, and eventually a final result.
-   **Preemptable:** The client can cancel an active goal.
-   **Long-running:** Suitable for tasks like navigating a robot to a distant location.

### Code Snippets/Examples

We will outline the structure for a simple service and action example.

### Example: Minimal Service Server and Client

We will create a service that adds two integers.

```python
# minimal_service_member_function.py (Service Server)
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        self.get_logger().info(f'Sending response: sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```python
# minimal_client_async.py (Service Client)
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(f'Result of add_two_ints: for {sys.argv[1]} + {sys.argv[2]} = {response.sum}')

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    import sys
    main()
```

**Run Instructions (Services):**

1.  Open two separate terminal windows.
2.  In the first terminal, source your ROS 2 environment and run the service server:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_service
    ```
3.  In the second terminal, source your ROS 2 environment and run the service client (e.g., to add 5 and 3):
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_client_async 5 3
    ```
    (Replace `<your_package_name>` with the actual name of the ROS 2 package you will create in the next task.)

**Expected Output (Service Server Terminal):**
```text
[INFO] [minimal_service]: Incoming request: a=5, b=3
[INFO] [minimal_service]: Sending response: sum=8
```

**Expected Output (Service Client Terminal):**
```text
[INFO] [minimal_client_async]: Result of add_two_ints: for 5 + 3 = 8
```

### Example: Minimal Action Server and Client

We will create an action that computes a Fibonacci sequence.

```python
# minimal_action_server.py (Action Server)
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class MinimalActionServer(Node):

    def __init__(self):
        super().__init__('minimal_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        sequence = [0, 1]
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
            sequence.append(sequence[i] + sequence[i-1])
            feedback_msg = Fibonacci.Feedback()
            feedback_msg.sequence = sequence
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Publishing feedback: {feedback_msg.sequence}')
            time.sleep(1) # Simulate long-running task

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence
        self.get_logger().info(f'Goal succeeded. Result: {result.sequence}')
        return result

def main(args=None):
    rclpy.init(args=args)

    minimal_action_server = MinimalActionServer()

    rclpy.spin(minimal_action_server)

if __name__ == '__main__':
    main()
```

```python
# minimal_action_client.py (Action Client)
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class MinimalActionClient(Node):

    def __init__(self):
        super().__init__('minimal_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

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
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.sequence}')

def main(args=None):
    rclpy.init(args=args)

    action_client = MinimalActionClient()
    action_client.send_goal(10)

    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

**Run Instructions (Actions):**

1.  Open two separate terminal windows.
2.  In the first terminal, source your ROS 2 environment and run the action server:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_action_server
    ```
3.  In the second terminal, source your ROS 2 environment and run the action client:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_action_client
    ```
    (Replace `<your_package_name>` with the actual name of the ROS 2 package you will create in the next task.)

**Expected Output (Action Server Terminal):**
```text
[INFO] [minimal_action_server]: Executing goal...
[INFO] [minimal_action_server]: Publishing feedback: [0, 1]
[INFO] [minimal_action_server]: Publishing feedback: [0, 1, 1]
...
[INFO] [minimal_action_server]: Goal succeeded. Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Expected Output (Action Client Terminal):**
```text
[INFO] [minimal_action_client]: Goal accepted :)
[INFO] [minimal_action_client]: Received feedback: [0, 1]
[INFO] [minimal_action_client]: Received feedback: [0, 1, 1]
...
[INFO] [minimal_action_client]: Result: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Exercises

1.  Modify the service to perform a different mathematical operation (e.g., multiplication, division).
2.  Implement an action client that sends a goal to the Fibonacci action server and then cancels the goal after a few feedback messages are received. Observe the server's response.
3.  Create a custom service or action definition (`.srv` or `.action` file) and use it in your nodes.

## Summary

Services provide a synchronous request-response mechanism for discrete operations, while actions offer an asynchronous, goal-oriented communication pattern with feedback and preemption capabilities for long-running tasks. These patterns, along with topics, form the core communication toolkit in ROS 2.

## Troubleshooting

-   **Service/Action not found**: Ensure the server node is running before the client. Verify the service/action name.
-   **Client timeout**: If the client waits indefinitely, check if the server node is actually providing the service/action. Use `ros2 service list` or `ros2 action list`.
-   **Incorrect arguments**: For service clients, ensure the correct number and type of arguments are passed from the command line.
