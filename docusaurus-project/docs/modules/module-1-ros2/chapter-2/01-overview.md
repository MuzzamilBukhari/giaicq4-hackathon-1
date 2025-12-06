---
id: module-1-ros2-chapter-2-overview
title: "Chapter 2: Services & Actions - Overview"
sidebar_label: "Overview"
---

# Chapter 2: Services & Actions

## Introduction

While topics are great for continuous data streams, ROS 2 provides **services** and **actions** for request-response and goal-oriented communication patterns.

## Services vs Actions vs Topics

| Feature | Topics | Services | Actions |
|---------|--------|----------|---------|
| **Pattern** | Pub/Sub | Request/Response | Goal/Feedback/Result |
| **Direction** | One-way | Two-way (sync) | Two-way (async) |
| **Feedback** | No | No | Yes (ongoing) |
| **Cancellation** | No | No | Yes |
| **Use Case** | Sensor data | Calculations, queries | Long-running tasks |

## When to Use Services

Services are ideal for:
- **Calculations**: "Compute forward kinematics for these joint angles"
- **Queries**: "Get current robot state"
- **Triggers**: "Start calibration routine"
- **Short operations**: Typically < 1 second

### Service Pattern
```
Client → Request → Server
Client ← Response ← Server
```

### Example Use Cases
- Image processing: Send image, receive detected objects
- Path planning: Send goal, receive path
- Configuration: Set/get parameters

## When to Use Actions

Actions are ideal for:
- **Long-running tasks**: Navigation, manipulation sequences
- **Need feedback**: "10% complete, moving to waypoint 2"
- **Cancelable**: User can abort operation
- **Complex workflows**: Multi-step processes

### Action Pattern
```
Client → Goal → Server
Client ← Feedback ← Server (periodic)
Client ← Result ← Server (final)
```

### Example Use Cases
- Robot navigation to goal pose
- Gripper grasp sequence
- Multi-point trajectory execution

## Service Types

ROS 2 services use `.srv` files defining request and response:

```
# AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

**Standard Services:**
- `std_srvs/SetBool`: Enable/disable
- `std_srvs/Trigger`: Simple trigger
- Custom services for domain-specific needs

## Action Types

Actions use `.action` files with goal, result, and feedback:

```
# Fibonacci.action
# Goal
int32 order
---
# Result
int32[] sequence
---
# Feedback
int32[] partial_sequence
```

**Standard Actions:**
- `nav2_msgs/NavigateToPose`: Navigation
- `control_msgs/FollowJointTrajectory`: Arm control

## Chapter Roadmap

1. **Overview** (this page): Services vs Actions concepts
2. **Examples**: Implementation in Python and C++
3. **Labs**: Build service servers, action servers, and clients

## Learning Outcomes

After this chapter:
- ✅ Understand when to use services vs actions vs topics
- ✅ Create service servers and clients
- ✅ Implement action servers with feedback
- ✅ Handle action goals, cancellation, and results
- ✅ Define custom service and action interfaces

## Next Steps

Continue to [Examples](./02-examples.md) to see services and actions in action!
