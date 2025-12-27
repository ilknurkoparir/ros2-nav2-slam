import os
from ament_index_python.packages import get_package_share_path, get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    urdf_path = os.path.join(get_package_share_path('my_robot_description'), 'urdf', 'main.xacro')
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True  
        }]
    )
    
    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        parameters=[{'use_sim_time': True}]  
    )
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', os.path.join(get_package_share_path('my_robot_description'), 'rviz', 'urdf_config.rviz')],
        parameters=[{'use_sim_time': True}]  
    )
    
    world_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'worlds',
        'home.world'
    )
    
    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
        launch_arguments={'world': world_path}.items()
    )
    
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot', '-x', '-0.09', '-y', '0.18'],
        parameters=[{'use_sim_time': True}],  
        output='screen'
    )
   
    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_node,  
        spawn_entity,
        rviz_node
    ])