---
id: module-1-ros2-chapter-1-topics
title: "Topics & Communication"
sidebar_label: "Topics"
---

# Topics & Communication

## What are Topics?

Topics are named buses over which nodes exchange **messages**. They implement a publish-subscribe pattern where:
- **Publishers** send messages to a topic
- **Subscribers** receive messages from a topic
- Topics are many-to-many (multiple publishers and subscribers)

## Creating a Publisher

### Python Example: Simple Talker

```python
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
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
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

**Key Components:**
- `create_publisher(msg_type, topic_name, qos_depth)`
- Timer for periodic publishing
- Message creation and publishing

## Creating a Subscriber

### Python Example: Simple Listener

```python
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
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

**Key Components:**
- `create_subscription(msg_type, topic_name, callback, qos_depth)`
- Callback function executed when message received
- `rclpy.spin()` keeps node alive

## Standard Message Types

### Common std_msgs
```python
from std_msgs.msg import String, Int32, Float64, Bool, Header
```

### Sensor Messages
```python
from sensor_msgs.msg import Image, LaserScan, Imu, JointState
```

### Geometry Messages
```python
from geometry_msgs.msg import Twist, Pose, PoseStamped, Transform
```

### Example: Publishing Twist (Velocity Commands)
```python
from geometry_msgs.msg import Twist

class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_velocity)
    
    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 0.5  # Forward velocity
        msg.angular.z = 0.2  # Angular velocity
        self.publisher.publish(msg)
```

## Quality of Service (QoS)

### QoS Profiles

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# Reliable communication (like TCP)
reliable_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)

# Best-effort (like UDP, lower latency)
best_effort_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE
)

# Create publisher with custom QoS
self.publisher = self.create_publisher(String, 'topic', reliable_qos)
```

### When to Use Each
- **RELIABLE**: Critical data (commands, configurations)
- **BEST_EFFORT**: High-frequency sensor data (camera, LiDAR)
- **TRANSIENT_LOCAL**: Late-joining subscribers get last message
- **VOLATILE**: Real-time data only

## Custom Messages

### Define Message Type

Create `my_interfaces/msg/SensorData.msg`:
```
# Custom sensor data message
string sensor_name
float64 temperature
float64 humidity
int32 timestamp_ms
```

### Build Interface Package
```bash
cd ~/ros2_ws
colcon build --packages-select my_interfaces
source install/setup.bash
```

### Use Custom Message
```python
from my_interfaces.msg import SensorData

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')
        self.publisher = self.create_publisher(SensorData, '/sensor_data', 10)
        
    def publish_data(self):
        msg = SensorData()
        msg.sensor_name = "DHT22"
        msg.temperature = 23.5
        msg.humidity = 60.2
        msg.timestamp_ms = int(time.time() * 1000)
        self.publisher.publish(msg)
```

## ROS 2 CLI Tools

### List Active Topics
```bash
ros2 topic list
```

### Get Topic Info
```bash
ros2 topic info /topic_name
```

### Echo Topic Messages
```bash
ros2 topic echo /topic_name
```

### Publish from CLI
```bash
ros2 topic pub /topic_name std_msgs/String "data: 'Hello ROS 2'"
```

### Check Message Type
```bash
ros2 interface show std_msgs/msg/String
```

### Measure Topic Rate
```bash
ros2 topic hz /camera/image_raw
```

## Best Practices

1. **Meaningful Topic Names**: Use `/namespace/descriptive_name`
2. **Choose Appropriate QoS**: Match reliability to use case
3. **Message Design**: Keep messages simple, avoid deep nesting
4. **Callback Efficiency**: Minimize processing in callbacks
5. **Error Handling**: Check message validity before processing

## Common Pitfalls

❌ **Blocking operations in callbacks**
```python
def callback(self, msg):
    time.sleep(5)  # BAD: blocks executor
```

✅ **Async or separate thread for long operations**
```python
def callback(self, msg):
    self.executor.create_task(self.process_async(msg))
```

❌ **QoS mismatch between publisher and subscriber**
- Publisher: RELIABLE, Subscriber: BEST_EFFORT → No connection

## Exercise: Multi-Publisher System

**Challenge**: Create a system with:
- 1 temperature publisher (updates every 2 seconds)
- 1 humidity publisher (updates every 3 seconds)
- 1 subscriber that logs both

**Bonus**: Add a custom message combining both readings.

## Next Steps

Continue to [Labs](./labs.md) for hands-on practice with publishers and subscribers.
