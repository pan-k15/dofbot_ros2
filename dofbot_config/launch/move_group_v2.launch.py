from moveit_configs_utils import MoveItConfigsBuilder
from launch_ros.actions import Node
from launch import LaunchDescription


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder(
        "yahboom_dofbot",
        package_name="dofbot_config"
    ).to_moveit_configs()

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),

            # ⭐ IMPORTANT: enable MTC execution
            {
                "capabilities": "move_group/ExecuteTaskSolutionCapability"
            },

            {"trajectory_execution.allowed_execution_duration_scaling": 2.0},
            {"publish_robot_description_semantic": True},
            {"use_sim_time": False},
        ],
    )

    return LaunchDescription([
        move_group_node
    ])