#!/usr/bin/env python3
"""
MPC (Model Predictive Control) Skeleton Example
This demonstrates the basic concepts covered in Chapter 3: Bipedal Locomotion
"""

import numpy as np
import math
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

class MPCLocomotionController:
    """
    Model Predictive Control skeleton for bipedal locomotion
    This is a simplified implementation for educational purposes
    """

    def __init__(self, dt: float = 0.1, prediction_horizon: int = 10):
        """
        Initialize MPC controller
        dt: time step
        prediction_horizon: number of steps to predict into the future
        """
        self.dt = dt
        self.prediction_horizon = prediction_horizon
        self.gravity = 9.81  # m/s^2
        self.com_height = 0.8  # Center of mass height (m)

        # Robot state [x, y, vx, vy] - position and velocity
        self.state = np.array([0.0, 0.0, 0.0, 0.0])

    def predict_dynamics(self, state: np.ndarray, control_input: np.ndarray, dt: float) -> np.ndarray:
        """
        Predict next state based on current state and control input
        For walking, we use simplified inverted pendulum dynamics
        """
        x, y, vx, vy = state
        fx, fy = control_input  # Control forces

        # Simplified dynamics: point mass with gravity
        # In reality, MPC would use more complex humanoid dynamics
        new_vx = vx + (fx / 1.0) * dt  # Assuming mass = 1 for simplicity
        new_vy = vy + (fy / 1.0) * dt - self.gravity * dt  # Include gravity

        new_x = x + new_vx * dt
        new_y = y + new_vy * dt

        return np.array([new_x, new_y, new_vx, new_vy])

    def calculate_zmp(self, com_pos: np.ndarray, com_acc: np.ndarray) -> np.ndarray:
        """
        Calculate Zero-Moment Point (ZMP) from center of mass position and acceleration
        ZMP_x = CoM_x - (CoM_height / gravity) * CoM_acc_x
        ZMP_y = CoM_y - (CoM_height / gravity) * CoM_acc_y
        """
        zmp_x = com_pos[0] - (self.com_height / self.gravity) * com_acc[0]
        zmp_y = com_pos[1] - (self.com_height / self.gravity) * com_acc[1]
        return np.array([zmp_x, zmp_y])

    def plan_step_location(self, current_state: np.ndarray, target_zmp: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Plan the next step location based on target ZMP
        Returns: (step_position, step_timing)
        """
        # In a real MPC, this would involve solving an optimization problem
        # For this skeleton, we'll use a simple approach

        # Calculate desired foot placement to achieve target ZMP
        # This is a simplified approach - real MPC would optimize over the prediction horizon
        com_pos = current_state[:2]  # x, y position
        com_vel = current_state[2:]  # vx, vy velocity

        # Simple strategy: place foot to move ZMP toward target
        step_offset = target_zmp - com_pos
        step_position = com_pos + step_offset * 0.5  # Take a step halfway toward target

        # Return step position and timing (next step time)
        step_timing = self.dt * 2  # Take next step in 2 time steps

        return step_position, step_timing

    def cost_function(self, predicted_states: List[np.ndarray], target_zmp: np.ndarray) -> float:
        """
        Calculate cost of a trajectory based on how well it tracks the target ZMP
        """
        total_cost = 0.0

        for state in predicted_states:
            # Calculate ZMP for this state (simplified)
            com_pos = state[:2]
            # For simplicity, assume constant CoM acceleration based on velocity
            # In reality, this would require more complex dynamics
            zmp = self.calculate_zmp(com_pos, np.array([0.0, 0.0]))

            # Cost is distance from target ZMP
            dist_to_target = np.linalg.norm(zmp - target_zmp)
            total_cost += dist_to_target**2

        return total_cost

    def optimize_control(self, current_state: np.ndarray, target_zmp: np.ndarray) -> np.ndarray:
        """
        Find optimal control input by evaluating different options
        This is a simplified version of the MPC optimization
        """
        # In a real MPC, this would involve solving a constrained optimization problem
        # For this skeleton, we'll try a few different control inputs and pick the best one

        best_control = np.array([0.0, 0.0])
        best_cost = float('inf')

        # Try different control inputs
        control_candidates = [
            np.array([0.0, 0.0]),      # No control
            np.array([0.1, 0.0]),      # Small x force
            np.array([-0.1, 0.0]),     # Small -x force
            np.array([0.0, 0.1]),      # Small y force
            np.array([0.0, -0.1]),     # Small -y force
            np.array([0.1, 0.1]),      # Diagonal
            np.array([-0.1, -0.1]),    # Diagonal
        ]

        for control in control_candidates:
            # Predict trajectory with this control
            predicted_states = []
            state = current_state.copy()

            for i in range(self.prediction_horizon):
                state = self.predict_dynamics(state, control, self.dt)
                predicted_states.append(state)

            # Calculate cost of this trajectory
            cost = self.cost_function(predicted_states, target_zmp)

            if cost < best_cost:
                best_cost = cost
                best_control = control

        return best_control

    def step_simulation(self, target_zmp: np.ndarray) -> Dict:
        """
        Perform one step of MPC control
        """
        # Optimize control input
        optimal_control = self.optimize_control(self.state, target_zmp)

        # Apply control and update state
        self.state = self.predict_dynamics(self.state, optimal_control, self.dt)

        # Calculate current ZMP
        current_com = self.state[:2]
        current_com_acc = np.array([0.0, 0.0])  # Simplified
        current_zmp = self.calculate_zmp(current_com, current_com_acc)

        # Plan next step location
        next_step_pos, next_step_time = self.plan_step_location(self.state, target_zmp)

        return {
            "current_state": self.state.copy(),
            "current_zmp": current_zmp,
            "target_zmp": target_zmp,
            "optimal_control": optimal_control,
            "next_step_position": next_step_pos,
            "next_step_timing": next_step_time,
            "cost": self.cost_function([self.state], target_zmp)
        }

def simulate_walking_pattern():
    """Simulate a simple walking pattern using the MPC controller"""
    print("MPC Locomotion Controller Simulation")
    print("=" * 40)

    controller = MPCLocomotionController(dt=0.1, prediction_horizon=10)

    # Define a simple walking pattern - move in a straight line
    target_positions = [
        np.array([0.5, 0.0]),   # Move forward
        np.array([1.0, 0.0]),   # Continue forward
        np.array([1.5, 0.1]),   # Slight right
        np.array([2.0, 0.0]),   # Back to center
        np.array([2.5, 0.0]),   # Continue forward
    ]

    # Store trajectory for visualization
    positions = []
    zmp_positions = []

    print("Starting simulation...")
    for i, target_pos in enumerate(target_positions):
        print(f"\nStep {i+1}: Target ZMP = {target_pos}")

        result = controller.step_simulation(target_pos)

        pos = result["current_state"][:2]  # Extract x, y position
        zmp = result["current_zmp"]

        positions.append(pos.copy())
        zmp_positions.append(zmp.copy())

        print(f"  Current position: {pos}")
        print(f"  Current ZMP: {zmp}")
        print(f"  Optimal control: {result['optimal_control']}")
        print(f"  Next step at: {result['next_step_position']}")

    # Convert to numpy arrays for plotting
    positions = np.array(positions)
    zmp_positions = np.array(zmp_positions)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(positions[:, 0], positions[:, 1], 'b-o', label='CoM Trajectory', linewidth=2, markersize=8)
    plt.plot(zmp_positions[:, 0], zmp_positions[:, 1], 'r-s', label='ZMP Trajectory', linewidth=2, markersize=6)
    plt.title('MPC-Based Walking Simulation: CoM vs ZMP Trajectories')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')

    # Add step positions as text
    for i, (pos, zmp) in enumerate(zip(positions, zmp_positions)):
        plt.annotate(f'{i+1}', (pos[0], pos[1]), xytext=(5, 5), textcoords='offset points')

    plt.tight_layout()
    plt.show()

def main():
    print("MPC (Model Predictive Control) Skeleton Example")
    print("=" * 50)

    # Example 1: Single step MPC control
    print("\n1. Single MPC Control Step Example:")
    controller = MPCLocomotionController()

    target_zmp = np.array([0.5, 0.0])  # Target ZMP position
    result = controller.step_simulation(target_zmp)

    print(f"   Target ZMP: {target_zmp}")
    print(f"   Current state: {result['current_state']}")
    print(f"   Current ZMP: {result['current_zmp']}")
    print(f"   Optimal control: {result['optimal_control']}")
    print(f"   Next step position: {result['next_step_position']}")
    print(f"   Cost: {result['cost']:.4f}")

    # Example 2: Walking simulation
    print("\n2. Walking Simulation")
    simulate_walking_pattern()

    print("\nMPC Controller Summary:")
    print("  - Predicts future states over a horizon")
    print("  - Optimizes control inputs to minimize cost function")
    print("  - Maintains balance by controlling ZMP position")
    print("  - Plans footstep locations for stable walking")

if __name__ == "__main__":
    main()