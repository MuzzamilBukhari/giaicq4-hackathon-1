# Tasks for Module 1 — ROS 2 Fundamentals (Docusaurus-ready)

**Feature**: Module 1 — ROS 2 Fundamentals (Docusaurus-ready)
**Goal**: Produce a complete set of atomic tasks that create Module 1 as Docusaurus pages + runnable example assets. Each task must produce files in the repository and include acceptance criteria that can be validated locally/CI.

## Phase 1: Setup

- [x] T001 Decide ROS 2 Distro: Lock target distro (Humble) and record rationale + test matrix (Ubuntu 22.04, Jetson notes). specs/001-ros2-fundamentals/decision-ros-distro.md
- [x] T002 Create docs folder for Module 1: Create directory and add _category_.json and index.md with frontmatter. docs/module-1-ros2/
- [x] T003 Create chapter template file: Add frontmatter template and required sections (objectives, summary, examples, exercises, troubleshooting). docs/module-1-ros2/_chapter-template.md

## Phase 2: User Story 1 - Learning ROS 2 Core Concepts

**Goal**: A student wants to understand fundamental ROS 2 concepts (nodes, topics, services, actions) through practical examples provided in the module.
**Independent Test**: The student can run the provided rclpy publisher/subscriber example and observe data exchange between nodes, verifying their understanding of topic communication.

- [x] T004 [US1] Author Lesson 1: Nodes & Topics page: Write learning objectives, conceptual explanation, small runnable example snippet (publisher/subscriber), run instructions, expected output, troubleshooting. docs/module-1-ros2/lesson-1-nodes-topics.md
- [x] T005 [US1] Add runnable publisher/subscriber example: Create minimal ROS 2 Python package with publisher and subscriber examples and step-by-step run commands. static/code/module-1-ros2/rclpy_examples/
- [x] T006 [US1] Author Lesson 2: Services & Actions page: Explanations, code snippets (service server/client, action server/client), step-by-step lab plan. docs/module-1-ros2/lesson-2-services-actions.md
- [x] T007 [US1] Add runnable service & action example: Provide minimal service server/client and action server/client with README run steps and expected output. static/code/module-1-ros2/service_examples/

## Phase 3: User Story 2 - Building Robot Descriptions and Launching Systems

**Goal**: A student wants to learn how to describe a robot's physical structure using URDF and how to compose and manage multiple ROS 2 nodes using launch files to bring up a complete robotic system.
**Independent Test**: The student can successfully load a URDF model into a simulation environment (e.g., Gazebo) and can use a launch file to start multiple interacting ROS 2 nodes, verifying system integration.

- [x] T008 [US2] Author Lesson 4: URDF & Robot Description: Explain URDF basics, joints/links, sensors, include a minimal humanoid proxy URDF and loading instructions in Gazebo. docs/module-1-ros2/lesson-4-urdf-robot-description.md
- [x] T009 [US2] Add URDF + Gazebo integration demo: Provide launch file and instructions to spawn robot in Gazebo and verify topics (e.g., /tf, /joint_states). static/code/module-1-ros2/urdf_examples/
- [x] T010 [US2] Author Lesson 5: Launch Files & Parameter Management: Explain launch composition, passing parameters, remapping, and an example that composes pub/sub and URDF spawn. docs/module-1-ros2/lesson-5-launch-files-and-params.md
- [x] T011 [US2] Add launch examples and parameter files: Create sample launch files, parameter YAML, and instructions to run full example. static/code/module-1-ros2/launch_examples/

## Phase 4: User Story 3 - Bridging Python Agents to ROS Controllers

**Goal**: A student wants to understand the mechanism for connecting Python-based AI agents (e.g., for high-level decision making) with lower-level ROS 2 robotic controllers, enabling embodied AI applications.
**Independent Test**: The student can run the agent-ROS bridge example, where a Python agent sends commands (e.g., movement goals) to a ROS 2 action server, and the simulated robot responds accordingly.

- [x] T012 [US3] Author Lesson 6: Agent → ROS bridge: Show architecture of a Python agent sending commands to ROS (e.g., via service/action). Include a tiny bridge example connecting a text command to an action call. docs/module-1-ros2/lesson-6-agent-to-ros-bridge.md
- [x] T013 [US3] Add Agent-to-ROS bridge example: Provide a script that accepts a command and triggers a ROS action in simulation. static/code/module-1-ros2/agent_bridge_examples/

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T014 Author Lesson 3: rclpy patterns & node lifecycle (practical): Show common rclpy idioms, QoS example, simple lifecycle or proper node shutdown handling, small example code. docs/module-1-ros2/lesson-3-rclpy-patterns.md
- [x] T015 Add rclpy examples: Add small examples demonstrating QoS and safe shutdown. static/code/module-1-ros2/rclpy_patterns/
- [x] T016 Create Lab pages for each lesson: Each lab includes prerequisites, step-by-step tasks, expected outputs, verification checklist, and troubleshooting tips. docs/module-1-ros2/labs/
- [x] T017 Capstone page & scaffold: Define capstone mini-project "Voice command → ROS action → simulated robot behavior", provide scaffold steps, expected deliverables, and reference files. docs/module-1-ros2/capstone.md
- [x] T018 Create module-level validation checklists: Include `colcon build` checklist, ros2 run commands to validate each demo, Gazebo checks, and Jetson notes. specs/001-ros2-fundamentals/checklists/build-validate.md & specs/001-ros2-fundamentals/checklists/run-verify.md
- [x] T019 Add Docusaurus frontmatter & sidebar registration: Ensure sidebar_position and ids are deterministic and module appears under "Modules" in sidebar. docs/module-1-ros2/* and sidebars.js
- [x] T020 Local smoke test: Run `npm run build` (Docusaurus), `colcon build` for examples, `ros2 launch` sample - record successes/failures. specs/001-ros2-fundamentals/checklists/build-validate.md
- [x] T021 Jetson notes & optional emulation: Add Jetson Orin/Orin Nano-specific instructions, cross-compilation or flash notes, and any emulation tips if no Jetson hardware available. docs/module-1-ros2/jetson-notes.md
- [x] T022 Commit, branch, and PR creation: Commit all created files, push branch, and open PR referencing spec & plan. specs/001-ros2-fundamentals/contracts/pr-links.md

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 must be completed before Phase 3.
- Phase 3 must be completed before Phase 4.
- Phase 4 must be completed before Phase 5.

## Parallel Execution Examples

### User Story 1 (T004 - T007)

- T004 [P] Author Lesson 1: Nodes & Topics page: docs/module-1-ros2/lesson-1-nodes-topics.md
- T005 [P] Add runnable publisher/subscriber example: static/code/module-1-ros2/rclpy_examples/
- T006 [P] Author Lesson 2: Services & Actions page: docs/module-1-ros2/lesson-2-services-actions.md
- T007 [P] Add runnable service & action example: static/code/module-1-ros2/service_examples/

### User Story 2 (T008 - T011)

- T008 [P] Author Lesson 4: URDF & Robot Description: docs/module-1-ros2/lesson-4-urdf-robot-description.md
- T009 [P] Add URDF + Gazebo integration demo: static/code/module-1-ros2/urdf_examples/
- T010 [P] Author Lesson 5: Launch Files & Parameter Management: docs/module-1-ros2/lesson-5-launch-files-and-params.md
- T011 [P] Add launch examples and parameter files: static/code/module-1-ros2/launch_examples/

### User Story 3 (T012 - T013)

- T012 [P] Author Lesson 6: Agent → ROS bridge: docs/module-1-ros2/lesson-6-agent-to-ros-bridge.md
- T013 [P] Add Agent-to-ROS bridge example: static/code/module-1-ros2/agent_bridge_examples/

## Implementation Strategy

The implementation will proceed in a phased approach, prioritizing foundational setup and core user stories first. Each phase aims to deliver independently testable components. Incremental delivery will allow for continuous validation and feedback.

## Format Validation

All tasks adhere to the `- [ ] [TaskID] [P?] [Story?] Description with file path` format.
