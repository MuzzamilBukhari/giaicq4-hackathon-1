from omni.isaac.core import World
from omni.isaac.sensor import Camera
import numpy as np
import cv2

def setup_camera_perception():
    """Set up camera perception in Isaac Sim"""

    # Create world
    world = World(stage_units_in_meters=1.0)

    # Add default ground plane
    world.scene.add_default_ground_plane()

    # Create a camera sensor
    camera = world.scene.add(
        Camera(
            prim_path="/World/Camera",
            position=np.array([2, 2, 2]),
            frequency=30,  # 30 Hz capture rate
            resolution=(640, 480),  # Resolution
            focal_length=24.0,
            horizontal_aperture=20.955,
            clipping_range=(0.1, 1000.0)
        )
    )

    # Add some objects for the camera to see
    from omni.isaac.core.objects import DynamicCuboid
    world.scene.add(
        DynamicCuboid(
            prim_path="/World/Object1",
            name="object_1",
            position=np.array([0, 0.5, 0]),
            size=0.5,
            color=np.array([0.8, 0.1, 0.1])
        )
    )

    return world, camera

def capture_and_process_images(world, camera, num_frames=100):
    """Capture and process images from the camera"""

    world.reset()

    for i in range(num_frames):
        world.step(render=True)

        if i % 10 == 0:  # Process every 10th frame
            try:
                # Get RGB image
                rgb_image = camera.get_rgb()

                # Get depth image
                depth_image = camera.get_depth()

                # Get semantic segmentation (if available)
                try:
                    segmentation = camera.get_semantic_segmentation()
                except:
                    segmentation = None

                print(f"Captured frame {i}: RGB shape={rgb_image.shape if rgb_image is not None else 'None'}, "
                      f"Depth shape={depth_image.shape if depth_image is not None else 'None'}")

                # Example processing: calculate average RGB values
                if rgb_image is not None:
                    avg_rgb = np.mean(rgb_image, axis=(0, 1))
                    print(f"  Average RGB: [{avg_rgb[0]:.1f}, {avg_rgb[1]:.1f}, {avg_rgb[2]:.1f}]")

            except Exception as e:
                print(f"Error capturing image: {e}")

def main():
    world, camera = setup_camera_perception()
    capture_and_process_images(world, camera, num_frames=50)
    print("Camera perception example completed!")

if __name__ == "__main__":
    main()