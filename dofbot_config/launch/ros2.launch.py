from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():

    robot_description_content = Command(
        [
            "xacro ",
            PathJoinSubstitution([
                FindPackageShare("dofbot_moveit"),
                "urdf",
                "dofbot.urdf"
            ]),
            " use_fake_hardware:=true"
        ]
    )

    robot_description = {
        "robot_description": robot_description_content
    }

    controllers_file = PathJoinSubstitution(
        [
            FindPackageShare("dofbot_config"),
            "config",
            "ros2_controllers.yaml",
        ]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controllers_file],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    dofbot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["dofbot_controller"],
    )

    return LaunchDescription(
        [
            control_node,
            joint_state_broadcaster_spawner,
            dofbot_controller_spawner,
        ]
    )