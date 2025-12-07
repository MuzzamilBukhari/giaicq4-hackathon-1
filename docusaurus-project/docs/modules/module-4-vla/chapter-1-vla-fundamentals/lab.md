---
id: chapter-1-vla-fundamentals-lab
title: Lab - Build a Simple VLA Text-to-Action Simulation Pipeline
sidebar_label: "Lab: VLA Text-to-Action Pipeline"
---

# Lab: Build a Simple VLA Text-to-Action Simulation Pipeline

## Overview

In this lab, you will create a basic Vision-Language-Action (VLA) pipeline that takes a text instruction and translates it into a simulated robot action. This exercise demonstrates the fundamental concepts of how language models can be integrated with robotic systems to perform simple tasks.

## Learning Objectives

- Understand the basic components of a VLA system
- Implement a simple text-to-action pipeline
- Simulate the execution of VLA commands in a virtual environment

## Prerequisites

- ROS 2 Humble installed and configured
- Gazebo or Isaac Sim simulation environment
- Basic Python programming knowledge
- Understanding of ROS 2 message types

## Estimated Time

60-90 minutes

## Setup

1. Ensure your ROS 2 environment is sourced:
   ```bash
   source /opt/ros/humble/setup.bash
   source install/setup.bash  # If you have a workspace
   ```

2. Create a new workspace for this lab:
   ```bash
   mkdir -p ~/vla_lab_ws/src
   cd ~/vla_lab_ws
   ```

## Step 1: Define the Action Message

First, let's define a simple ROS 2 action message that will represent our VLA commands:

1. Create a new package for our action definitions:
   ```bash
   cd src
   ros2 pkg create --build-type ament_python vla_msgs
   ```

2. In the `vla_msgs` package, create an `action` directory and define our action:
   ```bash
   mkdir vla_msgs/action
   ```

3. Create the action definition file `TextToAction.action`:
   ```
   # Goal: The text instruction to execute
   string text_instruction
   ---
   # Result: The outcome of the action
   bool success
   string message
   ---
   # Feedback: Progress information during execution
   string current_step
   float32 progress
   ```

4. Update the `setup.py` file to include the action:

## Step 2: Create the VLA Processing Node

Now, let's create a ROS 2 node that will process text instructions and convert them to robot actions:

1. Create the VLA processing node:
   ```bash
   mkdir -p vla_msgs/vla_nodes
   touch vla_msgs/vla_nodes/__init__.py
   ```

2. Create the main VLA processing file `vla_processor.py`:
   ```python
   import rclpy
   from rclpy.action import ActionServer
   from rclpy.node import Node
   import re
   from vla_msgs.action import TextToAction

   class VLAProcessor(Node):
       def __init__(self):
           super().__init__('vla_processor')
           self._action_server = ActionServer(
               self,
               TextToAction,
               'process_text_action',
               self.execute_callback)

       def execute_callback(self, goal_handle):
           self.get_logger().info(f'Processing instruction: {goal_handle.request.text_instruction}')

           # Simple rule-based text processing (in a real system, this would use an LLM)
           feedback_msg = TextToAction.Feedback()
           feedback_msg.current_step = "Parsing instruction"
           feedback_msg.progress = 0.1
           goal_handle.publish_feedback(feedback_msg)

           # Extract action and target from text
           instruction = goal_handle.request.text_instruction.lower()
           action = self.parse_action(instruction)
           target = self.parse_target(instruction)

           feedback_msg.current_step = f"Action: {action}, Target: {target}"
           feedback_msg.progress = 0.3
           goal_handle.publish_feedback(feedback_msg)

           # Simulate action execution
           success = self.execute_simulated_action(action, target)

           feedback_msg.current_step = "Action completed"
           feedback_msg.progress = 0.9
           goal_handle.publish_feedback(feedback_msg)

           result = TextToAction.Result()
           result.success = success
           result.message = f"Executed {action} on {target}" if success else "Action failed"

           goal_handle.succeed()
           return result

       def parse_action(self, instruction):
           # Simple keyword matching for demonstration
           if 'move' in instruction or 'go to' in instruction:
               return 'move_to'
           elif 'pick' in instruction or 'grasp' in instruction:
               return 'grasp'
           elif 'place' in instruction or 'put' in instruction:
               return 'place'
           else:
               return 'unknown'

       def parse_target(self, instruction):
           # Simple target extraction for demonstration
           if 'table' in instruction:
               return 'table'
           elif 'box' in instruction:
               return 'box'
           elif 'shelf' in instruction:
               return 'shelf'
           elif 'object' in instruction:
               return 'object'
           else:
               return 'default'

       def execute_simulated_action(self, action, target):
           # Simulate action execution (in a real system, this would interface with simulation/robot)
           self.get_logger().info(f'Simulating {action} on {target}')
           # Simulate some processing time
           import time
           time.sleep(2)
           return True

   def main(args=None):
       rclpy.init(args=args)
       vla_processor = VLAProcessor()
       rclpy.spin(vla_processor)
       vla_processor.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

## Step 3: Create a Simulation Interface

Let's create a simple simulation interface that will respond to our VLA commands:

1. Create `simulation_interface.py`:
   ```python
   import rclpy
   from rclpy.node import Node
   from std_msgs.msg import String
   from geometry_msgs.msg import Pose
   import json

   class SimulationInterface(Node):
       def __init__(self):
           super().__init__('simulation_interface')
           self.publisher = self.create_publisher(String, 'simulation_commands', 10)
           self.subscription = self.create_subscription(
               String,
               'vla_results',
               self.listener_callback,
               10)
           self.get_logger().info('Simulation interface started')

       def listener_callback(self, msg):
           self.get_logger().info(f'Simulation received: {msg.data}')

   def main(args=None):
       rclpy.init(args=args)
       sim_interface = SimulationInterface()
       rclpy.spin(sim_interface)
       sim_interface.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

## Step 4: Test the Pipeline

1. Build your package:
   ```bash
   cd ~/vla_lab_ws
   colcon build --packages-select vla_msgs
   source install/setup.bash
   ```

2. In one terminal, start the VLA processor:
   ```bash
   ros2 run vla_msgs vla_processor
   ```

3. In another terminal, send a test action goal:
   ```bash
   ros2 action send_goal /process_text_action vla_msgs/action/TextToAction "{text_instruction: 'Move the robot to the table'}"
   ```

## Step 5: Extend the Pipeline

Try extending the basic pipeline with additional features:

1. Add more sophisticated text parsing
2. Implement a simple state machine for the robot
3. Add error handling for unrecognized instructions
4. Create a visualization for the action execution

## Verification

To verify your implementation:

1. Confirm that the action server starts without errors
2. Verify that you can send text instructions and receive responses
3. Check that the progress feedback is published during execution
4. Ensure that both success and failure cases are handled properly

## Troubleshooting

- If the action server doesn't start, check that your package is properly built and sourced
- If actions fail, verify that the action definition matches between client and server
- If feedback isn't published, check that the action client is properly configured

## Next Steps

In the next lab, you'll apply these VLA concepts to more complex humanoid kinematics problems, connecting language-based instructions to specific joint movements and task planning.