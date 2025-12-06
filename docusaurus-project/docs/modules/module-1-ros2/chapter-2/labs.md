---
id: module-1-ros2-chapter-2-labs
title: "Chapter 2 Labs"
sidebar_label: "Labs"
---

# Chapter 2: Services & Actions Labs

Complete these labs to master ROS 2 services and actions.

## Lab 2.1: Calculator Service

**Objective**: Build a multi-operation calculator service.

### Requirements

Create a service that supports:
- Addition
- Subtraction
- Multiplication
- Division (with error handling)

### Custom Service Definition

File: `my_interfaces/srv/Calculate.srv`
```
# Request
float64 a
float64 b
string operation  # "add", "sub", "mul", "div"
---
# Response
float64 result
bool success
string message
```

### Implementation Template

```python
from my_interfaces.srv import Calculate

class CalculatorService(Node):
    def __init__(self):
        super().__init__('calculator_service')
        self.srv = self.create_service(
            Calculate,
            'calculate',
            self.calculate_callback
        )
    
    def calculate_callback(self, request, response):
        # TODO: Implement calculator logic
        # Handle all operations
        # Check for division by zero
        # Set success and message appropriately
        pass
```

### Testing

```bash
# Test addition
ros2 service call /calculate my_interfaces/srv/Calculate "{a: 10.0, b: 5.0, operation: 'add'}"

# Test division by zero
ros2 service call /calculate my_interfaces/srv/Calculate "{a: 10.0, b: 0.0, operation: 'div'}"
```

### Success Criteria
- [ ] All four operations work correctly
- [ ] Division by zero returns `success: false`
- [ ] Meaningful error messages returned
- [ ] Invalid operations handled gracefully

---

## Lab 2.2: LED Controller Action

**Objective**: Create an action server for LED blinking pattern.

### Action Definition

File: `my_interfaces/action/BlinkLED.action`
```
# Goal
int32 blink_count
float32 frequency  # Hz
---
# Result
bool completed
int32 actual_blinks
---
# Feedback
int32 blinks_remaining
int32 current_blink
```

### Requirements

1. **Action Server**: Controls LED (simulated with print statements)
2. **Feedback**: Reports progress every blink
3. **Cancellation**: Stops blinking when canceled
4. **Validation**: Reject invalid frequencies (< 0.1 Hz or > 10 Hz)

### Implementation Hints

```python
from my_interfaces.action import BlinkLED
import time

class LEDActionServer(Node):
    def __init__(self):
        super().__init__('led_action_server')
        self._action_server = ActionServer(
            self, BlinkLED, 'blink_led', self.execute_callback
        )
    
    def execute_callback(self, goal_handle):
        # Validate frequency
        if goal_handle.request.frequency < 0.1 or goal_handle.request.frequency > 10.0:
            goal_handle.abort()
            return BlinkLED.Result()
        
        # Calculate period
        period = 1.0 / goal_handle.request.frequency
        
        # Blink loop
        for i in range(goal_handle.request.blink_count):
            # Check for cancel
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = BlinkLED.Result()
                result.actual_blinks = i
                return result
            
            # Simulate LED on
            self.get_logger().info('LED ON')
            time.sleep(period / 2)
            
            # Simulate LED off
            self.get_logger().info('LED OFF')
            time.sleep(period / 2)
            
            # Send feedback
            feedback = BlinkLED.Feedback()
            feedback.current_blink = i + 1
            feedback.blinks_remaining = goal_handle.request.blink_count - (i + 1)
            goal_handle.publish_feedback(feedback)
        
        # Success
        goal_handle.succeed()
        result = BlinkLED.Result()
        result.completed = True
        result.actual_blinks = goal_handle.request.blink_count
        return result
```

### Testing

```bash
# Send goal with feedback
ros2 action send_goal /blink_led my_interfaces/action/BlinkLED "{blink_count: 5, frequency: 2.0}" --feedback

# Test cancellation (Ctrl+C during execution)
```

### Success Criteria
- [ ] Blinks correct number of times
- [ ] Frequency (timing) accurate
- [ ] Feedback published during execution
- [ ] Cancellation stops blinking immediately
- [ ] Invalid frequencies rejected

---

## Lab 2.3: Patrol Action with Waypoints

**Objective**: Build a robot patrol action that visits multiple waypoints.

### Action Definition

```
# Goal
geometry_msgs/Point[] waypoints
---
# Result
bool success
int32 waypoints_reached
float64 total_distance
---
# Feedback
int32 current_waypoint_index
geometry_msgs/Point current_position
float64 distance_to_next_waypoint
```

### Requirements

- Simulate robot movement (linear interpolation)
- Publish feedback 10 times per second
- Support cancellation
- Calculate and return total distance traveled

### Bonus Features
- [ ] Visualize path in RViz (publish markers)
- [ ] Add obstacle detection (random failure chance)
- [ ] Recovery behavior on failure

---

## Lab 2.4: Integrated Service-Action System

**Objective**: Build a complete system using topics, services, and actions.

### System Components

1. **State Publisher** (Topic): Publishes robot state at 10 Hz
2. **Query Service**: Returns current state on request
3. **Command Action**: Executes movement commands with feedback

### Architecture

```
┌─────────────────┐
│ State Publisher │─────► /robot/state (topic)
└─────────────────┘
         ▲
         │ (reads state)
         │
┌─────────────────┐
│ Query Service   │◄────► /get_state (service)
└─────────────────┘
         ▲
         │ (checks state)
         │
┌─────────────────┐
│ Command Action  │◄────► /execute_command (action)
└─────────────────┘
```

### Custom Messages

**State.msg:**
```
float64 x
float64 y
float64 theta
float64 battery_voltage
string status  # "idle", "moving", "charging"
```

**GetState.srv:**
```
---
State current_state
```

**ExecuteCommand.action:**
```
# Goal
string command  # "move_forward", "turn_left", "turn_right", "stop"
float64 duration
---
# Result
bool success
State final_state
---
# Feedback
float64 time_elapsed
State current_state
```

### Implementation Steps

1. Create interface package with all definitions
2. Implement state publisher node
3. Implement query service (reads from state publisher)
4. Implement command action server (modifies state)
5. Create client to test system

### Success Criteria
- [ ] State published continuously
- [ ] Service returns current state
- [ ] Action executes commands and updates state
- [ ] All components work together
- [ ] Proper error handling

---

## Challenge Lab: Multi-Robot Coordinator

**Objective**: Coordinate multiple robots using services and actions.

### Scenario

3 robots need to visit 3 destinations. Coordinator assigns tasks optimally.

### Requirements

1. **Robot Nodes** (3 instances):
   - Publish status
   - Provide "execute_task" action
   
2. **Coordinator Node**:
   - Service: "assign_tasks"
   - Action: "coordinate_mission"
   - Algorithm: Simple task assignment

3. **Monitor Node**:
   - Subscribes to all robot statuses
   - Displays progress

### Bonus
- [ ] Optimal task assignment (Hungarian algorithm)
- [ ] Handle robot failures and reassign
- [ ] Launch file for entire system

---

## Submission

For each lab:
1. **Code**: All nodes and interfaces
2. **Launch file**: To start system easily
3. **Demo video**: 2-3 minutes showing functionality
4. **README**: Setup and usage instructions

### Grading
- **Functionality** (50%): Meets all requirements
- **Code Quality** (20%): Clean, well-commented
- **Error Handling** (15%): Robust to edge cases
- **Documentation** (15%): Clear README and inline comments

---

## Next Chapter

After completing these labs, continue with Module 1 advanced topics (coming soon).

Excellent work with services and actions! 🎯
