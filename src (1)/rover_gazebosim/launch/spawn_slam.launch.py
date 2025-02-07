import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import xacro

def generate_launch_description():
     slam_config_file=os.path.join(get_package_share_directory('rover_gazebosim'),'config','mapper_params_online_async.yaml')
     return LaunchDescription([
     Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_config_file]  # Replace with your config path
        ),
     ])