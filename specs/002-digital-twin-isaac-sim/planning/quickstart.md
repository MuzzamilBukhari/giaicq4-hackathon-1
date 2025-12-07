# Quickstart Guide: Module 2 & 3 Implementation

## Overview
This guide provides a quick reference for the implemented Module 2 (Digital Twin & Simulation) and Module 3 (NVIDIA Isaac Sim) content for the Physical AI & Humanoid Robotics curriculum.

## Directory Structure
```
docs/
├── modules/
│   ├── module-2-digital-twin/
│   │   ├── index.md
│   │   ├── chapter-1-gazebo-fundamentals/
│   │   │   ├── index.md
│   │   │   └── lab.md
│   │   ├── chapter-2-unity-for-robotics/
│   │   │   ├── index.md
│   │   │   └── lab.md
│   │   └── chapter-3-sim-to-real-transfer/
│   │       ├── index.md
│   │       └── lab.md
│   └── module-3-isaac-sim/
│       ├── index.md
│       ├── chapter-1-isaac-sim-setup/
│       │   ├── index.md
│       │   └── lab.md
│       ├── chapter-2-perception-pipeline/
│       │   ├── index.md
│       │   └── lab.md
│       └── chapter-3-ai-training-integration/
│           ├── index.md
│           └── lab.md
static/
└── code/
    ├── module-2/
    │   ├── gazebo_examples/
    │   │   ├── simple_robot.urdf
    │   │   └── simple_world.sdf
    │   ├── unity_examples/
    │   │   └── robot_joint_controller.cs
    │   └── domain_randomization/
    │       └── domain_randomizer.cs
    └── module-3/
        ├── isaac_examples/
        │   └── simple_scene.py
        ├── perception_pipeline/
        │   └── camera_example.py
        └── ai_training/
            └── simple_classifier.py
```

## Key Technologies
- **Gazebo Classic**: For ROS 2 Humble compatibility
- **Unity Robotics Hub**: For visualization and URDF import
- **NVIDIA Isaac Sim 4.0.0**: For perception and AI training
- **ROS 2 Humble**: Core robotics framework

## Getting Started

### For Students
1. Navigate to the modules in the documentation sidebar
2. Start with Module 2 Chapter 1 to learn Gazebo fundamentals
3. Progress through each chapter, completing the labs
4. Use the example code in `static/code/` to follow along

### For Educators
1. Review the learning objectives for each chapter
2. Ensure students have prerequisites (ROS 2 fundamentals)
3. Guide students through the hands-on labs
4. Use the example assets to demonstrate concepts

## Prerequisites
- Ubuntu 22.04
- ROS 2 Humble installation
- Basic understanding of robotics concepts
- For Isaac Sim: GPU with CUDA support

## Example Usage

### Running Gazebo Examples
```bash
cd ~/workspace/gazebo_examples
# Use the URDF files with ROS 2 launch files
```

### Unity Integration
1. Install Unity Robotics Hub
2. Use URDF Importer to import robot models
3. Follow the documentation for ROS-Unity bridge setup

### Isaac Sim Setup
1. Install Isaac Sim 4.0.0
2. Run example Python scripts from `static/code/module-3/`
3. Verify camera topics are publishing correctly

## Lab Verification
Each lab includes:
- Clear learning objectives
- Prerequisites
- Step-by-step instructions
- Expected outputs
- Verification checks
- Troubleshooting tips

## Asset Policy
- All example files are <100KB
- Large assets linked externally
- Code examples are minimal and demonstrative
- Assets are organized by module for easy access