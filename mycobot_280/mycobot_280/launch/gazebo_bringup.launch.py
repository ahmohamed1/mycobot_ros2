import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import  ExecuteProcess, RegisterEventHandler
from launch.event_handlers import (OnExecutionComplete, OnProcessExit,
                                OnProcessIO, OnProcessStart, OnShutdown)

from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'mycobot_description'
    file_subpath = 'urdf/mycobot_urdf.urdf.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )


    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2','control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
             output='screen'
    )
    load_arm_controller = ExecuteProcess(
        cmd=['ros2','control', 'load_controller', '--set-state', 'active',
             'mycobot_arm_controller'],
             output='screen'
    )


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        )


    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'mycobot'],
                    output='screen')




    # Run the node
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller])
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_arm_controller])
        ),
        gazebo,
        node_robot_state_publisher,
        spawn_entity
        
    ])


