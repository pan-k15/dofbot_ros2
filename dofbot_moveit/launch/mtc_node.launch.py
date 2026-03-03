from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder("yahboom_dofbot", package_name="dofbot_config")
        .to_moveit_configs()
    )

    pick_place_demo = Node(
        package="dofbot_moveit",
        executable="mtc_node",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
        ],
    )

    return LaunchDescription([pick_place_demo])