---
title: Chapter 1 - Isaac Sim Setup
sidebar_position: 1
description: Learn how to install and configure NVIDIA Isaac Sim, understand USD workflow, import assets, and create basic scenes.
---

# Chapter 1: Isaac Sim Setup

## Overview

This chapter introduces NVIDIA Isaac Sim, a powerful GPU-accelerated simulation environment built on NVIDIA's Omniverse platform. You'll learn how to install and configure Isaac Sim, understand the Universal Scene Description (USD) workflow, import assets, and create basic simulation scenes.

## Learning Objectives

By the end of this chapter, you will be able to:
- Install and configure NVIDIA Isaac Sim with Omniverse
- Understand the Universal Scene Description (USD) workflow and format
- Import and create assets for Isaac Sim environments
- Create and configure basic simulation scenes
- Set up the development environment for Isaac Sim workflows

## 1.1 Omniverse Installation Basics

NVIDIA Isaac Sim runs on the Omniverse platform, which provides real-time collaboration and simulation capabilities. Proper installation is crucial for leveraging Isaac Sim's full potential.

### System Requirements

Before installing Isaac Sim, ensure your system meets the requirements:

**Minimum Requirements:**
- **GPU**: NVIDIA GPU with Compute Capability 6.0 or higher (Pascal architecture or newer)
- **VRAM**: 8GB or more recommended
- **CPU**: Multi-core processor (Intel i7 or AMD Ryzen 7)
- **RAM**: 16GB or more
- **OS**: Ubuntu 20.04 LTS or 22.04 LTS (recommended), Windows 10/11

**Recommended Requirements:**
- **GPU**: NVIDIA RTX 3080/4080 or A40/A6000 for optimal performance
- **VRAM**: 16GB or more for complex scenes
- **RAM**: 32GB or more
- **Storage**: SSD with 50GB+ free space

### Installation Methods

Isaac Sim can be installed using several methods:

1. **Docker Installation** (Recommended for development)
2. **Native Installation** (For production use)
3. **Isaac Sim Omniverse App** (For standalone use)

### Docker Installation (Recommended)

Docker installation provides the most consistent environment and is recommended for development:

```bash
# Pull the Isaac Sim Docker image
docker pull nvcr.io/nvidia/isaac-sim:4.0.0

# Run Isaac Sim with GPU support
docker run --gpus all -it --rm \
  --network=host \
  --env "ACCEPT_EULA=Y" \
  --env "NVIDIA_VISIBLE_DEVICES=all" \
  --env "NVIDIA_DRIVER_CAPABILITIES=all" \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  --env "DISPLAY=$DISPLAY" \
  --volume $HOME/.Xauthority:/root/.Xauthority \
  --runtime=nvidia \
  --env "PRIVACY_CONSENT=Y" \
  nvcr.io/nvidia/isaac-sim:4.0.0
```

### Native Installation

For native installation on Ubuntu:

1. **Install NVIDIA GPU drivers** (latest recommended)
2. **Install Isaac Sim dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-dev python3-venv
   ```

3. **Download Isaac Sim** from NVIDIA Developer website
4. **Extract and install**:
   ```bash
   tar -xzf isaac-sim-4.0.0.tar.gz
   cd isaac-sim-4.0.0
   ./install.sh
   ```

### Omniverse Nucleus Setup

For multi-user collaboration, set up Omniverse Nucleus:

1. **Install Omniverse Nucleus** on a central server
2. **Configure access permissions** for team members
3. **Set up asset libraries** for shared resources

## 1.2 USD Workflow

Universal Scene Description (USD) is Pixar's format for 3D scene interchange. Isaac Sim uses USD extensively for scene definition, asset management, and simulation setup.

### USD Fundamentals

USD is a powerful scene description framework that enables:

- **Layered Composition**: Combine multiple scene layers
- **Variant Sets**: Different versions of the same asset
- **Payloads**: Deferred loading of complex assets
- **References**: Asset reuse and instancing

### USD File Structure

A typical USD file has the structure:

```usd
#usda 1.0
(
    doc = "Example USD scene for Isaac Sim"
    metersPerUnit = 1.0
    upAxis = "Y"
)

def Xform "World"
{
    def Xform "Robot" (
        prepend references = @./robot.usd@
    )
    {
        matrix4d xformOp:transform = ( (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1) )
    }

    def Xform "Environment" (
        prepend references = @./environment.usd@
    )
    {
    }
}
```

### USD Prim Types in Isaac Sim

Isaac Sim extends USD with robotics-specific prim types:

- **Robot Prims**: Define robot kinematics and dynamics
- **Sensor Prims**: Camera, LiDAR, IMU, etc.
- **Actuator Prims**: Joint controllers and motors
- **RigidBody Prims**: Physics-enabled objects

### USD Tools and Editors

Several tools help work with USD:

1. **Isaac Sim Editor**: Visual editor for USD scenes
2. **USDView**: Pixar's reference USD viewer
3. **Code-based tools**: Python API for USD manipulation

### Example USD Scene Creation

Creating a simple scene programmatically:

```python
import omni
from pxr import Usd, UsdGeom, Gf, Sdf

def create_simple_scene(stage_path):
    """Create a simple USD scene with ground and objects"""

    # Create a new stage
    stage = Usd.Stage.CreateNew(stage_path)

    # Set up scene units
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # Create world Xform
    world = UsdGeom.Xform.Define(stage, "/World")

    # Create ground plane
    ground = UsdGeom.Mesh.Define(stage, "/World/Ground")
    ground.CreatePointsAttr([(-10, 0, -10), (10, 0, -10), (10, 0, 10), (-10, 0, 10)])
    ground.CreateFaceVertexIndicesAttr([0, 1, 2, 0, 2, 3])
    ground.CreateFaceVertexCountsAttr([3, 3])

    # Create a cube object
    cube = UsdGeom.Cube.Define(stage, "/World/Cube")
    cube.AddTranslateOp().Set((0, 1, 0))
    cube.CreateSizeAttr(1.0)

    # Save the stage
    stage.GetRootLayer().Save()
    print(f"Scene saved to: {stage_path}")

# Usage
create_simple_scene("simple_scene.usd")
```

## 1.3 Asset Import & Creation

Isaac Sim supports various asset formats and provides tools for creating and importing 3D assets for simulation.

### Supported Asset Formats

Isaac Sim supports multiple asset formats:

- **USD**: Native format, preferred for complex scenes
- **FBX**: Industry standard for 3D models
- **OBJ**: Simple geometry format
- **GLTF/GLB**: Web-friendly 3D format
- **Alembic**: Animation and geometry cache

### Asset Import Process

The asset import process involves:

1. **Prepare Assets**: Ensure proper scale, units, and coordinate systems
2. **Import to Omniverse**: Use Isaac Sim's import tools
3. **Add Physics**: Configure collision shapes and materials
4. **Validate**: Check for proper behavior in simulation

### Creating Robot Assets

When creating robot assets for Isaac Sim:

1. **Kinematic Structure**: Define joint hierarchy properly
2. **Collision Geometry**: Create appropriate collision meshes
3. **Visual Materials**: Apply realistic materials and textures
4. **Physical Properties**: Set mass, friction, and damping

Example of defining a simple robot in USD:

```usd
#usda 1.0
(
    doc = "Simple robot for Isaac Sim"
    metersPerUnit = 1.0
    upAxis = "Y"
)

def Xform "Robot"
{
    def Xform "Base"
    {
        def Cube "Link"
        {
            size = 0.5
            extent = [(-0.25, -0.25, -0.25), (0.25, 0.25, 0.25)]
        }

        def PhysicsRigidBodyAPI "Link"
        {
            physics:mass = 10.0
            physics:diagonalInertia = (1.0, 1.0, 1.0)
        }
    }

    def Xform "Arm"
    {
        def Joint "Joint1"
        {
            joint:localRotOrder = "ZYX"
            joint:physics:axis = "X"
            joint:physics:limit:low = -1.57
            joint:physics:limit:high = 1.57
        }

        def Cube "Link"
        {
            size = 0.3
            extent = [(-0.15, -0.15, -0.15), (0.15, 0.15, 0.15)]
        }
    }
}
```

### Asset Optimization

For optimal performance in Isaac Sim:

- **Reduce Polygon Count**: Use appropriate level of detail
- **Optimize Textures**: Use compressed formats and appropriate resolution
- **Instance Repeated Objects**: Use instancing for multiple similar objects
- **Use LODs**: Implement Level of Detail for distant objects

### Isaac Sim Asset Library

Isaac Sim provides a rich asset library:

- **Robot Models**: Pre-built robot models with kinematics
- **Environments**: Indoor and outdoor environments
- **Objects**: Common objects for manipulation tasks
- **Sensors**: Pre-configured sensor models

## 1.4 Isaac Sim Scene Basics

Creating effective simulation scenes in Isaac Sim involves understanding the core components and best practices.

### Scene Hierarchy

A typical Isaac Sim scene follows this hierarchy:

```
/World
├── /Environments
│   ├── /Room
│   └── /Outdoor
├── /Robots
│   ├── /Robot1
│   └── /Robot2
├── /Objects
│   ├── /ManipulationObjects
│   └── /Obstacles
└── /Sensors
    ├── /Camera1
    └── /LiDAR1
```

### Essential Scene Components

Every Isaac Sim scene should include:

1. **World Origin**: Proper coordinate system setup
2. **Physics Scene**: Configuration for physics simulation
3. **Lighting**: Proper illumination for realistic rendering
4. **Ground Plane**: Base for objects to rest on

### Creating Scenes Programmatically

Using Isaac Sim's Python API to create scenes:

```python
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.sensor import Camera
import numpy as np

class IsaacSimScene:
    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)

    def setup_basic_scene(self):
        """Setup a basic scene with ground, lighting, and physics"""

        # Create ground plane
        create_prim(
            prim_path="/World/GroundPlane",
            prim_type="Plane",
            position=np.array([0, 0, 0]),
            orientation=np.array([0, 0, 0, 1])
        )

        # Add physics material to ground
        create_prim(
            prim_path="/World/PhysicsMaterial",
            prim_type="PhysicsMaterial",
            mass_density=1000,
            dynamic_friction=0.5,
            static_friction=0.5,
            restitution=0.1
        )

        # Create a simple robot
        add_reference_to_stage(
            usd_path="path/to/robot.usd",
            prim_path="/World/Robot"
        )

        # Add a camera
        camera = Camera(
            prim_path="/World/Camera",
            position=np.array([2, 2, 2]),
            orientation=np.array([0.5, 0.5, 0.5, 0.5])
        )

        # Setup physics scene
        self.world.scene.add_default_ground_plane()

    def run_simulation(self):
        """Run the simulation loop"""
        self.world.reset()

        for i in range(1000):  # Run for 1000 steps
            self.world.step(render=True)

            # Add your simulation logic here
            if i % 100 == 0:
                print(f"Simulation step: {i}")

# Usage
scene = IsaacSimScene()
scene.setup_basic_scene()
scene.run_simulation()
```

### Scene Configuration Parameters

Key parameters for scene configuration:

- **Simulation Frequency**: Physics update rate (typically 60-240 Hz)
- **Render Frequency**: Graphics update rate (typically 30-60 Hz)
- **Gravity**: Default -9.81 m/s² in Y direction (or Z in some configurations)
- **Physics Solver**: Parameters for stability and accuracy

### Best Practices

- **Use Appropriate Scale**: Keep objects at realistic scales for physics stability
- **Optimize for Performance**: Balance visual quality with simulation speed
- **Validate Physics**: Ensure objects behave realistically in simulation
- **Test with Sensors**: Verify sensor data quality in the scene

## Summary

This chapter covered the fundamentals of setting up NVIDIA Isaac Sim, including installation, USD workflow understanding, asset management, and basic scene creation. You learned about the Omniverse platform, USD format for scene description, and how to create effective simulation environments. These foundational skills are essential for leveraging Isaac Sim's advanced capabilities in the subsequent chapters.

## Next Steps

In the next chapter, you'll explore Isaac Sim's powerful perception pipeline capabilities, including synthetic sensor generation and data processing for robotics applications.

## External Resources

- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/isaacsim.html)
- [Universal Scene Description (USD) Documentation](https://graphics.pixar.com/usd/release/docs/index.html)
- [Omniverse Developer Resources](https://developer.nvidia.com/omniverse)
- [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/index.html)