import launch
from launch_ros.actions import Node

def generate_launch_description():
    # Launch the joint state publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen',
        arguments=['$(find YOUR_ROBOT_DESCRIPTION_PACKAGE)/YOUR_ROBOT_DESCRIPTION.urdf']
    )

    # Launch the robot state publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        arguments=['$(find YOUR_ROBOT_DESCRIPTION_PACKAGE)/YOUR_ROBOT_DESCRIPTION.urdf']
    )

    # Launch the MoveIt planning execution node
    moveit_execution_manager_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        name='move_group',
        output='screen'
    )

    return launch.LaunchDescription([
        joint_state_publisher_node,
        robot_state_publisher_node,
        moveit_execution_manager_node
    ])

if __name__ == '__main__':
    generate_launch_description()