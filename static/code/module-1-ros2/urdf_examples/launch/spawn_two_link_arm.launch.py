import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # Get the URDF file
    urdf_file_name = 'two_link_arm.urdf'
    urdf_path = os.path.join(
        get_package_share_directory('urdf_examples'),
        'urdf',
        urdf_file_name)

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': Command(['xacro ', urdf_path])}
        ]
    )

    # Joint State Publisher GUI (optional, for controlling joints)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=LaunchConfiguration('use_gui', default='true')
    )

    # Gazebo related nodes
    # Include the Gazebo launch file
    gazebo_launch_file = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch',
        'gazebo.launch.py'
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={'verbose': 'true'}.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-file', urdf_path,
                                   '-entity', 'two_link_arm'],
                        output='screen')


    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node, # Optional for direct joint control
        # Uncomment these lines if you want to launch Gazebo directly from this launch file
        # gazebo_server,
        # spawn_entity,
    ])