---
id: module-1-ros2-index
title: "Module 1: ROS 2 Fundamentals"
sidebar_label: "Module 1: ROS 2"
sidebar_position: 1
---

# Module 1: ROS 2 Fundamentals (Weeks 3-5)

Welcome to Module 1! This module provides comprehensive coverage of ROS 2 (Robot Operating System 2), the industry-standard framework for building distributed robotic applications.

## Module Overview

ROS 2 Humble Hawksbill is a complete rewrite of ROS 1, offering real-time performance, improved security, and cross-platform support. You'll learn to build modular, scalable robotic systems using Python and C++.

### Learning Objectives

By the end of this module, you will:
- Understand ROS 2 architecture and communication patterns
- Create and manage ROS 2 nodes, topics, services, and actions
- Design robot descriptions using URDF and Xacro
- Implement launch files for complex system orchestration
- Build agent-to-ROS bridges for AI integration
- Deploy ROS 2 applications on NVIDIA Jetson hardware

## Topics Covered

### Chapter 1: Foundations & Nodes
- ROS 2 architecture and DDS middleware
- Creating publishers and subscribers
- Topic communication patterns
- Message types and custom messages
- Quality of Service (QoS) settings

### Chapter 2: Services & Actions
- Synchronous service communication
- Request-response patterns
- Asynchronous action servers/clients
- Feedback and goal management
- Use cases for each pattern

### Chapter 3: rclpy Patterns
- Python node design patterns
- Lifecycle nodes and managed nodes
- Timers and callbacks
- Parameters and dynamic reconfiguration
- Best practices for Python ROS 2

### Chapter 4: URDF & Robot Description
- Unified Robot Description Format (URDF)
- Links, joints, and kinematic chains
- Visual and collision geometry
- Xacro for modular robot descriptions
- Robot State Publisher

### Chapter 5: Launch Files & Parameters
- Python launch files
- XML/YAML launch files
- Parameter configuration
- Node composition and containers
- Multi-robot launches

### Chapter 6: Agent-to-ROS Bridge
- Integrating AI agents with ROS 2
- Publishing sensor data for AI models
- Receiving actions from agents
- Gym/Gymnasium integration
- PyTorch model deployment

## Module Structure

```
Week 3: Nodes, Topics, and Basic Communication
Week 4: Services, Actions, and Advanced Patterns
Week 5: Robot Description, Launch Systems, and AI Integration
```

## Hands-On Labs

Each chapter includes practical labs:
- **Lab 1.1**: Simple talker-listener nodes
- **Lab 1.2**: Custom message definitions
- **Lab 2.1**: Service-based calculator
- **Lab 2.2**: Action server for robot navigation
- **Lab 3.1**: Parameter-driven node behavior
- **Lab 4.1**: Create URDF for simple robot
- **Lab 5.1**: Multi-node launch file
- **Lab 6.1**: Gym environment with ROS 2 bridge

## Capstone Project

**Objective**: Build a complete ROS 2 system integrating all concepts.

**Requirements**:
- Multi-node architecture (sensors, planning, control)
- Service and action interfaces
- URDF robot model visualization in RViz
- Launch system for entire stack
- AI agent integration (optional reinforcement learning)

**Deliverables**:
- Source code with documentation
- Launch files for reproduction
- Video demonstration
- Written report (max 5 pages)

## Prerequisites

- Ubuntu 22.04 LTS with ROS 2 Humble installed
- Python 3.10+ and basic Python knowledge
- Familiarity with Linux terminal
- (Optional) C++ for advanced performance

See [Setup Guides](../../setup-guides/setup-guides-index) for installation instructions.

## Resources

### Official Documentation
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [ROS 2 Tutorials](https://docs.ros.org/en/humble/Tutorials.html)
- [ROS 2 Design Docs](https://design.ros2.org/)

### Community Resources
- [ROS Discourse Forum](https://discourse.ros.org/)
- [ROS Answers](https://answers.ros.org/)
- Course Discord/Slack channels

### Code Examples
- Module code repository: `/code/module-1-ros2/`
- Official ROS 2 demos: `ros-humble-demo-nodes-*`

## Assessment

- **Weekly Labs**: 40% (due each week)
- **Capstone Project**: 50%
- **Participation**: 10% (code reviews, forum help)

## Timeline

| Week | Topics | Deliverables |
|------|--------|--------------|
| 3 | Chapters 1-2 | Labs 1.1, 1.2, 2.1 |
| 4 | Chapters 3-4 | Labs 2.2, 3.1, 4.1 |
| 5 | Chapters 5-6 | Labs 5.1, 6.1, Capstone |

## Next Steps

Ready to dive in? Start with:
1. [Chapter 1: Foundations & Nodes](./chapter-1/01-overview.md)
2. Review [ROS 2 concepts](https://docs.ros.org/en/humble/Concepts.html)
3. Set up your development environment

Let's build amazing robotic systems! 🚀🤖
