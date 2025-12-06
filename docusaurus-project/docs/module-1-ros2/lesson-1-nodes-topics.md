---
sidebar_position: 2
sidebar_label: "Nodes & Topics"
id: module-1-ros2-nodes-topics
---

# Lesson 1: Nodes & Topics

## Learning Objectives

- Understand the concept of ROS 2 nodes as executable processes.
- Comprehend ROS 2 topics as a publish-subscribe communication mechanism.
- Learn to create simple ROS 2 publisher and subscriber nodes using `rclpy`.
- Be able to run and observe data exchange between nodes via topics.

## Introduction

In ROS 2, a **node** is an executable that performs computation. Nodes communicate with each other using a messaging system. The most common communication pattern is **topics**, which implement a publish-subscribe model. One node publishes data to a topic, and other nodes subscribe to that topic to receive the data.

## Conceptual Explanation

**Nodes:** Each node in a ROS 2 system should be responsible for a single, modular purpose (e.g., a camera driver node, a motor control node, a localization node). This modularity makes systems easier to build, debug, and maintain.

**Topics:** Topics are named buses over which nodes exchange messages. Messages are simply data structures. A node can publish messages to any topic, and any number of nodes can subscribe to a topic to receive messages. This decouples the senders from the receivers.

### Code Snippets/Examples

Let's create a simple publisher and subscriber using `rclpy`, the Python client library for ROS 2.

### Example: Minimal Publisher and Subscriber

We will create two Python scripts:
1.  `minimal_publisher.py`: Publishes a string message to the `/topic` topic.
2.  `minimal_subscriber.py`: Subscribes to the `/topic` topic and prints received messages.

```python
# minimal_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, ROS 2! %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```python
# minimal_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Run Instructions:**

1.  Open two separate terminal windows.
2.  In the first terminal, source your ROS 2 environment and run the publisher:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_publisher
    ```
3.  In the second terminal, source your ROS 2 environment and run the subscriber:
    ```bash
    source /opt/ros/humble/setup.bash
    ros2 run <your_package_name> minimal_subscriber
    ```
    (Replace `<your_package_name>` with the actual name of the ROS 2 package you will create in the next task.)

**Expected Output:**

*Terminal 1 (Publisher):*
```text
[INFO] [minimal_publisher]: Publishing: "Hello, ROS 2! 0"
[INFO] [minimal_publisher]: Publishing: "Hello, ROS 2! 1"
...
```

*Terminal 2 (Subscriber):*
```text
[INFO] [minimal_subscriber]: I heard: "Hello, ROS 2! 0"
[INFO] [minimal_subscriber]: I heard: "Hello, ROS 2! 1"
...
```

## Exercises

1.  Modify the publisher to publish a different message type (e.g., `Int32`). You will need to import `Int32` from `std_msgs.msg` and change the message type in `create_publisher` and `publish`.
2.  Create a third node that subscribes to the same topic and performs a simple operation on the received data (e.g., counts messages, reverses the string).

## Summary

Nodes are the fundamental execution units in ROS 2, and topics provide a flexible, decoupled mechanism for inter-node communication. By understanding how to create and manage publishers and subscribers, you have the building blocks for creating more complex robotic applications.

## Troubleshooting

-   **Nodes not found**: Ensure your ROS 2 environment is sourced (`source /opt/ros/humble/setup.bash`). Check that your package is built and installed correctly.
-   **No messages received**: Verify that both publisher and subscriber are running. Use `ros2 topic list` to see active topics and `ros2 topic echo /topic` to inspect messages directly on the command line.
