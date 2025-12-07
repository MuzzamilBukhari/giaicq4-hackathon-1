---
id: chapter-2-humanoid-kinematics-lab
title: Lab - Implement FK/IK for a Simplified Humanoid Arm or Leg Model
sidebar_label: "Lab: FK/IK Implementation"
---

# Lab: Implement FK/IK for a Simplified Humanoid Arm or Leg Model

## Overview

In this lab, you will implement Forward Kinematics (FK) and Inverse Kinematics (IK) for a simplified humanoid arm or leg model. You will use the Denavit-Hartenberg (DH) parameters to model the kinematic chain and implement both FK and IK solutions using mathematical approaches.

## Learning Objectives

- Implement Forward Kinematics for a simple robotic arm/leg
- Implement Inverse Kinematics for position control
- Understand the relationship between joint space and Cartesian space
- Apply DH parameters to model a kinematic chain

## Prerequisites

- Basic knowledge of linear algebra (matrices, transformations)
- Understanding of trigonometry
- Python programming experience
- Basic understanding of robotics kinematics concepts

## Estimated Time

90-120 minutes

## Setup

1. Create a new directory for this lab:
   ```bash
   mkdir -p ~/kinematics_lab
   cd ~/kinematics_lab
   ```

2. Create a Python file for our kinematics implementation:
   ```bash
   touch kinematics.py
   ```

## Step 1: Create the DH Parameter Model

First, let's create a simple 3-DOF planar arm model using DH parameters:

1. Open `kinematics.py` and add the following code:

```python
import numpy as np
import math
from typing import List, Tuple

class DHParameter:
    """Class to represent Denavit-Hartenberg parameters for a joint"""
    def __init__(self, a: float, alpha: float, d: float, theta: float):
        self.a = a      # Link length
        self.alpha = alpha  # Link twist
        self.d = d      # Link offset
        self.theta = theta  # Joint angle

class PlanarArm:
    """Simple 3-DOF planar arm for kinematics demonstration"""

    def __init__(self):
        # Define DH parameters for a simple 3-DOF planar arm
        # Joint 1: Revolute joint
        self.dh_params = [
            DHParameter(a=1.0, alpha=0.0, d=0.0, theta=0.0),  # Joint 1
            DHParameter(a=1.0, alpha=0.0, d=0.0, theta=0.0),  # Joint 2
            DHParameter(a=0.5, alpha=0.0, d=0.0, theta=0.0),  # Joint 3
        ]
        self.joint_angles = [0.0, 0.0, 0.0]  # Initial joint angles

    def dh_transform(self, dh: DHParameter) -> np.ndarray:
        """Calculate the transformation matrix for a single DH parameter set"""
        c_theta = math.cos(dh.theta)
        s_theta = math.sin(dh.theta)
        c_alpha = math.cos(dh.alpha)
        s_alpha = math.sin(dh.alpha)

        transform = np.array([
            [c_theta, -s_theta * c_alpha, s_theta * s_alpha, dh.a * c_theta],
            [s_theta, c_theta * c_alpha, -c_theta * s_alpha, dh.a * s_theta],
            [0, s_alpha, c_alpha, dh.d],
            [0, 0, 0, 1]
        ])
        return transform

    def forward_kinematics(self, joint_angles: List[float] = None) -> Tuple[np.ndarray, List[np.ndarray]]:
        """Calculate forward kinematics to get end-effector position"""
        if joint_angles is None:
            joint_angles = self.joint_angles

        # Update DH parameters with current joint angles
        current_dh = []
        for i, dh in enumerate(self.dh_params):
            new_dh = DHParameter(dh.a, dh.alpha, dh.d, dh.theta + joint_angles[i])
            current_dh.append(new_dh)

        # Calculate transformation matrices for each joint
        transforms = []
        cumulative_transform = np.eye(4)

        for dh in current_dh:
            t = self.dh_transform(dh)
            cumulative_transform = cumulative_transform @ t
            transforms.append(cumulative_transform.copy())

        # End-effector position is the translation part of the final transform
        end_effector_pos = cumulative_transform[:3, 3]

        return end_effector_pos, transforms

    def jacobian(self, joint_angles: List[float] = None) -> np.ndarray:
        """Calculate the Jacobian matrix for the arm"""
        if joint_angles is None:
            joint_angles = self.joint_angles

        # Get all transforms
        _, transforms = self.forward_kinematics(joint_angles)

        # Calculate end-effector position
        end_effector_pos = transforms[-1][:3, 3]

        # Initialize Jacobian (3x3 for planar arm - x, y, theta)
        jacobian = np.zeros((3, 3))

        for i in range(3):
            # Get the z-axis of joint i (rotation axis)
            z_i = transforms[i][:3, 2]  # Third column is the z-axis

            # Get the position of joint i
            if i == 0:
                joint_pos = np.array([0, 0, 0])
            else:
                joint_pos = transforms[i-1][:3, 3]

            # Calculate the vector from joint i to end-effector
            r = end_effector_pos - joint_pos

            # For revolute joints, the Jacobian column is [z_i × r; z_i]
            # For planar arm, we only care about x, y, theta (not z rotation)
            jacobian[:2, i] = np.cross(z_i[:2], r[:2])  # Linear velocity part
            jacobian[2, i] = z_i[2]  # Angular velocity part (about z-axis)

        return jacobian

    def inverse_kinematics_analytical(self, target_pos: np.ndarray,
                                    initial_angles: List[float] = None) -> Tuple[List[float], bool]:
        """Solve inverse kinematics using analytical method for planar arm"""
        if initial_angles is None:
            initial_angles = [0.0, 0.0, 0.0]

        x, y, _ = target_pos

        # For a 3-DOF planar arm, we'll solve for the first 2 joints analytically
        # and set the third joint to achieve desired orientation
        l1 = self.dh_params[0].a
        l2 = self.dh_params[1].a
        l3 = self.dh_params[2].a  # For orientation

        # Calculate distance from origin to target
        r = math.sqrt(x**2 + y**2)

        # Check if target is reachable
        if r > l1 + l2:
            print(f"Target {target_pos} is out of reach. Max reach: {l1 + l2}")
            return initial_angles, False

        if r < abs(l1 - l2):
            print(f"Target {target_pos} is too close. Min reach: {abs(l1 - l2)}")
            return initial_angles, False

        # Calculate joint angles using law of cosines
        # Angle of the second joint
        cos_theta2 = (l1**2 + l2**2 - r**2) / (2 * l1 * l2)
        theta2 = math.acos(max(-1, min(1, cos_theta2)))  # Clamp to [-1, 1] to avoid numerical errors

        # Calculate angle of the first joint
        k1 = l1 + l2 * math.cos(theta2)
        k2 = l2 * math.sin(theta2)

        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # For the third joint, we'll set it to achieve a specific orientation
        # For simplicity, let's set it to achieve a specific end-effector angle
        theta3 = 0.0  # We can adjust this based on desired orientation

        solution = [theta1, theta2, theta3]
        return solution, True

def test_kinematics():
    """Test function to demonstrate FK and IK"""
    arm = PlanarArm()

    print("=== Forward Kinematics Test ===")

    # Test with some joint angles
    test_angles = [math.pi/4, math.pi/6, math.pi/3]  # 45°, 30°, 60°

    end_pos, transforms = arm.forward_kinematics(test_angles)
    print(f"Joint angles: {test_angles}")
    print(f"End-effector position: {end_pos}")

    print("\n=== Jacobian Test ===")
    jacobian = arm.jacobian(test_angles)
    print(f"Jacobian matrix:\n{jacobian}")

    print("\n=== Inverse Kinematics Test ===")
    target_pos = np.array([1.5, 1.0, 0.0])  # Target position

    ik_solution, success = arm.inverse_kinematics_analytical(target_pos)
    if success:
        print(f"Target position: {target_pos}")
        print(f"IK solution: {ik_solution}")

        # Verify by running FK with the IK solution
        fk_pos, _ = arm.forward_kinematics(ik_solution)
        print(f"Verification FK position: {fk_pos}")
        print(f"Distance from target: {np.linalg.norm(target_pos - fk_pos)}")
    else:
        print("IK solution failed - target may be unreachable")

if __name__ == "__main__":
    test_kinematics()
```

## Step 2: Create a Visualization Script

Create a visualization script to help understand the kinematic solutions:

1. Create `visualize_kinematics.py`:

```python
import matplotlib.pyplot as plt
import numpy as np
from kinematics import PlanarArm
import math

def plot_arm(arm: PlanarArm, joint_angles: list, title: str = "Robot Arm Configuration"):
    """Plot the robot arm in 2D"""
    end_pos, transforms = arm.forward_kinematics(joint_angles)

    # Extract joint positions
    joint_positions = []
    for t in transforms:
        joint_positions.append(t[:2, 3])  # x, y coordinates

    # Add base position (origin)
    joint_positions = [np.array([0, 0])] + joint_positions

    # Convert to numpy array for plotting
    positions = np.array(joint_positions)

    # Plot the arm
    plt.figure(figsize=(10, 8))
    plt.plot(positions[:, 0], positions[:, 1], 'bo-', linewidth=3, markersize=10, label='Arm links')
    plt.plot(positions[0, 0], positions[0, 1], 'go', markersize=12, label='Base')  # Base
    plt.plot(positions[-1, 0], positions[-1, 1], 'ro', markersize=12, label='End-effector')  # End-effector

    # Annotate joint angles
    for i, (x, y) in enumerate(positions):
        plt.annotate(f'J{i}', (x, y), xytext=(5, 5), textcoords='offset points')

    plt.grid(True)
    plt.axis('equal')
    plt.title(title)
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.legend()
    plt.show()

def plot_workspace(arm: PlanarArm, resolution: int = 50):
    """Plot the workspace of the arm"""
    l1 = arm.dh_params[0].a
    l2 = arm.dh_params[1].a
    l3 = arm.dh_params[2].a

    # Theoretical workspace boundaries
    max_radius = l1 + l2 + l3
    min_radius = abs(l1 - l2) - l3 if l3 < abs(l1 - l2) else 0

    # Create grid of points
    x = np.linspace(-max_radius, max_radius, resolution)
    y = np.linspace(-max_radius, max_radius, resolution)
    X, Y = np.meshgrid(x, y)

    # Calculate distance from origin for each point
    R = np.sqrt(X**2 + Y**2)

    # Create workspace mask (points within reach)
    workspace = (R >= min_radius) & (R <= max_radius)

    plt.figure(figsize=(10, 8))
    plt.contourf(X, Y, workspace, levels=1, colors=['lightblue'], alpha=0.5)
    plt.contour(X, Y, workspace, levels=[0.5], colors=['blue'], linewidths=2)

    # Draw theoretical boundaries
    theta = np.linspace(0, 2*np.pi, 100)
    x_max = max_radius * np.cos(theta)
    y_max = max_radius * np.sin(theta)
    plt.plot(x_max, y_max, 'b--', label=f'Max reach: {max_radius:.2f}')

    if min_radius > 0:
        x_min = min_radius * np.cos(theta)
        y_min = min_radius * np.sin(theta)
        plt.plot(x_min, y_min, 'b--', label=f'Min reach: {min_radius:.2f}')

    plt.grid(True)
    plt.axis('equal')
    plt.title('Robot Arm Workspace')
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.legend()
    plt.show()

def main():
    arm = PlanarArm()

    # Demonstrate FK
    joint_angles = [math.pi/4, math.pi/6, 0.0]
    plot_arm(arm, joint_angles, "Forward Kinematics - Joint Angles: [π/4, π/6, 0]")

    # Demonstrate IK
    target_pos = np.array([1.5, 1.0, 0.0])
    ik_solution, success = arm.inverse_kinematics_analytical(target_pos)

    if success:
        plot_arm(arm, ik_solution, f"Inverse Kinematics - Target: [{target_pos[0]:.1f}, {target_pos[1]:.1f}]")

    # Plot workspace
    plot_workspace(arm)

if __name__ == "__main__":
    main()
```

## Step 3: Create a More Advanced IK Solver

Create an iterative IK solver that can handle more complex scenarios:

1. Create `ik_iterative.py`:

```python
import numpy as np
from kinematics import PlanarArm
import math

class IterativeIK:
    """Iterative Inverse Kinematics solver using Jacobian transpose method"""

    def __init__(self, arm: PlanarArm, max_iterations: int = 100, tolerance: float = 1e-4):
        self.arm = arm
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def solve(self, target_pos: np.ndarray, initial_angles: list = None) -> tuple:
        """Solve IK using iterative method"""
        if initial_angles is None:
            current_angles = [0.0, 0.0, 0.0]
        else:
            current_angles = initial_angles.copy()

        for i in range(self.max_iterations):
            # Calculate current end-effector position
            current_pos, _ = self.arm.forward_kinematics(current_angles)

            # Calculate error
            error = target_pos[:2] - current_pos[:2]  # Only care about x, y for planar arm
            error_norm = np.linalg.norm(error)

            if error_norm < self.tolerance:
                print(f"IK solution found in {i+1} iterations")
                return current_angles, True

            # Calculate Jacobian
            jacobian = self.arm.jacobian(current_angles)

            # Use Jacobian transpose method for simple iterative solution
            # delta_theta = J^T * delta_x
            delta_theta = 0.1 * jacobian[:2, :].T @ error  # Scale down for stability

            # Update joint angles
            current_angles = [a + da for a, da in zip(current_angles, delta_theta)]

        print(f"IK solution did not converge after {self.max_iterations} iterations")
        return current_angles, False

def compare_solutions():
    """Compare analytical and iterative IK solutions"""
    arm = PlanarArm()
    iterative_ik = IterativeIK(arm)

    # Test target
    target_pos = np.array([1.2, 0.8, 0.0])

    print(f"Target position: {target_pos}")

    # Analytical solution
    analytical_solution, success_a = arm.inverse_kinematics_analytical(target_pos)
    if success_a:
        pos_a, _ = arm.forward_kinematics(analytical_solution)
        error_a = np.linalg.norm(target_pos[:2] - pos_a[:2])
        print(f"Analytical IK solution: {analytical_solution}")
        print(f"Analytical IK error: {error_a}")

    # Iterative solution
    iterative_solution, success_i = iterative_ik.solve(target_pos)
    if success_i:
        pos_i, _ = arm.forward_kinematics(iterative_solution)
        error_i = np.linalg.norm(target_pos[:2] - pos_i[:2])
        print(f"Iterative IK solution: {iterative_solution}")
        print(f"Iterative IK error: {error_i}")

if __name__ == "__main__":
    compare_solutions()
```

## Step 4: Test Your Implementation

1. Run the basic kinematics test:
   ```bash
   python kinematics.py
   ```

2. Visualize the arm configurations:
   ```bash
   python visualize_kinematics.py
   ```

3. Test the iterative IK solver:
   ```bash
   python ik_iterative.py
   ```

## Step 5: Extend the Implementation

Try extending the basic implementation with additional features:

1. Add more joints to create a 6-DOF arm
2. Implement different IK methods (Jacobian pseudoinverse, damped least squares)
3. Add joint limits to the IK solver
4. Create a simple animation of the arm moving to different positions

## Verification

To verify your implementation:

1. Confirm that FK correctly calculates end-effector position from joint angles
2. Verify that the Jacobian calculation is mathematically correct
3. Check that analytical IK solutions match expected values
4. Ensure iterative IK converges to reasonable solutions
5. Validate that the visualization accurately represents the arm configuration

## Troubleshooting

- If IK solutions are not converging, try reducing the step size in the iterative method
- If FK gives unexpected results, check your DH parameter definitions
- If the arm appears distorted in visualization, verify the transformation calculations
- If joint limits are not respected, add bounds checking to your IK solvers

## Next Steps

In the next lab, you'll apply these kinematics concepts to bipedal locomotion, learning how to use inverse kinematics for foot placement and balance control in humanoid robots.