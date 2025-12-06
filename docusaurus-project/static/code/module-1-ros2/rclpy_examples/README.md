# ROS 2 rclpy Examples Package

This package contains basic ROS 2 publisher-subscriber examples using Python (`rclpy`).

## Package Structure

```
rclpy_examples/
├── package.xml          # ROS 2 package manifest
├── setup.py            # Python package setup
├── setup.cfg           # Python package configuration
├── src/
│   └── pub_sub_demo/
│       ├── __init__.py
│       ├── minimal_publisher.py
│       └── minimal_subscriber.py
└── README.md
```

## Prerequisites

- ROS 2 (Humble or later recommended)
- Python 3.8+
- `rclpy` library (included with ROS 2)

## Building the Package

1. Navigate to your ROS 2 workspace:
   ```bash
   cd ~/ros2_ws
   ```

2. Copy this package to the `src` directory:
   ```bash
   cp -r /path/to/rclpy_examples src/
   ```

3. Build using colcon:
   ```bash
   colcon build --packages-select rclpy_examples
   ```

4. Source the workspace:
   ```bash
   source install/setup.bash
   ```

## Running the Examples

### Publisher Node

In terminal 1:
```bash
ros2 run rclpy_examples publisher
```

Expected output:
```
[INFO] [minimal_publisher]: Publishing: "Hello World: 0"
[INFO] [minimal_publisher]: Publishing: "Hello World: 1"
...
```

### Subscriber Node

In terminal 2:
```bash
ros2 run rclpy_examples subscriber
```

Expected output:
```
[INFO] [minimal_subscriber]: I heard: "Hello World: 0"
[INFO] [minimal_subscriber]: I heard: "Hello World: 1"
...
```

## Verifying Communication

You can verify the topic is working:
```bash
ros2 topic list
ros2 topic echo /topic
ros2 node list
```

## Troubleshooting

- **Package not found**: Ensure you've sourced the workspace: `source install/setup.bash`
- **No messages received**: Check that both nodes are running in separate terminals
- **Build errors**: Verify ROS 2 is properly installed and sourced

## Learn More

See the corresponding lesson in the documentation for detailed explanations of:
- Node creation patterns
- Publisher/Subscriber architecture
- Topic communication
- QoS (Quality of Service) settings
