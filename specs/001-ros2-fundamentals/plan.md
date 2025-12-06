# Implementation Plan: Module 1 — ROS 2 Fundamentals (Physical AI & Humanoid Robotics Textbook)

**Branch**: `001-ros2-fundamentals` | **Date**: 2025-12-05 | **Spec**: [specs/001-ros2-fundamentals/spec.md](specs/001-ros2-fundamentals/spec.md)
**Input**: Feature specification from `/specs/001-ros2-fundamentals/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the creation of "Module 1 — ROS 2 Fundamentals (Physical AI & Humanoid Robotics Textbook)", a Docusaurus-ready educational module. It will cover core ROS 2 concepts, rclpy, URDF, launch files, parameter management, and Python agent bridging. The technical approach involves structuring lessons as Markdown files, developing reproducible code examples in Python, and ensuring compatibility with ROS 2 Humble/Iron, Gazebo simulation, and NVIDIA Jetson devices.

## Technical Context

**Language/Version**: Python 3.10+ (for rclpy examples).
**Primary Dependencies**: ROS 2 (Humble or Iron), rclpy, Gazebo (Ignition recommended), Docusaurus.
**Storage**: N/A (module content is static files).
**Testing**: Manual execution and verification of ROS 2 nodes, services, actions, URDF loading, and launch files in simulation and on Jetson. Automated validation of Docusaurus Markdown rendering.
**Target Platform**: Ubuntu 22.04 (workstation), NVIDIA Jetson Orin/Orin Nano.
**Project Type**: Educational textbook module integrated into a Docusaurus static site.
**Performance Goals**: N/A, focus on clarity, accuracy, and reproducibility of examples.
**Constraints**:
- Supported ROS 2 distros: Humble or Iron (to be clarified).
- All examples runnable in Gazebo and on NVIDIA Jetson Orin/Orin Nano (or documented emulation).
- Small, well-documented, modular code snippets.
- Docusaurus-ready file outputs: `/docs/module-1-ros2/...` Markdown pages + `/static/code/module-1-ros2/...` assets.
- Scope limited to fundamentals and applied labs; no advanced robot control stacks.
**Scale/Scope**: A single Docusaurus module containing:
- Module introduction page.
- 4-6 lesson pages covering core ROS 2 concepts.
- Corresponding labs (2-3 hours each) for major topics.
- At least 6 runnable code examples.
- One capstone mini-project.
- Explicit run/validation checklist.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Technical Accuracy**: All examples and explanations will be based on established ROS 2, robotics, and simulation concepts.
- [x] **Educational Clarity**: Content will be structured for beginner-to-intermediate students, focusing on easy comprehension.
- [x] **Structured Pedagogical Flow**: The plan outlines a logical progression from foundational ROS 2 concepts to applied scenarios.
- [x] **Consistency**: The plan aims for uniform style, terminology, and formatting across lessons and examples.
- [x] **AI-Native Writing Workflow**: The plan aligns with Docusaurus and Spec-Kit standards for content generation and integration.

## Project Structure

### Documentation (this feature)

```text
specs/001-ros2-fundamentals/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docs/
└── module-1-ros2/
    ├── _category_.json    # Docusaurus sidebar category
    ├── index.md           # Module introduction
    ├── lesson-1-nodes-topics.md
    ├── lesson-2-services-actions.md
    ├── lesson-3-urdf-robot-description.md
    ├── lesson-4-launch-files-parameters.md
    ├── lesson-5-rclpy-agents-bridging.md
    └── capstone-project.md

static/
└── code/
    └── module-1-ros2/
        ├── rclpy_examples/
        │   ├── publisher.py
        │   └── subscriber.py
        ├── service_examples/
        │   ├── service_server.py
        │   └── service_client.py
        ├── action_examples/
        │   ├── action_server.py
        │   └── action_client.py
        ├── urdf_examples/
        │   ├── robot.urdf
        │   └── urdf_controller.py
        ├── launch_examples/
        │   └── my_robot.launch.py
        └── agent_bridge_examples/
            ├── voice_command_agent.py
            └── ros_action_interface.py
```

**Structure Decision**: The module content will reside in `docs/module-1-ros2/` as Markdown files, leveraging Docusaurus features for navigation and presentation. All runnable code examples and assets will be organized under `static/code/module-1-ros2/` to ensure they are accessible and separated from the Docusaurus build process, allowing for direct execution and clear referencing from the Markdown lessons. This structure aligns with Docusaurus best practices for external assets.

## Complexity Tracking

N/A - No violations in Constitution Check requiring justification.

## Decisions Needing Documentation (from prompt)

1.  **ROS 2 Distro**: ROS 2 Humble: Long Term Support (LTS) release, stable, widely adopted, good community support, and compatible with Gazebo Classic.
2.  **Lesson Sequencing**:
    -   Introduction to ROS 2.
    -   Nodes and Topics.
    -   Services and Actions.
    -   URDF/Robot Description.
    -   Launch Files and Parameter Management.
    -   Bridging Python Agents to ROS Controllers.
3.  **Example Structure**: Examples will be standalone Python files or small ROS 2 packages organized within `static/code/module-1-ros2/`, referenced directly from Markdown.
4.  **Code Snippet Validation**: Manual local run steps, observation of console output, and visual verification in simulation (Gazebo). A comprehensive validation checklist will be maintained.
5.  **Module Content Organization**: One Markdown page per major lesson, plus an introduction and capstone project page within `docs/module-1-ros2/`.
6.  **Gazebo Integration**: Gazebo Classic (version 11) will be used initially for compatibility with ROS 2 Humble. If Iron is chosen, Gazebo Garden (Ignition) will be considered. All examples will be tested in Gazebo.
7.  **Lab Format**: Step-by-step instructions, including prerequisites, clear run commands, expected outputs (console and/or visual), verification steps, and dedicated troubleshooting tips.
8.  **Capstone Project Integration**: The capstone mini-project will serve as a culminating exercise, integrating concepts from prior lessons (voice command parsing, ROS action communication, simulated robot behavior). It will be a standalone lesson page with its own code and instructions.

## Testing Strategy (from prompt)

-   Validate all ROS 2 examples run without error on a clean Ubuntu 22.04 machine using the chosen ROS 2 distro (Humble/Iron).
-   Validate code blocks in Markdown match actual runnable code in `/static/code/module-1-ros2/`.
-   Validate simulator examples load correctly in Gazebo with URDF and joint interfaces, demonstrating expected robot behavior.
-   Confirm that tutorials follow a logical progression and align with constitution principles (clarity, reproducibility, rigor).
-   Validate all Markdown files render correctly in the Docusaurus site with proper frontmatter and navigation.
-   Ensure Jetson instructions are included and technically sound where needed (e.g., for deployment/execution of specific examples).

## Technical Details (from prompt)

-   **Workflow**: Employ a "research-while-planning" approach to resolve ambiguities and determine best practices as needed.
-   **ROS 2 Best Practices**: `rclpy` examples will use proper Quality of Service (QoS) settings where appropriate, and node lifecycle will be explained simply in conceptual sections.
-   **Consistent Example Pattern**: Each code example will follow a clear pattern: code listing → step-by-step run instructions → expected output → troubleshooting tips.
-   **Code Placement**: All runnable code, URDFs, launch files, and related assets will be located in `/static/code/module-1-ros2/` and referenced from the Docusaurus Markdown pages.
-   **Docusaurus Formatting**: Consistent use of Docusaurus formatting conventions, including frontmatter, headings, admonitions (notes, warnings), and code fences for all Markdown content.
-   **Module Phases**: The implementation will proceed through the following phases:
    1.  Lesson Architecture (defining content structure and flow).
    2.  Example Strategy (designing and implementing runnable code).
    3.  Lab Design (creating comprehensive lab guides).
    4.  Capstone Integration (developing and integrating the mini-project).
    5.  Validation Framework (establishing and executing testing procedures).
