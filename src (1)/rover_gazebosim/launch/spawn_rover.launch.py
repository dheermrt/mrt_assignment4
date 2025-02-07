import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import xacro


def generate_launch_description():
    # Load robot description from URDF file
    robot_description = xacro.process_file(
        os.path.join(get_package_share_directory('rover_gazebosim'), 'urdf/urdf/rover.urdf')
    ).toxml()

    # Load configuration for parameter bridge
    config_file = os.path.join(get_package_share_directory('rover_gazebosim'), 'config', 'parameter_bridge.yaml')
    rviz_config_file=os.path.join(get_package_share_directory('rover_gazebosim'),'config','rover.rviz')
    ekf_config_file = os.path.join(get_package_share_directory('rover_gazebosim'), 'config', 'ekf_config.yaml')
    slam_config_file=os.path.join(get_package_share_directory('rover_gazebosim'),'config','mapper_params_online_async.yaml')

    return LaunchDescription([
        # Launch arguments for GUI and initial position
        DeclareLaunchArgument('gui', default_value='true', description='Enable/Disable GUI'),
        DeclareLaunchArgument('x', default_value='0', description='Initial x position of the rover'),
        DeclareLaunchArgument('y', default_value='0', description='Initial y position of the rover'),
        DeclareLaunchArgument('z', default_value='0.5', description='Initial z position of the rover'),

        # Set environment variables for resource paths
        SetEnvironmentVariable(
            name='IGN_GAZEBO_RESOURCE_PATH',
            value=os.path.join(get_package_share_directory('rover_gazebosim'), 'meshes') + ':' +
                  os.path.join(get_package_share_directory('rover_gazebosim'), 'urdf')
        ),

        # Launch Ignition Gazebo with a specific world file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
            ),
            launch_arguments={
                "gz_args": "~/mrt_ws/src/rover_gazebosim/worlds/empty.sdf"
            }.items(),
        ),

        # Robot State Publisher for publishing the robot's URDF to the parameter server
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{"robot_description": robot_description}]
        ),

        # Joint State Publisher for publishing joint states
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_gui': LaunchConfiguration('gui')}]
        ),

        # Spawn the rover in Ignition Gazebo
        Node(
            package="ros_gz_sim",
            executable="create",
            output="screen",
            name="rover_spawn",
            arguments=[
                "-string", robot_description,
                "-name", "rover",
                "-x", LaunchConfiguration("x"),
                "-y", LaunchConfiguration("y"),
                "-z", LaunchConfiguration("z"),
            ],
        ),

        # ROS-Gazebo Bridge for parameter communication
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{'config_file': config_file}]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d',rviz_config_file],
        ),
         # Launch robot_localization (EKF node)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_localization_node',
            output='screen',
            parameters=[ekf_config_file]
        ),
        # Node(
        #     package='pointcloud_to_laserscan',
        #     executable='pointcloud_to_laserscan_node',
        #     name='pointcloud_to_laserscan',
        #     parameters=[{
        #         'range_min': 0.1,
        #         'range_max': 30.0,
        #         'scan_time': 0.1,
        #         'use_inf': True,
        #         'target_frame': 'sensor_laser',  # Replace with your robot's base frame
        #         'transform_tolerance': 0.3,
        #         'queue_size': 50
            
        #     }], 
        #     remappings=[
        #         ('cloud_in', '/laser_scan'),   # Input PointCloud2 topic
        #         ('scan', '/scan')             # Output LaserScan topic
        #     ]
        # ),
        #   Node(
        #    package='slam_toolbox',
        #     executable='sync_slam_toolbox_node',
        #     name='slam_toolbox',
        #     output='screen',
        #     parameters=[slam_config_file]  # Replace with your config path
        # ),
      
    ])

 
