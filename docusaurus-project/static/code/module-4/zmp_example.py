#!/usr/bin/env python3
"""
Simple ZMP (Zero Moment Point) Example
This demonstrates the basic concepts covered in Chapter 3: Bipedal Locomotion
"""

import numpy as np
import matplotlib.pyplot as plt

class ZMPCalculator:
    """Simple ZMP calculator for educational purposes"""

    def __init__(self, com_height=0.8):
        """
        Initialize ZMP calculator
        com_height: Center of mass height in meters
        """
        self.com_height = com_height
        self.gravity = 9.81  # m/s^2

    def calculate_zmp_simple(self, com_x, com_y, com_acc_x=0, com_acc_y=0):
        """
        Calculate ZMP position from CoM position and acceleration
        This is a simplified version for educational purposes
        """
        # ZMP_x = CoM_x - (CoM_height / gravity) * CoM_acc_x
        # ZMP_y = CoM_y - (CoM_height / gravity) * CoM_acc_y
        zmp_x = com_x - (self.com_height / self.gravity) * com_acc_x
        zmp_y = com_y - (self.com_height / self.gravity) * com_acc_y

        return zmp_x, zmp_y

    def is_stable(self, zmp_x, zmp_y, support_polygon_x, support_polygon_y):
        """
        Check if the robot is stable based on ZMP position
        support_polygon_x, support_polygon_y: vertices of the support polygon
        """
        # Simple check: is ZMP within the bounding box of the support polygon
        min_x, max_x = min(support_polygon_x), max(support_polygon_x)
        min_y, max_y = min(support_polygon_y), max(support_polygon_y)

        return min_x <= zmp_x <= max_x and min_y <= zmp_y <= max_y

def plot_zmp_stability(com_x, com_y, zmp_x, zmp_y, support_polygon_x, support_polygon_y):
    """Plot ZMP and support polygon for visualization"""
    plt.figure(figsize=(10, 8))

    # Plot support polygon
    plt.fill(support_polygon_x + [support_polygon_x[0]],
             support_polygon_y + [support_polygon_y[0]],
             alpha=0.3, color='green', label='Support Polygon')

    # Plot CoM
    plt.plot(com_x, com_y, 'ro', markersize=10, label=f'CoM ({com_x:.2f}, {com_y:.2f})')

    # Plot ZMP
    plt.plot(zmp_x, zmp_y, 'bo', markersize=10, label=f'ZMP ({zmp_x:.2f}, {zmp_y:.2f})')

    # Connect CoM and ZMP with a line
    plt.plot([com_x, zmp_x], [com_y, zmp_y], 'k--', alpha=0.5, label='CoM to ZMP')

    plt.grid(True)
    plt.axis('equal')
    plt.title('ZMP and Stability Analysis')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.legend()
    plt.show()

def main():
    print("Simple ZMP Example")
    print("=" * 30)

    zmp_calc = ZMPCalculator(com_height=0.85)  # Typical humanoid CoM height

    # Example 1: Stable position
    print("\n1. Stable Position Example:")
    com_x, com_y = 0.0, 0.0  # CoM at origin
    com_acc_x, com_acc_y = 0.0, 0.0  # No acceleration

    zmp_x, zmp_y = zmp_calc.calculate_zmp_simple(com_x, com_y, com_acc_x, com_acc_y)
    print(f"   CoM position: ({com_x}, {com_y})")
    print(f"   CoM acceleration: ({com_acc_x}, {com_acc_y})")
    print(f"   ZMP position: ({zmp_x:.3f}, {zmp_y:.3f})")

    # Define a simple rectangular support polygon (feet positions)
    support_polygon_x = [-0.1, 0.2, 0.2, -0.1]  # Rectangle from x=-0.1 to x=0.2
    support_polygon_y = [-0.1, -0.1, 0.1, 0.1]  # Rectangle from y=-0.1 to y=0.1

    is_stable = zmp_calc.is_stable(zmp_x, zmp_y, support_polygon_x, support_polygon_y)
    print(f"   Is stable: {is_stable}")
    print(f"   Support polygon: X=[{min(support_polygon_x)}, {max(support_polygon_x)}], Y=[{min(support_polygon_y)}, {max(support_polygon_y)}]")

    # Example 2: Unstable position (ZMP outside support polygon)
    print("\n2. Unstable Position Example:")
    com_x_unstable, com_y_unstable = 0.5, 0.0  # CoM shifted outside support area
    com_acc_x_unstable, com_acc_y_unstable = 0.5, 0.0  # Acceleration pushing further

    zmp_x_unstable, zmp_y_unstable = zmp_calc.calculate_zmp_simple(
        com_x_unstable, com_y_unstable, com_acc_x_unstable, com_acc_y_unstable
    )
    print(f"   CoM position: ({com_x_unstable}, {com_y_unstable})")
    print(f"   CoM acceleration: ({com_acc_x_unstable}, {com_acc_y_unstable})")
    print(f"   ZMP position: ({zmp_x_unstable:.3f}, {zmp_y_unstable:.3f})")

    is_stable_unstable = zmp_calc.is_stable(
        zmp_x_unstable, zmp_y_unstable, support_polygon_x, support_polygon_y
    )
    print(f"   Is stable: {is_stable_unstable}")

    # Optional: Plot the results
    plot_choice = input("\nWould you like to see a visualization? (y/n): ")
    if plot_choice.lower() == 'y':
        plot_zmp_stability(
            com_x, com_y, zmp_x, zmp_y,
            support_polygon_x, support_polygon_y
        )

if __name__ == "__main__":
    main()