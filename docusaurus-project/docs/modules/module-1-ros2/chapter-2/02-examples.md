---
id: module-1-ros2-chapter-2-examples
title: "Services & Actions Examples"
sidebar_label: "Examples"
---

# Services & Actions Implementation

## Service Server Example

### Python Service Server

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(
            AddTwoInts, 
            'add_two_ints', 
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: {request.a} + {request.b}')
        return response


def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

**Key points:**
- `create_service(srv_type, name, callback)`
- Callback receives request, must return response
- Service runs continuously waiting for requests

## Service Client Example

### Python Service Client

```python
import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
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
    minimal_client.get_logger().info(f'Result: {response.sum}')
    minimal_client.destroy_node()
    rclpy.shutdown()
```

### Usage
```bash
# Terminal 1: Start server
ros2 run my_package service_server

# Terminal 2: Call service
ros2 run my_package service_client 5 7
# Output: Result: 12

# Or use CLI
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 7}"
```

## Action Server Example

### Python Action Server (Fibonacci)

```python
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        # Initialize feedback
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        # Generate Fibonacci sequence
        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + 
                feedback_msg.partial_sequence[i-1]
            )
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        # Return result
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
```

**Key points:**
- `ActionServer(node, action_type, name, callback)`
- Callback executes goal and publishes feedback
- Must call `goal_handle.succeed()` or `goal_handle.abort()`
- Return final result

## Action Client Example

### Python Action Client

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.partial_sequence}')


def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
```

### Action Client with Cancellation

```python
def send_goal_with_cancel(self, order):
    goal_msg = Fibonacci.Goal()
    goal_msg.order = order
    
    self._action_client.wait_for_server()
    goal_future = self._action_client.send_goal_async(goal_msg)
    
    rclpy.spin_until_future_complete(self, goal_future)
    goal_handle = goal_future.result()
    
    # Cancel after 2 seconds
    time.sleep(2)
    cancel_future = goal_handle.cancel_goal_async()
    rclpy.spin_until_future_complete(self, cancel_future)
    
    self.get_logger().info('Goal canceled')
```

## Custom Service Definition

### Create Service Interface

File: `my_interfaces/srv/ComputeRectangleArea.srv`
```
# Request
float64 length
float64 width
---
# Response
float64 area
```

### Build and Use

```bash
# Build
colcon build --packages-select my_interfaces
source install/setup.bash

# Server implementation
from my_interfaces.srv import ComputeRectangleArea

class AreaService(Node):
    def __init__(self):
        super().__init__('area_service')
        self.srv = self.create_service(
            ComputeRectangleArea,
            'compute_area',
            self.compute_area_callback
        )
    
    def compute_area_callback(self, request, response):
        response.area = request.length * request.width
        return response
```

## Custom Action Definition

### Create Action Interface

File: `my_interfaces/action/MoveRobot.action`
```
# Goal
float64 target_x
float64 target_y
---
# Result
bool success
float64 final_x
float64 final_y
---
# Feedback
float64 current_x
float64 current_y
float64 distance_remaining
```

### Implementation

```python
from my_interfaces.action import MoveRobot

class MoveRobotServer(Node):
    def __init__(self):
        super().__init__('move_robot_server')
        self._action_server = ActionServer(
            self, MoveRobot, 'move_robot', self.execute_callback
        )
    
    def execute_callback(self, goal_handle):
        feedback_msg = MoveRobot.Feedback()
        
        # Simulate movement
        for step in range(10):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return MoveRobot.Result()
            
            # Update position
            feedback_msg.current_x = step * 0.1
            feedback_msg.current_y = step * 0.1
            feedback_msg.distance_remaining = 10 - step
            
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.5)
        
        goal_handle.succeed()
        result = MoveRobot.Result()
        result.success = True
        result.final_x = goal_handle.request.target_x
        result.final_y = goal_handle.request.target_y
        return result
```

## CLI Tools for Services and Actions

### Services

```bash
# List all services
ros2 service list

# Get service type
ros2 service type /add_two_ints

# Call service
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"

# Find services by type
ros2 service find std_srvs/srv/SetBool
```

### Actions

```bash
# List all actions
ros2 action list

# Get action info
ros2 action info /fibonacci

# Send action goal
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}"

# Send goal with feedback
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 5}" --feedback
```

## Best Practices

### Services
1. **Keep services fast**: < 1 second response time
2. **Error handling**: Always validate inputs
3. **Synchronous by nature**: Don't block server callback
4. **Use for stateless operations**: Each request independent

### Actions
1. **Provide meaningful feedback**: Update progress regularly
2. **Handle cancellation**: Check `is_cancel_requested`
3. **Set result status**: Call `succeed()`, `abort()`, or `canceled()`
4. **Timeout management**: Client should handle long-running goals

## Common Patterns

### Service with Validation
```python
def callback(self, request, response):
    if request.a < 0 or request.b < 0:
        self.get_logger().error('Negative numbers not allowed')
        response.sum = -1  # Error indicator
        return response
    
    response.sum = request.a + request.b
    return response
```

### Action with Progress Tracking
```python
def execute_callback(self, goal_handle):
    total_steps = 100
    for step in range(total_steps):
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return Result()
        
        feedback = Feedback()
        feedback.progress = (step / total_steps) * 100.0
        goal_handle.publish_feedback(feedback)
        
        # Do work...
        time.sleep(0.1)
    
    goal_handle.succeed()
    return Result()
```

## Next Steps

Practice with [Labs](./labs.md) to build your own services and actions!
