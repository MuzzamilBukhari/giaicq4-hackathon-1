---
ID: 2
TITLE: Module 1 ROS 2 Fundamentals Tasks
STAGE: tasks
DATE_ISO: 2025-12-05
SURFACE: agent
MODEL: claude-sonnet-4-5-20250929
FEATURE: 001-ros2-fundamentals
BRANCH: 001-ros2-fundamentals
USER:
COMMAND: /sp.tasks
LABELS: ["ros2", "fundamentals", "tasks", "docusaurus"]
LINKS:
  SPEC: specs/001-ros2-fundamentals/spec.md
  PLAN: specs/001-ros2-fundamentals/plan.md
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - specs/001-ros2-fundamentals/tasks.md
TESTS_YAML: []
---
## Prompt
```text
Feature: Module 1 — ROS 2 Fundamentals (Docusaurus-ready)

Goal: Produce a complete set of atomic tasks that create Module 1 as Docusaurus pages + runnable example assets. Each task must produce files in the repository and include acceptance criteria that can be validated locally/CI.

Deliverables (files to be created/modified):
- docs/module-1-ros2/intro.md
- docs/module-1-ros2/lesson-1-nodes-topics.md
- docs/module-1-ros2/lesson-2-services-actions.md
- docs/module-1-ros2/lesson-3-rclpy-patterns.md
- docs/module-1-ros2/lesson-4-urdf-robot-description.md
- docs/module-1-ros2/lesson-5-launch-files-and-params.md
- docs/module-1-ros2/lesson-6-agent-to-ros-bridge.md
- docs/module-1-ros2/labs/<lab pages>.md (one lab per major lesson)
- docs/module-1-ros2/capstone.md
- static/code/module-1/ (contains runnable packages/scripts/URDFs/launch files)
- specs/2-module-1-ros2/checklists/build-validate.md
- specs/2-module-1-ros2/checklists/run-verify.md

Task list (atomic, ordered):

1. Decide ROS 2 Distro (atomic decision)
   - Output: specs/2-module-1-ros2/decision-ros-distro.md
   - Action: Lock target distro (Humble) and record rationale + test matrix (Ubuntu 22.04, Jetson notes).
   - Acceptance: File exists and states distro = Humble with justification.

2. Create docs folder for Module 1
   - Output: docs/module-1-ros2/ (empty placeholders)
   - Action: Create directory and add README/intro.md with frontmatter.
   - Acceptance: intro.md contains frontmatter and module overview.

3. Create chapter template file
   - Output: docs/module-1-ros2/_chapter-template.md (hidden helper)
   - Action: Add frontmatter template and required sections (objectives, summary, examples, exercises, troubleshooting).
   - Acceptance: Template exists and is referenced by all lesson pages.

4. Author Lesson 1: Nodes & Topics page
   - Output: docs/module-1-ros2/lesson-1-nodes-topics.md
   - Action: Write learning objectives, conceptual explanation, small runnable example snippet (publisher/subscriber), run instructions, expected output, troubleshooting.
   - Acceptance: Page renders with frontmatter and includes a referenced script path in static/code/module-1/.

5. Add runnable publisher/subscriber example
   - Output: static/code/module-1/pub_sub_demo/ (Python rclpy files + package.xml + README)
   - Action: Create minimal ROS 2 Python package with publisher and subscriber examples and step-by-step run commands.
   - Acceptance: README contains `colcon build` and run steps; examples are referenced from lesson-1.

6. Author Lesson 2: Services & Actions page
   - Output: docs/module-1-ros2/lesson-2-services-actions.md
   - Action: Explanations, code snippets (service server/client, action server/client), step-by-step lab plan.
   - Acceptance: Page references static/code/module-1/service_action_demo.

7. Add runnable service & action example
   - Output: static/code/module-1/service_action_demo/ (Python ROS 2 package)
   - Action: Provide minimal service server/client and action server/client with README run steps and expected output.
   - Acceptance: Build/run steps validated in README.

8. Author Lesson 3: rclpy patterns & node lifecycle (practical)
   - Output: docs/module-1-ros2/lesson-3-rclpy-patterns.md
   - Action: Show common rclpy idioms, QoS example, simple lifecycle or proper node shutdown handling, small example code.
   - Acceptance: Example referenced in static/code/module-1/rclpy_patterns.

9. Add rclpy examples
   - Output: static/code/module-1/rclpy_patterns/
   - Action: Add small examples demonstrating QoS and safe shutdown.
   - Acceptance: README run steps + expected outputs included.

10. Author Lesson 4: URDF & Robot Description
    - Output: docs/module-1-ros2/lesson-4-urdf-robot-description.md
    - Action: Explain URDF basics, joints/links, sensors, include a minimal humanoid proxy URDF and loading instructions in Gazebo.
    - Acceptance: Page references static/code/module-1/urdf_demo.

11. Add URDF + Gazebo integration demo
    - Output: static/code/module-1/urdf_demo/ (URDF, meshes if needed, simple launch to spawn in Gazebo)
    - Action: Provide launch file and instructions to spawn robot in Gazebo and verify topics (e.g., /tf, /joint_states).
    - Acceptance: README includes `ros2 launch` example and expected topic outputs.

12. Author Lesson 5: Launch Files & Parameter Management
    - Output: docs/module-1-ros2/lesson-5-launch-files-and-params.md
    - Action: Explain launch composition, passing parameters, remapping, and an example that composes pub/sub and URDF spawn.
    - Acceptance: Page references static/code/module-1/launch_examples.

13. Add launch examples and parameter files
    - Output: static/code/module-1/launch_examples/
    - Action: Create sample launch files, parameter YAML, and instructions to run full example.
    - Acceptance: Launch example starts nodes and demonstrates parameter override.

14. Author Lesson 6: Agent → ROS bridge
    - Output: docs/module-1-ros2/lesson-6-agent-to-ros-bridge.md
    - Action: Show architecture of a Python agent sending commands to ROS (e.g., via service/action). Include a tiny bridge example connecting a text command to an action call.
    - Acceptance: Page references static/code/module-1/agent_bridge_demo.

15. Add Agent-to-ROS bridge example
    - Output: static/code/module-1/agent_bridge_demo/ (simple script + README)
    - Action: Provide a script that accepts a command and triggers a ROS action in simulation.
    - Acceptance: README run steps and verification steps included.

16. Create Lab pages for each lesson
    - Output: docs/module-1-ros2/labs/lab-1-nodes-topics.md ... lab-6-agent-bridge.md
    - Action: Each lab includes prerequisites, step-by-step tasks, expected outputs, verification checklist, and troubleshooting tips.
    - Acceptance: Lab pages exist and link back to their lesson pages.

17. Capstone page & scaffold
    - Output: docs/module-1-ros2/capstone.md
    - Action: Define capstone mini-project "Voice command → ROS action → simulated robot behavior", provide scaffold steps, expected deliverables, and reference files.
    - Acceptance: Capstone contains checklist and references to any reused demo code (e.g., agent_bridge_demo).

18. Create module-level validation checklists
    - Output: specs/2-module-1-ros2/checklists/build-validate.md and run-verify.md
    - Action: Include `colcon build` checklist, ros2 run commands to validate each demo, Gazebo checks, and Jetson notes.
    - Acceptance: Checklists are explicit and can be executed manually/CI.

19. Add Docusaurus frontmatter & sidebar registration
    - Output: frontmatter in all docs files; update sidebars.js to include Module 1 ordering
    - Action: Ensure sidebar_position and ids are deterministic and module appears under "Modules" in sidebar.
    - Acceptance: Sidebar file contains module entries and pages have matching IDs.

20. Local smoke test
    - Output: local validation notes saved to specs/2-module-1-ros2/checklists/build-validate.md
    - Action: Run `npm run build` (Docusaurus), `colcon build` for examples, `ros2 launch` sample - record successes/failures.
    - Acceptance: All primary examples build and at least basic run steps succeed on Ubuntu 22.04 with ROS 2 Humble. Failures documented.

21. Jetson notes & optional emulation
    - Output: docs/module-1-ros2/jetson-notes.md
    - Action: Add Jetson Orin/Orin Nano-specific instructions, cross-compilation or flash notes, and any emulation tips if no Jetson hardware available.
    - Acceptance: Page contains practical steps and caveats.

22. Commit, branch, and PR creation
    - Output: branch `feature/module-1-ros2`, PR link in specs/2-module-1-ros2/contracts/pr-links.md
    - Action: Commit all created files, push branch, and open PR referencing spec & plan.
    - Acceptance: PR exists and is linked in contracts file.

Acceptance criteria (global):
- All listed deliverable files exist with correct frontmatter.
- Each static/code demo contains a README with `colcon build` + run steps and expected outputs.
- Docusaurus build completes and module pages render in sidebar.
- At least one demo (pub/sub or service) is validated to run end-to-end on Ubuntu 22.04 with ROS 2 Humble.
- Checklists document how to reproduce verification steps.

Priority & sequencing:
- High: tasks 1 → 2 → 4 → 5 → 6 → 7 → 11 → 12 → 19 → 20
- Medium: tasks 8 → 9 → 10 → 13 → 14 → 15
- Low: tasks 16 → 17 → 18 → 21 → 22

Notes:
- Keep code examples minimal and modular; prefer short packages over monolithic scripts.
- Use deterministic IDs and sidebar_position to avoid navigation drift.
- Document expected ROS versions and any simulator version constraints (Gazebo classic vs Ignition).
- If Jetson hardware is unavailable, provide emulation or cross-build guidance and mark as "optional hardware step".
```

## Response

The `tasks.md` file has been generated successfully at `specs/001-ros2-fundamentals/tasks.md`.

**Summary**:
*   **Total Task Count**: 22
*   **Tasks per User Story**:
    *   User Story 1 (Learning ROS 2 Core Concepts): 4 tasks
    *   User Story 2 (Building Robot Descriptions and Launching Systems): 4 tasks
    *   User Story 3 (Bridging Python Agents to ROS Controllers): 2 tasks
    *   Setup Phase: 3 tasks
    *   Polish & Cross-Cutting Concerns Phase: 9 tasks
*   **Parallel Opportunities**: Identified within each user story phase.
*   **Independent Test Criteria**: Defined for each user story in `specs/001-ros2-fundamentals/spec.md`.
*   **Suggested MVP Scope**: User Story 1 (T004 - T007) represents the initial MVP.
*   **Format Validation**: All tasks adhere to the required checklist format.
