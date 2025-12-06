---
id: module-1-ros2-chapter-1-overview
title: "Chapter 1: Foundations & Nodes - Overview"
sidebar_label: "Overview"
---

# Chapter 1: Foundations & Nodes

## Introduction

This chapter introduces the fundamental concepts of ROS 2, focusing on the architecture, communication patterns, and creating your first nodes using publishers and subscribers.

## What is ROS 2?

ROS 2 (Robot Operating System 2) is an open-source middleware framework for building distributed robotic applications. Unlike ROS 1, it's built on DDS (Data Distribution Service) for real-time, reliable communication.

### Key Features
- **Real-time capable**: Deterministic communication with QoS policies
- **Secure**: Authentication, encryption, access control
- **Cross-platform**: Linux, Windows, macOS
- **Language agnostic**: Python, C++, and more
- **Modular**: Microservice-style node architecture

## ROS 2 Architecture

### DDS Middleware Layer
ROS 2 uses DDS for peer-to-peer communication without a central master (unlike ROS 1):
- **Discovery**: Nodes automatically find each other
- **Publish-Subscribe**: Asynchronous data distribution
- **Quality of Service**: Reliability, durability, latency settings

### Node-Based Design
Everything in ROS 2 is a **node**:
- Nodes are independent processes
- Communicate via topics, services, actions
- Can be composed into a single process for efficiency

## Core Concepts

### Topics
- Unidirectional, many-to-many communication
- Publishers send messages, subscribers receive
- Named channels (e.g., `/camera/image`, `/cmd_vel`)

### Messages
- Typed data structures (e.g., `std_msgs/String`, `sensor_msgs/Image`)
- Defined in `.msg` files
- Automatically generate code for serialization

### Quality of Service (QoS)
Configure reliability and performance:
- **Reliability**: `RELIABLE` vs `BEST_EFFORT`
- **Durability**: `TRANSIENT_LOCAL` vs `VOLATILE`
- **History**: Keep last N messages

## Chapter Roadmap

1. **Overview** (this page): Architecture and concepts
2. **Topics & Communication**: Publishers, subscribers, message types
3. **Labs**: Hands-on exercises building nodes

## Learning Outcomes

After completing this chapter:
- ✅ Understand ROS 2 architecture and DDS
- ✅ Create publisher and subscriber nodes in Python
- ✅ Work with standard and custom message types
- ✅ Configure QoS policies for different scenarios
- ✅ Debug and introspect ROS 2 systems with CLI tools

## Prerequisites

- ROS 2 Humble installed
- Basic Python knowledge
- Terminal proficiency

## Next Steps

Continue to [Topics & Communication](./02-topics.md) to start building nodes.
