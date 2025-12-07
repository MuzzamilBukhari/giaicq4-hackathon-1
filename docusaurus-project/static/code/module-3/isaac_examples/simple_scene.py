import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.utils.viewports import set_camera_view
import numpy as np

def create_simple_scene():
    """Create a simple Isaac Sim scene with basic objects"""

    # Create world with 1m units
    world = World(stage_units_in_meters=1.0)

    # Add default ground plane
    world.scene.add_default_ground_plane()

    # Create a simple robot (using a cube as placeholder)
    from omni.isaac.core.objects import DynamicCuboid
    robot = world.scene.add(
        DynamicCuboid(
            prim_path="/World/Robot",
            name="simple_robot",
            position=np.array([0, 0.5, 0]),
            size=0.3,
            color=np.array([0.8, 0.1, 0.1])  # Red color
        )
    )

    # Add some objects for the robot to interact with
    cube1 = world.scene.add(
        DynamicCuboid(
            prim_path="/World/Cube1",
            name="cube_1",
            position=np.array([1, 0.5, 1]),
            size=0.2,
            color=np.array([0.1, 0.8, 0.1])  # Green color
        )
    )

    cube2 = world.scene.add(
        DynamicCuboid(
            prim_path="/World/Cube2",
            name="cube_2",
            position=np.array([-1, 0.5, -1]),
            size=0.2,
            color=np.array([0.1, 0.1, 0.8])  # Blue color
        )
    )

    # Set camera view for visualization
    set_camera_view(eye=np.array([3, 3, 3]), target=np.array([0, 0, 0]))

    return world, robot, [cube1, cube2]

def run_simple_simulation():
    """Run a simple simulation with the created scene"""

    world, robot, objects = create_simple_scene()

    # Reset the world
    world.reset()

    # Run simulation for 1000 steps
    for i in range(1000):
        world.step(render=True)

        # Simple "control" - just print progress
        if i % 100 == 0:
            print(f"Simulation step: {i}")

    print("Simulation completed!")

if __name__ == "__main__":
    run_simple_simulation()