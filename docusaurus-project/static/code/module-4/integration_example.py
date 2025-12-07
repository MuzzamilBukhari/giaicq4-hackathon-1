#!/usr/bin/env python3
"""
Complete Integration Example
This demonstrates the concepts covered in Chapter 4: Integration & Deployment
"""

import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class RobotState:
    """Represents the current state of the robot"""
    position: Dict[str, float]  # x, y, z coordinates
    orientation: Dict[str, float]  # roll, pitch, yaw
    joint_angles: Dict[str, float]  # joint name to angle
    is_safe: bool

class VLAParser:
    """Process natural language instructions into structured commands"""

    @staticmethod
    def parse_instruction(instruction: str) -> Dict[str, Any]:
        """Parse natural language instruction into structured command"""
        instruction_lower = instruction.lower()

        parsed = {
            'action_type': 'unknown',
            'target_location': None,
            'target_object': None,
            'required_locomotion': False,
            'confidence': 0.8  # Default confidence
        }

        if any(word in instruction_lower for word in ['move', 'go', 'walk', 'navigate', 'to']):
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
            parsed['target_object'] = 'object'

        elif any(word in instruction_lower for word in ['place', 'put', 'set', 'drop']):
            parsed['action_type'] = 'manipulation'
            parsed['target_object'] = 'object'

        elif any(word in instruction_lower for word in ['look', 'see', 'find', 'detect']):
            parsed['action_type'] = 'perception'

        return parsed

class KinematicsPlanner:
    """Plan movements based on kinematic constraints"""

    def plan_movement(self, action_type: str, target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan the kinematic movements needed for the action"""
        if action_type == 'navigation':
            # Plan a path to the target location
            path = self._plan_navigation_path(target)
            return path
        elif action_type == 'manipulation':
            # Plan arm movements for manipulation
            movements = self._plan_manipulation(target)
            return movements
        else:
            return []

    def _plan_navigation_path(self, target: Dict[str, float]) -> List[Dict[str, Any]]:
        """Plan a simple path to target location"""
        # In a real system, this would use path planning algorithms like A* or RRT
        # For this example, we'll create a simple straight-line path
        path = [
            {'type': 'move_to', 'target': target, 'speed': 0.5},
            {'type': 'wait', 'duration': 1.0}
        ]
        return path

    def _plan_manipulation(self, target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan arm manipulation movements"""
        movements = [
            {'type': 'approach', 'target_object': target.get('target_object', 'unknown')},
            {'type': 'grasp', 'object': target.get('target_object', 'unknown')},
            {'type': 'lift', 'height': 0.1}
        ]
        return movements

class LocomotionController:
    """Control bipedal locomotion"""

    def __init__(self):
        self.com_height = 0.8  # Center of mass height
        self.is_balanced = True

    def execute_navigation(self, path: List[Dict[str, Any]]) -> bool:
        """Execute navigation along the planned path"""
        print("  → Executing navigation...")

        for step in path:
            if step['type'] == 'move_to':
                target = step['target']
                print(f"    Moving to position: ({target['x']}, {target['y']}, {target['z']})")
                # Simulate movement
                time.sleep(0.5)
            elif step['type'] == 'wait':
                print(f"    Waiting for {step['duration']} seconds")
                time.sleep(step['duration'])

        print("  → Navigation completed")
        return True

    def check_balance(self) -> bool:
        """Check if the robot is currently balanced"""
        # In a real system, this would check ZMP, joint angles, etc.
        # For this example, we'll just return True
        return self.is_balanced

    def adjust_balance(self) -> bool:
        """Adjust robot's balance if needed"""
        if not self.is_balanced:
            print("  → Adjusting balance...")
            # Simulate balance adjustment
            time.sleep(0.2)
            self.is_balanced = True
            print("  → Balance restored")
            return True
        return True

class SafetyMonitor:
    """Monitor safety conditions"""

    def __init__(self):
        self.is_safe = True
        self.emergency_stop = False

    def check_safety(self, robot_state: RobotState) -> bool:
        """Check if current robot state is safe"""
        # Check for various safety conditions
        if not robot_state.is_safe:
            self.is_safe = False
            self.emergency_stop = True
            return False

        # Check for balance issues
        if robot_state.position.get('z', 0) < -0.1:  # Robot has fallen
            self.is_safe = False
            self.emergency_stop = True
            print("  ⚠️  Safety: Robot appears to have fallen, emergency stop activated")
            return False

        # Check for joint limit violations
        for joint_name, angle in robot_state.joint_angles.items():
            if abs(angle) > 3.14:  # Exceeding joint limits (π radians)
                self.is_safe = False
                self.emergency_stop = True
                print(f"  ⚠️  Safety: Joint {joint_name} limit exceeded, emergency stop activated")
                return False

        self.is_safe = True
        self.emergency_stop = False
        return True

class IntegrationPipeline:
    """Complete integration pipeline connecting all components"""

    def __init__(self):
        self.vla_parser = VLAParser()
        self.kinematics_planner = KinematicsPlanner()
        self.locomotion_controller = LocomotionController()
        self.safety_monitor = SafetyMonitor()

        # Initial robot state
        self.current_state = RobotState(
            position={'x': 0.0, 'y': 0.0, 'z': 0.0},
            orientation={'roll': 0.0, 'pitch': 0.0, 'yaw': 0.0},
            joint_angles={'left_hip': 0.0, 'right_hip': 0.0, 'left_knee': 0.0, 'right_knee': 0.0},
            is_safe=True
        )

    def execute_instruction(self, instruction: str) -> Dict[str, Any]:
        """Execute a complete instruction from user to robot behavior"""
        print(f"\n🤖 Processing instruction: '{instruction}'")

        # Step 1: Parse the instruction using VLA
        print("  → Parsing instruction with VLA system...")
        parsed_action = self.vla_parser.parse_instruction(instruction)
        print(f"  → Parsed action: {parsed_action}")

        # Step 2: Check safety
        print("  → Checking safety conditions...")
        if not self.safety_monitor.check_safety(self.current_state):
            print("  ❌ Safety check failed, aborting execution")
            return {
                'success': False,
                'message': 'Safety check failed',
                'executed_commands': []
            }

        # Step 3: Plan the kinematic movements
        print("  → Planning kinematic movements...")
        movement_plan = self.kinematics_planner.plan_movement(
            parsed_action['action_type'],
            parsed_action
        )
        print(f"  → Planned {len(movement_plan)} movement steps")

        # Step 4: Execute the plan
        print("  → Executing plan...")
        executed_commands = []

        if parsed_action['required_locomotion'] and parsed_action.get('target_location'):
            print("  → Executing navigation...")
            nav_success = self.locomotion_controller.execute_navigation(movement_plan)
            if nav_success:
                executed_commands.extend([step['type'] for step in movement_plan])
                print("  → Navigation completed successfully")
            else:
                print("  ❌ Navigation failed")
                return {
                    'success': False,
                    'message': 'Navigation failed',
                    'executed_commands': executed_commands
                }
        else:
            print("  → Executing manipulation...")
            for movement in movement_plan:
                executed_commands.append(movement['type'])
                print(f"    - Executing: {movement['type']}")
                time.sleep(0.2)  # Simulate execution time

        # Step 5: Final safety check
        print("  → Performing final safety check...")
        final_safe = self.safety_monitor.check_safety(self.current_state)

        result = {
            'success': final_safe,
            'message': f"Successfully executed '{parsed_action['action_type']}' action" if final_safe else "Execution completed but safety issues detected",
            'executed_commands': executed_commands,
            'parsed_action': parsed_action
        }

        print(f"  ✅ Instruction completed with result: {result['message']}")
        return result

def main():
    print("Complete Integration Pipeline Example")
    print("=" * 45)

    # Create the integration pipeline
    pipeline = IntegrationPipeline()

    # Example instructions to process
    example_instructions = [
        "Move the robot to the table",
        "Pick up the red object",
        "Go to the kitchen and look around",
        "Place the object on the shelf"
    ]

    all_results = []

    for instruction in example_instructions:
        result = pipeline.execute_instruction(instruction)
        all_results.append(result)
        print(f"  Result: {result['message']}")
        print("-" * 50)

    # Summary
    print("\n📊 Execution Summary:")
    successful = sum(1 for r in all_results if r['success'])
    total = len(all_results)
    print(f"  Successful executions: {successful}/{total}")

    print("\n🔧 Pipeline Components:")
    print("  - VLA System: Processes natural language to structured commands")
    print("  - Kinematics Planner: Plans joint movements and paths")
    print("  - Locomotion Controller: Handles walking and balance")
    print("  - Safety Monitor: Ensures safe operation throughout")
    print("  - Integration Layer: Coordinates all components")

    print("\n✅ Integration Pipeline Complete!")

if __name__ == "__main__":
    main()