#!/usr/bin/env python3
"""
Jacobian Computation Example
This demonstrates the basic concepts covered in Chapter 2: Humanoid Kinematics
"""

import numpy as np
import math
from typing import List, Tuple

class JacobianCalculator:
    """Calculate Jacobian matrices for robotic arms"""

    def __init__(self):
        # Link lengths for a simple 2-link planar arm
        self.l1 = 1.0  # Length of first link
        self.l2 = 0.8  # Length of second link

    def forward_kinematics(self, theta1: float, theta2: float) -> Tuple[float, float]:
        """
        Calculate end-effector position from joint angles
        Returns: (x, y) position of end-effector
        """
        x = self.l1 * math.cos(theta1) + self.l2 * math.cos(theta1 + theta2)
        y = self.l1 * math.sin(theta1) + self.l2 * math.sin(theta1 + theta2)
        return x, y

    def jacobian_analytical(self, theta1: float, theta2: float) -> np.ndarray:
        """
        Calculate Jacobian matrix analytically
        For a 2-link planar arm, the Jacobian is 2x2:
        [dx/dtheta1  dx/dtheta2]
        [dy/dtheta1  dy/dtheta2]
        """
        # Derivatives of the forward kinematics equations
        dx_dtheta1 = -self.l1 * math.sin(theta1) - self.l2 * math.sin(theta1 + theta2)
        dx_dtheta2 = -self.l2 * math.sin(theta1 + theta2)
        dy_dtheta1 = self.l1 * math.cos(theta1) + self.l2 * math.cos(theta1 + theta2)
        dy_dtheta2 = self.l2 * math.cos(theta1 + theta2)

        jacobian = np.array([
            [dx_dtheta1, dx_dtheta2],
            [dy_dtheta1, dy_dtheta2]
        ])

        return jacobian

    def jacobian_numerical(self, theta1: float, theta2: float, epsilon: float = 1e-6) -> np.ndarray:
        """
        Calculate Jacobian matrix using numerical differentiation
        This method approximates the derivatives using small perturbations
        """
        # Calculate base position
        x_base, y_base = self.forward_kinematics(theta1, theta2)

        # Calculate position with small perturbation in theta1
        x_pert1, y_pert1 = self.forward_kinematics(theta1 + epsilon, theta2)
        dx_dtheta1 = (x_pert1 - x_base) / epsilon
        dy_dtheta1 = (y_pert1 - y_base) / epsilon

        # Calculate position with small perturbation in theta2
        x_pert2, y_pert2 = self.forward_kinematics(theta1, theta2 + epsilon)
        dx_dtheta2 = (x_pert2 - x_base) / epsilon
        dy_dtheta2 = (y_pert2 - y_base) / epsilon

        jacobian = np.array([
            [dx_dtheta1, dx_dtheta2],
            [dy_dtheta1, dy_dtheta2]
        ])

        return jacobian

    def inverse_jacobian(self, theta1: float, theta2: float) -> np.ndarray:
        """
        Calculate the inverse of the Jacobian matrix
        Note: Only possible when the Jacobian is square and non-singular
        """
        jacobian = self.jacobian_analytical(theta1, theta2)

        # Check if the determinant is non-zero (non-singular)
        det = np.linalg.det(jacobian)
        if abs(det) < 1e-6:
            print("Warning: Jacobian is close to singular (determinant ≈ 0)")
            print("This indicates a singularity in the robot's configuration")

        try:
            jacobian_inv = np.linalg.inv(jacobian)
            return jacobian_inv
        except np.linalg.LinAlgError:
            print("Error: Jacobian is singular, inverse does not exist")
            return jacobian  # Return original for reference

def main():
    print("Jacobian Computation Example")
    print("=" * 30)

    jacobian_calc = JacobianCalculator()

    # Example 1: Calculate Jacobian at specific joint angles
    print("\n1. Jacobian Calculation Example:")
    theta1, theta2 = math.pi/4, math.pi/6  # 45° and 30°

    x, y = jacobian_calc.forward_kinematics(theta1, theta2)
    print(f"   Joint angles: θ1={theta1:.3f} rad ({math.degrees(theta1):.1f}°), θ2={theta2:.3f} rad ({math.degrees(theta2):.1f}°)")
    print(f"   End-effector position: ({x:.3f}, {y:.3f})")

    jacobian_analytical = jacobian_calc.jacobian_analytical(theta1, theta2)
    print(f"   Analytical Jacobian:\n{jacobian_analytical}")

    jacobian_numerical = jacobian_calc.jacobian_numerical(theta1, theta2)
    print(f"   Numerical Jacobian:\n{jacobian_numerical}")

    # Check if they are approximately equal
    diff = np.abs(jacobian_analytical - jacobian_numerical)
    max_diff = np.max(diff)
    print(f"   Max difference between analytical and numerical: {max_diff:.6f}")

    # Example 2: Use Jacobian for velocity mapping
    print("\n2. Velocity Mapping Example:")
    print("   If we want the end-effector to move with velocity (dx_dt, dy_dt),")
    print("   we can find the required joint velocities (dtheta1_dt, dtheta2_dt)")

    # Desired end-effector velocity
    dx_dt, dy_dt = 0.1, 0.05  # m/s
    end_effector_velocity = np.array([dx_dt, dy_dt])

    print(f"   Desired end-effector velocity: ({dx_dt}, {dy_dt}) m/s")

    # Calculate required joint velocities
    jacobian_inv = jacobian_calc.inverse_jacobian(theta1, theta2)
    joint_velocities = jacobian_inv @ end_effector_velocity

    print(f"   Required joint velocities: (dθ1/dt, dθ2/dt) = ({joint_velocities[0]:.3f}, {joint_velocities[1]:.3f}) rad/s")

    # Example 3: Check for singularities
    print("\n3. Singularity Check Example:")
    # At certain configurations, the Jacobian becomes singular
    # For example, when the arm is fully extended (θ2 = 0)
    theta1_singular, theta2_singular = 0.0, 0.0
    jacobian_singular = jacobian_calc.jacobian_analytical(theta1_singular, theta2_singular)
    det_singular = np.linalg.det(jacobian_singular)

    print(f"   At θ1=0, θ2=0: Jacobian determinant = {det_singular:.6f}")
    print(f"   This configuration is {'singular' if abs(det_singular) < 1e-6 else 'not singular'}")

if __name__ == "__main__":
    main()