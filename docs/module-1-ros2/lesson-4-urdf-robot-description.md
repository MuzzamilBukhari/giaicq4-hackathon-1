---
sidebar_position: 5
sidebar_label: "URDF & Robot Description"
id: module-1-ros2-urdf-robot-description
---

# Lesson 4: URDF & Robot Description

## Learning Objectives

- Understand the purpose and structure of URDF (Unified Robot Description Format).
- Learn to define robot links and joints using URDF.
- Comprehend how to integrate simple sensors and mimic basic robot structures.
- Be able to load a URDF model into a simulation environment like Gazebo.

## Introduction

To effectively control and simulate robots, we need a standardized way to describe their physical characteristics. In ROS 2, this is primarily achieved using **URDF** (Unified Robot Description Format). URDF is an XML format used to describe all aspects of a robot, including its visual appearance, collision properties, and inertial properties, as well as the kinematic and dynamic properties of its links and joints.

## Conceptual Explanation

**URDF Components:**

-   **Links:** Represent the rigid bodies of the robot (e.g., base, arm segments, wheels). Each link has physical properties (mass, inertia) and visual/collision geometries.
-   **Joints:** Define the connections between links and specify their type (e.g., `revolute`, `continuous`, `fixed`, `prismatic`). Joints define how links move relative to each other.

**Kinematics:** The URDF describes the kinematic chain of the robot, which defines the relationships between its links and joints, allowing ROS 2 to understand the robot's structure and how its parts move.

**Integration with Simulators:** URDF files are often used to load robot models into simulation environments like Gazebo, enabling virtual testing and development before deploying to physical hardware.

### Code Snippets/Examples

Let's consider a very simple URDF for a two-link arm to illustrate the basic structure. (Full, runnable example will be in `static/code/module-1-ros2/urdf_examples/`)

### Example: Simple Two-Link Arm URDF

```xml
<?xml version="1.0"?>
<robot name="two_link_arm">

  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.1"/>
      </geometry>
    </visual>
  </link>

  <link name="link1">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.5"/>
      </geometry>
    </visual>
  </link>

  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.05"/>
    <axis xyz="0 0 1"/>
    <limit effort="1000" velocity="100" lower="-3.14" upper="3.14"/>
  </joint>

</robot>
```

**Loading Instructions in Gazebo (Conceptual):**

To load a URDF into Gazebo, you typically use a ROS 2 launch file that spawns the robot model. This involves:

1.  Ensuring Gazebo is installed and sourced.
2.  Creating a launch file that uses the `spawn_entity.py` script from the `gazebo_ros` package to insert your URDF model.

```xml
<!-- minimal_robot_spawn.launch.xml (conceptual) -->
<launch>
  <node pkg="gazebo_ros" exec="spawn_entity.py" args="-entity two_link_arm -file $(find your_urdf_package)/urdf/two_link_arm.urdf -x 0 -y 0 -z 0"/>
</launch>
```

**Expected Outcome:**

Upon launching Gazebo and the spawn script, you should see your robot model (e.g., the two-link arm) appear in the Gazebo simulation environment.

## Exercises

1.  Extend the two-link arm URDF to include a second link and joint, creating a two-segment arm.
2.  Add a simple visual element to one of the links (e.g., a sphere or a different colored box).
3.  Investigate how to add inertial properties to links and understand their importance for realistic simulation.

## Summary

URDF is a critical tool for describing robot hardware in ROS 2. By defining links and joints, URDF allows ROS 2 to understand a robot's structure, which is essential for motion planning, control, and simulation. Integrating URDF with tools like Gazebo enables comprehensive virtual testing of robotic systems.

## Troubleshooting

-   **URDF parsing errors**: Check XML syntax carefully. Tools like `check_urdf` (from `urdf_parser_py`) can help identify errors.
-   **Robot not appearing in Gazebo**: Ensure all necessary ROS 2 packages (`gazebo_ros`, `xacro` if used) are installed and sourced. Verify the path to your URDF file in the launch command.
-   **Incorrect robot pose/joints**: Double-check `origin` and `axis` definitions in your joints. Use `rviz2` to visualize the URDF before Gazebo to debug kinematic issues.
