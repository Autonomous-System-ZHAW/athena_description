import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_name = "athena_description"
    urdf_file = "rc-car-complete-fixed-corrected-v2.urdf"

    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        "urdf",
        urdf_file,
    )

    with open(urdf_path, "r") as infp:
        robot_description = infp.read()

    use_sim_time = LaunchConfiguration("use_sim_time")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Isaac Sim/Gazebo) clock if true",
    )

    robot_params = {
        "robot_description": robot_description,
        "use_sim_time": use_sim_time,
    }

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_params],
        output="screen",
    )

    joint_state_publisher = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        output="screen",
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            robot_state_publisher,
            joint_state_publisher,
        ]
    )
