#!/usr/bin/env python3
"""
Simple Forward and Inverse Kinematics Example
This demonstrates the basic concepts covered in Chapter 2: Humanoid Kinematics
"""

import numpy as np
import math

class SimpleKinematics:
    """Simple 2D kinematics example for educational purposes"""

    def __init__(self):
        # Link lengths for a simple 2-link arm
        self.l1 = 1.0  # Length of first link
        self.l2 = 0.8  # Length of second link

    def forward_kinematics(self, theta1, theta2):
        """
        Calculate end-effector position from joint angles
        theta1, theta2: Joint angles in radians
        Returns: (x, y) position of end-effector
        """
        x = self.l1 * math.cos(theta1) + self.l2 * math.cos(theta1 + theta2)
        y = self.l1 * math.sin(theta1) + self.l2 * math.sin(theta1 + theta2)
        return x, y

    def inverse_kinematics(self, x, y):
        """
        Calculate joint angles from end-effector position
        x, y: Desired end-effector position
        Returns: (theta1, theta2) joint angles or None if position is unreachable
        """
        # Calculate distance from origin to target
        r = math.sqrt(x**2 + y**2)

        # Check if target is reachable
        if r > self.l1 + self.l2:
            print(f"Target ({x}, {y}) is out of reach. Max reach: {self.l1 + self.l2}")
            return None

        if r < abs(self.l1 - self.l2):
            print(f"Target ({x}, {y}) is too close. Min reach: {abs(self.l1 - self.l2)}")
            return None

        # Calculate theta2 using law of cosines
        cos_theta2 = (self.l1**2 + self.l2**2 - r**2) / (2 * self.l1 * self.l2)
        theta2 = math.acos(max(-1, min(1, cos_theta2)))  # Clamp to [-1, 1] to avoid numerical errors

        # Calculate theta1
        k1 = self.l1 + self.l2 * math.cos(theta2)
        k2 = self.l2 * math.sin(theta2)

        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        return theta1, theta2

def main():
    print("Simple Kinematics Example")
    print("=" * 30)

    kin = SimpleKinematics()

    # Example 1: Forward Kinematics
    print("\n1. Forward Kinematics Example:")
    theta1, theta2 = math.pi/4, math.pi/6  # 45° and 30°
    x, y = kin.forward_kinematics(theta1, theta2)
    print(f"   Joint angles: θ1={theta1:.3f} rad ({math.degrees(theta1):.1f}°), θ2={theta2:.3f} rad ({math.degrees(theta2):.1f}°)")
    print(f"   End-effector position: ({x:.3f}, {y:.3f})")

    # Example 2: Inverse Kinematics
    print("\n2. Inverse Kinematics Example:")
    target_x, target_y = 1.2, 1.0
    solution = kin.inverse_kinematics(target_x, target_y)

    if solution:
        theta1_sol, theta2_sol = solution
        print(f"   Target position: ({target_x}, {target_y})")
        print(f"   Solution: θ1={theta1_sol:.3f} rad ({math.degrees(theta1_sol):.1f}°), θ2={theta2_sol:.3f} rad ({math.degrees(theta2_sol):.1f}°)")

        # Verify by running forward kinematics on the solution
        x_verify, y_verify = kin.forward_kinematics(theta1_sol, theta2_sol)
        print(f"   Verification - FK on solution: ({x_verify:.3f}, {y_verify:.3f})")
        print(f"   Error: {math.sqrt((target_x - x_verify)**2 + (target_y - y_verify)**2):.6f}")

if __name__ == "__main__":
    main()