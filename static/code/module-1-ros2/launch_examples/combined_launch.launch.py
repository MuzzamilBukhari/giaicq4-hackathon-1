import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Get paths
    pub_sub_share_dir = get_package_share_directory('pub_sub_demo')
    urdf_share_dir = get_package_share_directory('urdf_examples')
    gazebo_ros_share_dir = get_package_share_directory('gazebo_ros')

    # URDF file path
    urdf_file_name = 'two_link_arm.urdf'
    urdf_path = os.path.join(urdf_share_dir, 'urdf', urdf_file_name)

    # Gazebo launch file
    gazebo_launch_file = os.path.join(
        gazebo_ros_share_dir,
        'launch',
        'gazebo.launch.py'
    )

    # Nodes from pub_sub_demo package
    publisher_node = Node(
        package='pub_sub_demo',
        executable='minimal_publisher',
        name='publisher',
        output='screen',
    )

    subscriber_node = Node(
        package='pub_sub_demo',
        executable='minimal_subscriber',
        name='subscriber',
        output='screen',
    )

    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': Command(['xacro ', urdf_path])}
        ]
    )

    # Gazebo server
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={'verbose': 'false'}.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-file', urdf_path,
                                   '-entity', 'two_link_arm'],
                        output='screen')

    return LaunchDescription([
        publisher_node,
        subscriber_node,
        robot_state_publisher_node,
        gazebo_server,
        spawn_entity,
    ])