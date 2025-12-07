#!/usr/bin/env python3
"""
Mock VLA Pipeline Example
This demonstrates the basic concepts covered in Chapter 1: VLA Fundamentals
"""

import json
import time
from typing import Dict, Any, List

class MockVLAPipeline:
    """Mock Vision-Language-Action pipeline for educational purposes"""

    def __init__(self):
        self.action_templates = {
            "navigation": {
                "action_type": "navigation",
                "target_location": {"x": 0.0, "y": 0.0, "z": 0.0},
                "confidence": 0.8
            },
            "manipulation": {
                "action_type": "manipulation",
                "target_object": "unknown_object",
                "joint_commands": {},
                "confidence": 0.7
            },
            "perception": {
                "action_type": "perception",
                "target_object": "unknown_object",
                "confidence": 0.9
            }
        }

    def process_text_instruction(self, text_instruction: str) -> Dict[str, Any]:
        """
        Process natural language instruction and convert to structured robot command
        This is a mock implementation for educational purposes
        """
        print(f"Processing instruction: '{text_instruction}'")

        # Simple rule-based parsing for demonstration
        instruction_lower = text_instruction.lower()

        if any(word in instruction_lower for word in ['move', 'go', 'navigate', 'walk', 'to']):
            action_type = "navigation"
            target_location = self._extract_target_location(instruction_lower)

            command = self.action_templates["navigation"].copy()
            command["target_location"] = target_location
            command["confidence"] = 0.9

        elif any(word in instruction_lower for word in ['pick', 'grasp', 'grab', 'take']):
            action_type = "manipulation"
            target_object = self._extract_target_object(instruction_lower)

            command = self.action_templates["manipulation"].copy()
            command["target_object"] = target_object
            command["confidence"] = 0.8

        elif any(word in instruction_lower for word in ['look', 'see', 'find', 'detect']):
            action_type = "perception"
            target_object = self._extract_target_object(instruction_lower)

            command = self.action_templates["perception"].copy()
            command["target_object"] = target_object
            command["confidence"] = 0.95
        else:
            # Default to a general action
            command = self.action_templates["navigation"].copy()
            command["confidence"] = 0.6

        # Simulate processing time
        time.sleep(0.5)

        return {
            "original_instruction": text_instruction,
            "structured_command": command,
            "success": True,
            "message": f"Successfully parsed '{action_type}' command",
            "executed_commands": [f"execute_{action_type}_command()"]
        }

    def _extract_target_location(self, instruction: str) -> Dict[str, float]:
        """Extract target location from instruction (simplified for demo)"""
        # In a real system, this would use more sophisticated NLP
        if 'kitchen' in instruction:
            return {"x": 3.0, "y": -1.0, "z": 0.0}
        elif 'table' in instruction:
            return {"x": 2.0, "y": 1.0, "z": 0.0}
        elif 'door' in instruction:
            return {"x": 1.5, "y": 0.5, "z": 0.0}
        else:
            return {"x": 1.0, "y": 0.0, "z": 0.0}

    def _extract_target_object(self, instruction: str) -> str:
        """Extract target object from instruction (simplified for demo)"""
        # In a real system, this would use more sophisticated NLP
        if 'red' in instruction:
            return "red_object"
        elif 'blue' in instruction:
            return "blue_object"
        elif 'cup' in instruction:
            return "cup"
        elif 'box' in instruction:
            return "box"
        else:
            return "object"

def main():
    print("Mock VLA Pipeline Example")
    print("=" * 30)

    vla_pipeline = MockVLAPipeline()

    # Example instructions to process
    example_instructions = [
        "Move the robot to the table",
        "Pick up the red cup",
        "Look for the blue box in the kitchen",
        "Go to the door and wait there"
    ]

    for instruction in example_instructions:
        result = vla_pipeline.process_text_instruction(instruction)
        print(f"Result: {json.dumps(result, indent=2)}")
        print("-" * 50)

if __name__ == "__main__":
    main()