# Research Summary: Module 4 — Vision-Language-Action & Humanoid Robotics

## Decisions Made

### 1. Mathematical Depth for Kinematics and Locomotion
**Decision**: Use simplified numeric demonstrations rather than complex symbolic approaches
**Rationale**: The target audience consists of undergraduate students who need to understand core concepts without getting overwhelmed by advanced mathematics. The spec specifically states to "avoid advanced control theory derivations beyond simplified MPC and ZMP concepts."
**Alternatives considered**:
- Full symbolic FK/IK solvers using libraries like SymPy (rejected - too complex for target audience)
- Pure conceptual explanations without code examples (rejected - students need hands-on experience)

### 2. Simulation Environment for Labs
**Decision**: Focus on Gazebo Classic with optional Isaac Sim references
**Rationale**: Gazebo is widely used in ROS 2 ecosystem and well-integrated with the existing curriculum. The existing modules already cover Gazebo and Isaac Sim, so we'll maintain consistency while keeping labs simulation-only as required.
**Alternatives considered**:
- Unity Robotics (requires additional licensing and setup)
- Isaac Sim only (not all students may have access to NVIDIA hardware)
- Custom Python simulation (insufficient for realistic robotics concepts)

### 3. VLA Example Implementation
**Decision**: Use mock pipeline approach rather than real model APIs
**Rationale**: The spec explicitly states "No large ML models included in repo; examples must be lightweight conceptual or pseudo-code." Mock pipeline demonstrates concepts without requiring heavy computational resources.
**Alternatives considered**:
- Integration with real VLA models like RT-2 or VIMA (rejected - violates lightweight constraint)
- Pure theoretical explanations (rejected - students need practical examples)

### 4. Humanoid Model Simplification
**Decision**: Use simplified 2-link arm model and 3-link leg model for demonstrations
**Rationale**: This provides realistic enough examples for learning while keeping complexity manageable. Students can understand the concepts without getting bogged down in complex multi-link kinematics.
**Alternatives considered**:
- Full humanoid model with 20+ joints (rejected - too complex for learning)
- Simple point-mass model (rejected - insufficient for kinematics learning)

### 5. Action Grounding Format
**Decision**: Use JSON schema for structured robot commands with clear field definitions
**Rationale**: JSON provides a clear, human-readable format that demonstrates the concept of action grounding without being tied to specific implementation details. It's also easily extensible.
**Alternatives considered**:
- ROS 2 action messages only (insufficient for demonstrating grounding concepts)
- Custom text format (less standard and harder to parse)

### 6. Example Assets Storage
**Decision**: Store in `static/code/module-4/` as specified in the original requirements
**Rationale**: This maintains consistency with the project structure and keeps all Module 4 assets in one organized location.
**Alternatives considered**:
- Embedding directly in documentation (not reusable)
- Separate repository (unnecessary complexity for educational examples)

### 7. Diagram Format
**Decision**: Use ASCII diagrams in documentation with references to external image files where needed
**Rationale**: ASCII diagrams are directly embeddable in markdown and don't require external hosting. For more complex diagrams, we'll reference static images that can be stored in the Docusaurus static assets.
**Alternatives considered**:
- Inline SVG diagrams (more complex to maintain)
- External image hosting (potential link rot issues)

### 8. ROS 2 Action Structure
**Decision**: Create conceptual action message examples that demonstrate the structure without implementing full ROS 2 nodes
**Rationale**: Students need to understand the concept of ROS 2 actions for VLA systems without getting bogged down in implementation details. The focus is on the educational concept.
**Alternatives considered**:
- Full working ROS 2 action implementations (too complex for educational examples)
- Pure theoretical explanations (insufficient for hands-on learning)