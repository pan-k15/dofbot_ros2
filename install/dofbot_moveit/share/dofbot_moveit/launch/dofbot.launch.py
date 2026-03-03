import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import TimerAction, RegisterEventHandler
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    package_name = 'dofbot_moveit'
    
    # Command to get robot description from xacro file
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution([FindPackageShare(package_name), "urdf", 'dofbot.urdf.xacro']),
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # RViz config file path
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare(package_name), "rviz", "view_robot.rviz"]
    )

    # Nodes for joint state publisher, robot state publisher, and RViz
    # joint_state_publisher_node = Node(
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui",
    # )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    # Controller parameters file path
    controller_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'controller.yaml')

    # Controller manager node
    # controller_manager_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[controller_params_file],
    #     output={
    #         "stdout": "screen",
    #         "stderr": "screen",
    #     },
    # )
    # controller_manager_node = Node(
    #     package="controller_manager",
    #     executable="ros2_control_node",
    #     parameters=[
    #         robot_description,
    #         controller_params_file
    #     ],
    #     output="screen",
    # )
    controller_manager_node = Node(
    package="controller_manager",
    executable="ros2_control_node",
    parameters=[
        robot_description,
        controller_params_file,
        {"robot_description_topic": ""}
    ],
    output="screen",
)
    joint_state_broadcaster_spawner = Node(
    package="controller_manager",
    executable="spawner",
    arguments=["joint_state_broadcaster"],
    output="screen",
)
    # Joint trajectory controller spawner node
    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["dofbot_controller"],
        output="screen"
    )
    # Joint trajectory controller spawner node
    joint_trajectory_controller_gripper_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_controller"],
        output="screen"
    )
    # Define the launch sequence with delays
    nodes_to_start = [
        #joint_state_publisher_node,
        robot_state_publisher_node,
        #rviz_node,
        controller_manager_node,
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=controller_manager_node,
                on_start=[
                    TimerAction(
                        period=5.0,
                        actions=[joint_state_broadcaster_spawner]
                    )
                ],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=joint_state_broadcaster_spawner,
                on_start=[
                    TimerAction(
                        period=5.0,
                        actions=[joint_trajectory_controller_spawner]
                    )
                ],
            )
        ),
                RegisterEventHandler(
            event_handler=OnProcessStart(
                target_action=joint_trajectory_controller_spawner,
                on_start=[
                    TimerAction(
                        period=5.0,
                        actions=[joint_trajectory_controller_gripper_spawner]
                    )
                ],
            )
        ),
    ]

    return LaunchDescription(nodes_to_start)