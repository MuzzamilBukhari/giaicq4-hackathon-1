# Research & Decisions for Module 2 & 3 Implementation

## Gazebo Version Decision

**Decision**: Use Gazebo Classic for ROS 2 Humble compatibility
**Rationale**: Gazebo Classic has mature ROS 2 Humble integration and is the most stable option for educational purposes. While Ignition/Garden is the newer version, Gazebo Classic has better documentation and community support for the ROS 2 Humble LTS release.
**Alternatives considered**:
- Gazebo Garden (newer but less stable ROS 2 integration)
- Ignition Fortress (limited educational resources)

## Isaac Sim Version Decision

**Decision**: Target Isaac Sim 4.0.0 (latest stable at time of implementation)
**Rationale**: Isaac Sim 4.0.0 provides the best balance of features, stability, and documentation for educational use. It has comprehensive perception pipeline capabilities and good ROS 2 bridge support.
**Alternatives considered**:
- Isaac Sim 3.x (older but more stable)
- Isaac Sim Preview versions (more features but less stable)

## Unity Coverage Level

**Decision**: Provide visualization how-to + URDF importer guidance without full Unity project inclusion
**Rationale**: Full Unity projects are too large for repository inclusion and change frequently. Providing step-by-step instructions for the URDF importer and visualization workflows allows students to follow along without bloating the repository.
**Alternatives considered**:
- Full Unity project export (too large, version conflicts)
- Link-only approach (insufficient guidance)

## Asset Policy

**Decision**: Include only small configuration files (<100KB) in-repo; link to large assets
**Rationale**: Small URDF, SDF, USD, and JSON configuration files are essential for understanding concepts, while large mesh files and Unity scenes would bloat the repository and slow down cloning.
**Alternatives considered**:
- Include all assets (repository bloat)
- Link-only approach (reduced accessibility)

## Code Asset Location

**Decision**: Use `/static/code/module-2/` and `/static/code/module-3/` (module-specific organization)
**Rationale**: This provides clear separation of assets by module, making it easier for students to find relevant examples for each module.
**Alternatives considered**:
- Single top-level `/code/` folder (less organized by module)

## Lab Execution Model

**Decision**: Full local execution with GPU hints for Isaac Sim
**Rationale**: Students need to understand local setup and execution, but Isaac Sim requires significant GPU resources. Provide clear instructions for both local and Docker-based approaches.
**Alternatives considered**:
- Cloud-only execution (reduces local learning)

## Module Content Referencing

**Decision**: Use embedded links to detailed content rather than summary mirrors
**Rationale**: Avoiding content duplication keeps maintenance simpler and ensures information is in one authoritative location.
**Alternatives considered**:
- Summary mirrors (increases maintenance burden)