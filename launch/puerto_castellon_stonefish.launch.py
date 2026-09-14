from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='blueboat',
        description='Name of the robot'
    )
    
    xacro_file = PathJoinSubstitution([
        FindPackageShare('puerto_castellon_stonefish'),
        "urdf",
        "blueboat.xacro"
    ])
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        parameters=[{
            "robot_description": Command(["xacro ", xacro_file]),
            'use_sim_time':True
        }]
    )

    stonefish_simulator = IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare('stonefish_ros2'), 'launch', 'stonefish_simulator.launch.py'
        ]),
        launch_arguments={
            'simulation_data': PathJoinSubstitution([
                FindPackageShare('puerto_castellon_stonefish'), 'data'
            ]),
            'scenario_desc': PathJoinSubstitution([
                FindPackageShare('puerto_castellon_stonefish'), 'scenarios', 'puerto_castellon_stonefish.scn'
            ]),
            'simulation_rate': '100.0',
            'window_res_x': '1200',
            'window_res_y': '800',
            'rendering_quality': 'high'
        }.items()
    )

    return LaunchDescription([
        robot_name_arg,
        robot_state_publisher_node,
        stonefish_simulator,
    ])
