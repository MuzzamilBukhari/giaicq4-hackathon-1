---
id: chapter-4-integration-deployment-lab
title: Lab - End-to-End High-Level Pipeline—User Instruction → Simulated Humanoid Behavior
sidebar_label: "Lab: End-to-End Pipeline Integration"
---

# Lab: End-to-End High-Level Pipeline—User Instruction → Simulated Humanoid Behavior

## Overview

In this final lab of Module 4, you will integrate all the concepts learned throughout the module into a complete end-to-end pipeline. You'll create a system that takes high-level user instructions (in natural language), processes them through a Vision-Language-Action (VLA) system, applies humanoid kinematics for motion planning, and executes stable locomotion behaviors in simulation.

## Learning Objectives

- Integrate VLA systems with humanoid kinematics and locomotion control
- Implement an end-to-end pipeline from user instruction to robot behavior
- Understand the challenges and solutions in system integration
- Deploy and test a complete humanoid behavior system

## Prerequisites

- Completed Modules 1-4 of the Physical AI & Humanoid Robotics curriculum
- ROS 2 Humble installed and configured
- Gazebo or Isaac Sim installed
- Understanding of VLA systems, kinematics, and locomotion control
- Python programming experience

## Estimated Time

150-180 minutes

## Setup

1. Create a workspace for the integrated system:
   ```bash
   mkdir -p ~/vla_humanoid_integration_ws/src
   cd ~/vla_humanoid_integration_ws
   ```

2. Create a package for our integration system:
   ```bash
   cd src
   ros2 pkg create --build-type ament_python vla_humanoid_integration
   ```

## Step 1: Create the Integrated System Architecture

First, let's define the architecture of our end-to-end system:

1. Create the main integration node `vla_humanoid_integration/integration_pipeline.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point
from sensor_msgs.msg import JointState
from vla_msgs.action import TextToAction
from builtin_interfaces.msg import Duration
import numpy as np
import math
import json
from typing import Dict, List, Tuple, Optional

class VLAHumanoidIntegrator(Node):
    """Main integration node that connects VLA, kinematics, and locomotion"""

    def __init__(self):
        super().__init__('vla_humanoid_integrator')

        # Internal state
        self.current_pose = Pose()
        self.current_joint_states = JointState()
        self.is_executing = False
        self.execution_queue = []

        # Publishers
        self.command_pub = self.create_publisher(
            String,
            '/robot_commands',
            10
        )

        self.joint_command_pub = self.create_publisher(
            JointState,
            '/joint_commands',
            10
        )

        self.status_pub = self.create_publisher(
            String,
            '/system_status',
            10
        )

        # Subscribers
        self.instruction_sub = self.create_subscription(
            String,
            '/user_instructions',
            self.instruction_callback,
            10
        )

        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Action client for VLA processing
        self.vla_action_client = rclpy.action.ActionClient(
            self,
            TextToAction,
            'process_text_action'
        )

        # Timer for main control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('VLA Humanoid Integrator initialized')

    def instruction_callback(self, msg: String):
        """Handle incoming user instructions"""
        instruction = msg.data
        self.get_logger().info(f'Received instruction: {instruction}')

        # Add to execution queue
        self.execution_queue.append(instruction)

        # Process if not currently executing
        if not self.is_executing and self.execution_queue:
            self.process_next_instruction()

    def joint_state_callback(self, msg: JointState):
        """Update current joint states"""
        self.current_joint_states = msg

    def process_next_instruction(self):
        """Process the next instruction in the queue"""
        if not self.execution_queue:
            return

        instruction = self.execution_queue.pop(0)
        self.is_executing = True

        # Send to VLA processing
        self.send_vla_request(instruction)

    def send_vla_request(self, instruction: str):
        """Send instruction to VLA action server"""
        goal_msg = TextToAction.Goal()
        goal_msg.text_instruction = instruction

        self.vla_action_client.wait_for_server()
        future = self.vla_action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.vla_feedback_callback
        )

        future.add_done_callback(self.vla_response_callback)

    def vla_feedback_callback(self, feedback_msg):
        """Handle VLA processing feedback"""
        self.get_logger().info(f'VLA feedback: {feedback_msg.feedback.current_step}')

    def vla_response_callback(self, future):
        """Handle VLA processing response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('VLA goal rejected')
            self.is_executing = False
            return

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.vla_result_callback)

    def vla_result_callback(self, future):
        """Handle VLA processing result"""
        result = future.result().result

        if result.success:
            self.get_logger().info(f'VLA processing successful: {result.message}')
            # Now plan kinematics and locomotion based on VLA output
            self.plan_behavior(result.message)
        else:
            self.get_logger().error(f'VLA processing failed: {result.message}')
            self.is_executing = False

    def plan_behavior(self, action_description: str):
        """Plan the complete behavior including kinematics and locomotion"""
        self.get_logger().info(f'Planning behavior for: {action_description}')

        # Parse the action description to determine required movements
        parsed_action = self.parse_action_description(action_description)

        # Plan kinematic movements
        kinematic_plan = self.plan_kinematics(parsed_action)

        # Plan locomotion if needed
        locomotion_plan = self.plan_locomotion(parsed_action)

        # Execute the complete plan
        self.execute_plan(kinematic_plan, locomotion_plan)

    def parse_action_description(self, description: str) -> Dict:
        """Parse the action description into structured commands"""
        # Simple parsing for demonstration
        description_lower = description.lower()

        parsed = {
            'action_type': 'unknown',
            'target_location': None,
            'object_interaction': None,
            'required_locomotion': False
        }

        if 'move to' in description_lower or 'go to' in description_lower:
            parsed['action_type'] = 'navigation'
            parsed['required_locomotion'] = True
            # Extract target location (simplified)
            if 'table' in description_lower:
                parsed['target_location'] = {'x': 2.0, 'y': 1.0, 'z': 0.0}
            elif 'kitchen' in description_lower:
                parsed['target_location'] = {'x': 3.0, 'y': -1.0, 'z': 0.0}
            else:
                parsed['target_location'] = {'x': 1.0, 'y': 0.0, 'z': 0.0}

        elif 'pick' in description_lower or 'grasp' in description_lower:
            parsed['action_type'] = 'manipulation'
            parsed['object_interaction'] = 'grasp'

        elif 'place' in description_lower or 'put' in description_lower:
            parsed['action_type'] = 'manipulation'
            parsed['object_interaction'] = 'place'

        return parsed

    def plan_kinematics(self, parsed_action: Dict) -> List:
        """Plan the kinematic movements needed for the action"""
        self.get_logger().info('Planning kinematics...')

        # For demonstration, create a simple joint trajectory
        trajectory = []

        if parsed_action['action_type'] == 'manipulation':
            # Plan arm movement for manipulation
            trajectory.append({
                'joint_names': ['left_shoulder', 'left_elbow', 'right_shoulder', 'right_elbow'],
                'positions': [0.5, 0.3, 0.5, 0.3],
                'duration': Duration(sec=2)
            })
            trajectory.append({
                'joint_names': ['left_shoulder', 'left_elbow', 'right_shoulder', 'right_elbow'],
                'positions': [0.0, 0.0, 0.0, 0.0],
                'duration': Duration(sec=2)
            })

        return trajectory

    def plan_locomotion(self, parsed_action: Dict) -> List:
        """Plan the locomotion needed for the action"""
        if not parsed_action.get('required_locomotion', False):
            return []

        self.get_logger().info('Planning locomotion...')

        # For demonstration, create a simple walking trajectory
        trajectory = []

        if parsed_action['target_location']:
            target = parsed_action['target_location']
            # Simple path to target (in real system, this would use path planning)
            trajectory.append({
                'type': 'walk_to',
                'target': target,
                'speed': 0.5  # m/s
            })

        return trajectory

    def execute_plan(self, kinematic_plan: List, locomotion_plan: List):
        """Execute the complete behavior plan"""
        self.get_logger().info('Executing behavior plan...')

        # Execute locomotion first if needed
        if locomotion_plan:
            self.execute_locomotion(locomotion_plan)

        # Then execute kinematic movements
        if kinematic_plan:
            self.execute_kinematics(kinematic_plan)

        # Mark execution as complete
        self.is_executing = False

        # Process next instruction if available
        if self.execution_queue:
            self.process_next_instruction()

    def execute_locomotion(self, plan: List):
        """Execute locomotion plan"""
        self.get_logger().info('Executing locomotion plan...')

        # In a real system, this would interface with the locomotion controller
        # For demonstration, we'll just publish a command
        cmd_msg = String()
        cmd_msg.data = json.dumps({
            'command': 'locomotion',
            'plan': plan
        })
        self.command_pub.publish(cmd_msg)

    def execute_kinematics(self, plan: List):
        """Execute kinematic plan"""
        self.get_logger().info('Executing kinematic plan...')

        # Execute each trajectory point
        for point in plan:
            joint_state = JointState()
            joint_state.name = point['joint_names']
            joint_state.position = point['positions']

            # Publish joint commands
            self.joint_command_pub.publish(joint_state)

            # Wait for execution (in real system, this would be event-driven)
            time.sleep(point['duration'].sec + point['duration'].nanosec / 1e9)

    def control_loop(self):
        """Main control loop"""
        # Publish system status
        status_msg = String()
        status_msg.data = f"Idle - Queue: {len(self.execution_queue)}, Executing: {self.is_executing}"
        self.status_pub.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    integrator = VLAHumanoidIntegrator()

    try:
        rclpy.spin(integrator)
    except KeyboardInterrupt:
        pass
    finally:
        integrator.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 2: Create Supporting Components

Create additional components for the integration system:

1. Create `vla_humanoid_integration/safety_manager.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from sensor_msgs.msg import LaserScan, PointCloud2
from geometry_msgs.msg import Twist
import numpy as np

class SafetyManager(Node):
    """Safety manager for the integrated humanoid system"""

    def __init__(self):
        super().__init__('safety_manager')

        # Safety parameters
        self.emergency_stop_distance = 0.5  # meters
        self.is_safe = True
        self.emergency_stop_active = False

        # Publishers
        self.safety_status_pub = self.create_publisher(
            Bool,
            '/safety_status',
            10
        )

        self.emergency_stop_pub = self.create_publisher(
            Bool,
            '/emergency_stop',
            10
        )

        self.velocity_limit_pub = self.create_publisher(
            Twist,
            '/cmd_vel_limited',
            10
        )

        # Subscribers
        self.laser_scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_scan_callback,
            10
        )

        self.system_status_sub = self.create_subscription(
            String,
            '/system_status',
            self.system_status_callback,
            10
        )

        # Timer for safety checks
        self.safety_timer = self.create_timer(0.1, self.safety_check)

        self.get_logger().info('Safety Manager initialized')

    def laser_scan_callback(self, msg):
        """Process laser scan data for obstacle detection"""
        if len(msg.ranges) == 0:
            return

        # Find minimum distance in front of robot
        front_ranges = msg.ranges[len(msg.ranges)//2-30:len(msg.ranges)//2+30]
        min_distance = min([r for r in front_ranges if not np.isnan(r) and r > 0], default=float('inf'))

        # Check for obstacles
        if min_distance < self.emergency_stop_distance:
            self.get_logger().warn(f'Obstacle detected at {min_distance:.2f}m, triggering safety measures')
            self.emergency_stop_active = True
        else:
            self.emergency_stop_active = False

    def system_status_callback(self, msg):
        """Monitor system status"""
        status = msg.data
        self.get_logger().debug(f'System status: {status}')

    def safety_check(self):
        """Perform periodic safety checks"""
        # Update safety status
        self.is_safe = not self.emergency_stop_active

        # Publish safety status
        safety_msg = Bool()
        safety_msg.data = self.is_safe
        self.safety_status_pub.publish(safety_msg)

        # Publish emergency stop if needed
        emergency_msg = Bool()
        emergency_msg.data = self.emergency_stop_active
        self.emergency_stop_pub.publish(emergency_msg)

def main(args=None):
    rclpy.init(args=args)
    safety_manager = SafetyManager()

    try:
        rclpy.spin(safety_manager)
    except KeyboardInterrupt:
        pass
    finally:
        safety_manager.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 3: Create a Simple Example Publisher

Create a simple node to publish example instructions:

1. Create `vla_humanoid_integration/example_publisher.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class ExamplePublisher(Node):
    """Publish example instructions for the integrated system"""

    def __init__(self):
        super().__init__('example_publisher')

        self.instruction_pub = self.create_publisher(
            String,
            '/user_instructions',
            10
        )

        # Example instructions
        self.example_instructions = [
            "Move to the table",
            "Pick up the red object",
            "Place the object on the shelf",
            "Go to the kitchen",
            "Stand up and look around"
        ]

        # Timer to publish instructions periodically
        self.instruction_timer = self.create_timer(10.0, self.publish_next_instruction)
        self.current_instruction_index = 0

        self.get_logger().info('Example Publisher initialized')

    def publish_next_instruction(self):
        """Publish the next example instruction"""
        if self.current_instruction_index < len(self.example_instructions):
            instruction = self.example_instructions[self.current_instruction_index]
            msg = String()
            msg.data = instruction

            self.instruction_pub.publish(msg)
            self.get_logger().info(f'Published instruction: {instruction}')

            self.current_instruction_index += 1
        else:
            # Reset to start after all examples have been published
            self.current_instruction_index = 0

def main(args=None):
    rclpy.init(args=args)
    publisher = ExamplePublisher()

    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        pass
    finally:
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Step 4: Create a Launch File for the Complete System

1. Create the launch directory and file:
   ```bash
   mkdir -p vla_humanoid_integration/launch
   touch vla_humanoid_integration/launch/integration_system.launch.py
   ```

2. Add the following content to the launch file:

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Main integration node
    integration_node = Node(
        package='vla_humanoid_integration',
        executable='integration_pipeline',
        name='vla_humanoid_integrator',
        parameters=[{
            'use_sim_time': use_sim_time
        }],
        output='screen'
    )

    # Safety manager
    safety_node = Node(
        package='vla_humanoid_integration',
        executable='safety_manager',
        name='safety_manager',
        parameters=[{
            'use_sim_time': use_sim_time
        }],
        output='screen'
    )

    # Example publisher
    example_publisher = Node(
        package='vla_humanoid_integration',
        executable='example_publisher',
        name='example_publisher',
        parameters=[{
            'use_sim_time': use_sim_time
        }],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        integration_node,
        safety_node,
        example_publisher
    ])
```

## Step 5: Create the Package Configuration

1. Update `vla_humanoid_integration/setup.py`:

```python
from setuptools import setup
from glob import glob
import os

package_name = 'vla_humanoid_integration'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='VLA Humanoid Integration Pipeline',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'integration_pipeline = vla_humanoid_integration.integration_pipeline:main',
            'safety_manager = vla_humanoid_integration.safety_manager:main',
            'example_publisher = vla_humanoid_integration.example_publisher:main',
        ],
    },
)
```

2. Update `vla_humanoid_integration/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>vla_humanoid_integration</name>
  <version>0.1.0</version>
  <description>VLA Humanoid Integration Pipeline</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>builtin_interfaces</depend>
  <depend>launch</depend>
  <depend>launch_ros</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

## Step 6: Test the Integration System

1. Build the package:
   ```bash
   cd ~/vla_humanoid_integration_ws
   colcon build --packages-select vla_humanoid_integration
   source install/setup.bash
   ```

2. Run the integration system:
   ```bash
   ros2 launch vla_humanoid_integration integration_system.launch.py
   ```

## Step 7: Create a Complete Simulation Environment

For a more complete experience, create a simple simulation environment:

1. Create `simulation_test.py` in the project root:

```python
#!/usr/bin/env python3
"""
Complete test script for the VLA-Humanoid integration system.
This script simulates the complete pipeline from user instruction to robot behavior.
"""

import time
import threading
import queue
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class RobotState:
    """Represents the current state of the robot"""
    position: np.ndarray  # x, y, z
    orientation: np.ndarray  # roll, pitch, yaw
    joint_angles: Dict[str, float]  # joint name to angle
    is_safe: bool

class VLAParser:
    """Simple VLA parser for demonstration"""

    @staticmethod
    def parse_instruction(instruction: str) -> Dict[str, Any]:
        """Parse natural language instruction into structured command"""
        instruction_lower = instruction.lower()

        parsed = {
            'action_type': 'unknown',
            'target_location': None,
            'object_interaction': None,
            'required_locomotion': False,
            'confidence': 0.8  # Simulated confidence
        }

        if any(word in instruction_lower for word in ['move', 'go', 'walk', 'navigate']):
            parsed['action_type'] = 'navigation'
            parsed['required_locomotion'] = True

            if 'table' in instruction_lower:
                parsed['target_location'] = {'x': 2.0, 'y': 1.0, 'z': 0.0}
            elif 'kitchen' in instruction_lower:
                parsed['target_location'] = {'x': 3.0, 'y': -1.0, 'z': 0.0}
            elif 'door' in instruction_lower:
                parsed['target_location'] = {'x': 1.5, 'y': 0.5, 'z': 0.0}
            else:
                parsed['target_location'] = {'x': 1.0, 'y': 0.0, 'z': 0.0}

        elif any(word in instruction_lower for word in ['pick', 'grasp', 'grab', 'take']):
            parsed['action_type'] = 'manipulation'
            parsed['object_interaction'] = 'grasp'

        elif any(word in instruction_lower for word in ['place', 'put', 'drop', 'set']):
            parsed['action_type'] = 'manipulation'
            parsed['object_interaction'] = 'place'

        elif any(word in instruction_lower for word in ['look', 'turn', 'face']):
            parsed['action_type'] = 'orientation'

        return parsed

class KinematicsPlanner:
    """Plan kinematic movements for the robot"""

    def plan_manipulation(self, action: str) -> List[Dict[str, Any]]:
        """Plan arm movements for manipulation tasks"""
        if action == 'grasp':
            return [
                {'joint': 'left_shoulder', 'target': 0.5, 'duration': 1.0},
                {'joint': 'left_elbow', 'target': 0.3, 'duration': 1.0},
                {'joint': 'gripper', 'target': 0.0, 'duration': 0.5},  # Close gripper
            ]
        elif action == 'place':
            return [
                {'joint': 'gripper', 'target': 1.0, 'duration': 0.5},  # Open gripper
                {'joint': 'left_shoulder', 'target': 0.0, 'duration': 1.0},
                {'joint': 'left_elbow', 'target': 0.0, 'duration': 1.0},
            ]
        else:
            return []

class LocomotionPlanner:
    """Plan locomotion for the robot"""

    def plan_navigation(self, target: Dict[str, float], current_pos: np.ndarray) -> List[Dict[str, Any]]:
        """Plan walking trajectory to target location"""
        # Simple straight-line path
        dx = target['x'] - current_pos[0]
        dy = target['y'] - current_pos[1]
        distance = np.sqrt(dx**2 + dy**2)

        # Break into steps
        steps = []
        num_steps = max(1, int(distance / 0.1))  # 10cm steps

        for i in range(1, num_steps + 1):
            fraction = i / num_steps
            step_x = current_pos[0] + dx * fraction
            step_y = current_pos[1] + dy * fraction

            steps.append({
                'position': np.array([step_x, step_y, 0.0]),
                'duration': 0.5  # 0.5 seconds per step
            })

        return steps

class SafetyMonitor:
    """Monitor safety conditions"""

    def __init__(self):
        self.is_safe = True
        self.emergency_stop = False
        self.obstacle_detected = False

    def check_safety(self, robot_state: RobotState) -> bool:
        """Check if current robot state is safe"""
        # Simple safety checks
        if robot_state.position[2] < -0.1:  # Too low (fell over)
            self.is_safe = False
            return False

        # Simulate obstacle detection
        if np.random.random() < 0.05:  # 5% chance of obstacle
            self.obstacle_detected = True
            self.is_safe = False
            print("⚠️  Obstacle detected! Safety system activated.")
            return False

        self.is_safe = True
        self.obstacle_detected = False
        return True

class IntegrationSystem:
    """Main integration system that connects all components"""

    def __init__(self):
        self.vla_parser = VLAParser()
        self.kinematics_planner = KinematicsPlanner()
        self.locomotion_planner = LocomotionPlanner()
        self.safety_monitor = SafetyMonitor()

        self.current_state = RobotState(
            position=np.array([0.0, 0.0, 0.0]),
            orientation=np.array([0.0, 0.0, 0.0]),
            joint_angles={'left_shoulder': 0.0, 'left_elbow': 0.0, 'gripper': 1.0},
            is_safe=True
        )

        self.instruction_queue = queue.Queue()
        self.is_running = False

    def process_instruction(self, instruction: str):
        """Process a single instruction through the complete pipeline"""
        print(f"\n🤖 Processing instruction: '{instruction}'")

        # Step 1: Parse the instruction using VLA
        print("  → Parsing instruction with VLA system...")
        parsed_action = self.vla_parser.parse_instruction(instruction)
        print(f"  → Parsed action: {parsed_action}")

        # Step 2: Check safety
        print("  → Checking safety conditions...")
        if not self.safety_monitor.check_safety(self.current_state):
            print("  ❌ Safety check failed, aborting execution")
            return False

        # Step 3: Plan the behavior
        print("  → Planning behavior...")
        execution_plan = []

        # Plan locomotion if needed
        if parsed_action['required_locomotion'] and parsed_action['target_location']:
            print("  → Planning locomotion to target...")
            loco_plan = self.locomotion_planner.plan_navigation(
                parsed_action['target_location'],
                self.current_state.position
            )
            execution_plan.extend([('locomotion', step) for step in loco_plan])

        # Plan manipulation if needed
        if parsed_action['action_type'] == 'manipulation' and parsed_action['object_interaction']:
            print("  → Planning manipulation...")
            kin_plan = self.kinematics_planner.plan_manipulation(
                parsed_action['object_interaction']
            )
            execution_plan.extend([('manipulation', step) for step in kin_plan])

        # Step 4: Execute the plan
        print("  → Executing plan...")
        success = self.execute_plan(execution_plan)

        if success:
            print(f"  ✅ Instruction '{instruction}' completed successfully!")
        else:
            print(f"  ❌ Instruction '{instruction}' failed!")

        return success

    def execute_plan(self, plan: List[tuple]) -> bool:
        """Execute the planned behavior sequence"""
        for action_type, action in plan:
            if not self.safety_monitor.check_safety(self.current_state):
                print("  ❌ Safety check failed during execution, stopping")
                return False

            if action_type == 'locomotion':
                self.execute_locomotion_step(action)
            elif action_type == 'manipulation':
                self.execute_manipulation_step(action)

            time.sleep(0.1)  # Small delay between actions

        return True

    def execute_locomotion_step(self, step: Dict[str, Any]):
        """Execute a single locomotion step"""
        print(f"    → Moving to position {step['position'][:2]}")
        self.current_state.position = step['position']
        time.sleep(step['duration'])

    def execute_manipulation_step(self, step: Dict[str, Any]):
        """Execute a single manipulation step"""
        joint = step['joint']
        target = step['target']
        print(f"    → Moving {joint} to {target:.2f}")
        self.current_state.joint_angles[joint] = target
        time.sleep(step['duration'])

    def run_demo(self):
        """Run a demonstration of the complete system"""
        print("🚀 Starting VLA-Humanoid Integration Demo")
        print("=" * 50)

        # Example instructions to process
        instructions = [
            "Move to the table",
            "Pick up the red object",
            "Place the object on the shelf",
            "Go to the kitchen",
            "Turn around and look at the door"
        ]

        for instruction in instructions:
            success = self.process_instruction(instruction)
            time.sleep(1)  # Pause between instructions

        print("\n" + "=" * 50)
        print("✅ Demo completed!")
        print(f"Final robot position: {self.current_state.position}")
        print(f"Final joint angles: {self.current_state.joint_angles}")

def main():
    """Main function to run the integration demo"""
    system = IntegrationSystem()
    system.run_demo()

if __name__ == "__main__":
    main()
```

## Step 8: Run the Complete Integration Demo

1. Run the simulation test:
   ```bash
   python simulation_test.py
   ```

## Step 9: Extend the Implementation

Try extending the basic implementation with additional features:

1. Add more sophisticated VLA processing with real language models
2. Implement a more realistic kinematics solver with inverse kinematics
3. Add perception components to detect and identify objects
4. Implement a more advanced locomotion controller with ZMP-based balance

## Verification

To verify your implementation:

1. Confirm that the integration system properly connects all components
2. Verify that user instructions are correctly parsed and executed
3. Check that safety systems are properly integrated and responsive
4. Ensure that the complete pipeline works from instruction to behavior
5. Validate that the system handles both navigation and manipulation tasks

## Troubleshooting

- If the system doesn't respond to instructions, check ROS 2 communication between nodes
- If safety systems trigger incorrectly, adjust the safety thresholds
- If kinematic planning fails, verify the joint limits and configuration
- If locomotion planning is unstable, check the path planning algorithms

## Next Steps

This completes Module 4 of the Physical AI & Humanoid Robotics curriculum! You've now implemented a complete system that demonstrates:

- Vision-Language-Action systems for interpreting natural language instructions
- Humanoid kinematics for motion planning and control
- Bipedal locomotion for stable walking and navigation
- Complete system integration with safety considerations

You're now ready to explore advanced topics in humanoid robotics, including real-world deployment, advanced AI integration, and specialized applications in research and industry.