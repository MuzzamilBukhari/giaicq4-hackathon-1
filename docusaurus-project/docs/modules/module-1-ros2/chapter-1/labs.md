---
id: module-1-ros2-chapter-1-labs
title: "Chapter 1 Labs"
sidebar_label: "Labs"
---

# Chapter 1: Hands-On Labs

Complete these labs to practice ROS 2 fundamentals with publishers, subscribers, and topics.

## Lab 1.1: Simple Talker-Listener

**Objective**: Create a basic publisher-subscriber system.

### Instructions

1. **Create package**
   ```bash
   cd ~/ros2_ws/src
   ros2 pkg create --build-type ament_python lab1_basics --dependencies rclpy std_msgs
   ```

2. **Implement publisher** (`talker.py`)
   - Publish "Hello ROS 2: [count]" every 1 second to `/chatter`
   - Use `std_msgs/String`

3. **Implement subscriber** (`listener.py`)
   - Subscribe to `/chatter`
   - Log received messages

4. **Build and test**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select lab1_basics
   source install/setup.bash
   
   # Terminal 1
   ros2 run lab1_basics talker
   
   # Terminal 2
   ros2 run lab1_basics listener
   ```

### Success Criteria
- [ ] Talker publishes incrementing messages
- [ ] Listener receives and logs all messages
- [ ] `ros2 topic list` shows `/chatter`
- [ ] `ros2 topic echo /chatter` displays messages

---

## Lab 1.2: Multi-Topic Publisher

**Objective**: Publish to multiple topics with different rates.

### Requirements

Create a node that publishes:
- Temperature data to `/sensors/temperature` (every 2 sec)
- Humidity data to `/sensors/humidity` (every 3 sec)
- Combined data to `/sensors/combined` (every 5 sec)

Use `std_msgs/Float64` for individual topics.

### Template

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String
import random


class MultiSensorPublisher(Node):
    def __init__(self):
        super().__init__('multi_sensor_publisher')
        
        # Create publishers
        self.temp_pub = self.create_publisher(Float64, '/sensors/temperature', 10)
        self.humid_pub = self.create_publisher(Float64, '/sensors/humidity', 10)
        self.combined_pub = self.create_publisher(String, '/sensors/combined', 10)
        
        # Create timers
        self.temp_timer = self.create_timer(2.0, self.publish_temperature)
        self.humid_timer = self.create_timer(3.0, self.publish_humidity)
        self.combined_timer = self.create_timer(5.0, self.publish_combined)
        
        # State
        self.last_temp = 20.0
        self.last_humid = 50.0
    
    def publish_temperature(self):
        # TODO: Implement temperature publishing
        pass
    
    def publish_humidity(self):
        # TODO: Implement humidity publishing
        pass
    
    def publish_combined(self):
        # TODO: Implement combined publishing
        pass


def main(args=None):
    rclpy.init(args=args)
    node = MultiSensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Testing Commands

```bash
# Monitor temperature
ros2 topic hz /sensors/temperature

# Echo combined data
ros2 topic echo /sensors/combined

# Check all topics
ros2 topic list
```

### Success Criteria
- [ ] Temperature published every 2 seconds
- [ ] Humidity published every 3 seconds
- [ ] Combined data published every 5 seconds
- [ ] Topic rates verified with `ros2 topic hz`

---

## Lab 1.3: Custom Message Definition

**Objective**: Create and use a custom message type.

### Steps

1. **Create interface package**
   ```bash
   cd ~/ros2_ws/src
   ros2 pkg create --build-type ament_cmake sensor_interfaces
   ```

2. **Define message**
   
   Create `sensor_interfaces/msg/SensorReading.msg`:
   ```
   # Sensor reading with metadata
   string sensor_id
   float64 temperature
   float64 humidity
   float64 pressure
   int64 timestamp_ns
   bool is_valid
   ```

3. **Update CMakeLists.txt**
   ```cmake
   find_package(rosidl_default_generators REQUIRED)
   
   rosidl_generate_interfaces(${PROJECT_NAME}
     "msg/SensorReading.msg"
   )
   ```

4. **Update package.xml**
   ```xml
   <build_depend>rosidl_default_generators</build_depend>
   <exec_depend>rosidl_default_runtime</exec_depend>
   <member_of_group>rosidl_interface_packages</member_of_group>
   ```

5. **Build interface**
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select sensor_interfaces
   source install/setup.bash
   ```

6. **Use in Python node**
   ```python
   from sensor_interfaces.msg import SensorReading
   
   class CustomSensorPublisher(Node):
       def __init__(self):
           super().__init__('custom_sensor_pub')
           self.publisher = self.create_publisher(
               SensorReading, 
               '/sensor/reading', 
               10
           )
           self.timer = self.create_timer(1.0, self.publish_reading)
       
       def publish_reading(self):
           msg = SensorReading()
           msg.sensor_id = "DHT22_01"
           msg.temperature = 22.5
           msg.humidity = 55.3
           msg.pressure = 1013.25
           msg.timestamp_ns = self.get_clock().now().nanoseconds
           msg.is_valid = True
           self.publisher.publish(msg)
   ```

### Success Criteria
- [ ] Custom message builds without errors
- [ ] Publisher node runs successfully
- [ ] `ros2 interface show sensor_interfaces/msg/SensorReading` displays definition
- [ ] `ros2 topic echo /sensor/reading` shows custom messages

---

## Lab 1.4: QoS Experimentation

**Objective**: Understand QoS policy effects.

### Experiment Setup

Create two publisher-subscriber pairs:
1. **Reliable QoS**: Guaranteed delivery
2. **Best-Effort QoS**: May drop messages

### Implementation

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Reliable profile
reliable_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST
)

# Best-effort profile
best_effort_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST
)

class QoSExperimentNode(Node):
    def __init__(self):
        super().__init__('qos_experiment')
        
        # Create publishers with different QoS
        self.reliable_pub = self.create_publisher(
            String, '/reliable_topic', reliable_qos
        )
        self.best_effort_pub = self.create_publisher(
            String, '/best_effort_topic', best_effort_qos
        )
        
        # High-frequency publishing
        self.timer = self.create_timer(0.01, self.publish_data)  # 100 Hz
        self.count = 0
    
    def publish_data(self):
        msg = String()
        msg.data = f'Message {self.count}'
        self.reliable_pub.publish(msg)
        self.best_effort_pub.publish(msg)
        self.count += 1
```

### Test Scenarios

1. **Normal conditions**: Both should work
2. **Network stress**: Simulate with `tc` (Linux traffic control)
3. **Late-joining subscribers**: Start publisher, wait 5 sec, start subscriber

### Observations to Record
- Message loss count (RELIABLE vs BEST_EFFORT)
- Latency differences
- Behavior with late-joining subscribers

---

## Challenge Lab: Robot Telemetry System

**Objective**: Build a complete telemetry system.

### Requirements

Create a system with:
- **GPS Publisher**: Publishes location at 10 Hz
- **Battery Publisher**: Publishes voltage at 1 Hz
- **IMU Publisher**: Publishes orientation at 50 Hz
- **Telemetry Aggregator**: Subscribes to all, logs to file
- **Dashboard Node**: Prints summary every 5 seconds

### Bonus Features
- [ ] Custom message for aggregated data
- [ ] Timestamp synchronization
- [ ] Data validation (reject invalid readings)
- [ ] Launch file to start all nodes
- [ ] RViz visualization (advanced)

### Suggested Message Types
- GPS: `sensor_msgs/NavSatFix`
- Battery: `sensor_msgs/BatteryState`
- IMU: `sensor_msgs/Imu`

---

## Submission Guidelines

For each lab:
1. **Code**: Commit to Git repository
2. **Documentation**: README with run instructions
3. **Video**: 1-2 min demo showing functionality
4. **Report**: Brief answers to questions (if any)

### Grading Rubric
- **Functionality** (50%): Code works as specified
- **Code Quality** (25%): Clean, commented, follows ROS 2 conventions
- **Documentation** (15%): Clear instructions, explanations
- **Creativity** (10%): Bonus features, novel approaches

---

## Next Chapter

Once you complete these labs, move on to:
- [Chapter 2: Services & Actions](../chapter-2/01-overview.md)

Great work mastering ROS 2 fundamentals! 🚀
