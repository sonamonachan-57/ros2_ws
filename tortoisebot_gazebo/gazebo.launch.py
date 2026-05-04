from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    desc_pkg = get_package_share_directory("tortoisebot_description")
    urdf_file = os.path.join(desc_pkg, "urdf", "tortoisebot.urdf")

    # world
    gazebo_world = os.path.join(
        get_package_share_directory("tortoisebot_gazebo"),
        "worlds",
        "empty_world.sdf"
    )

    with open(urdf_file) as file:
        robot_description = file.read()

    return LaunchDescription([

        # Start Gazebo 
        ExecuteProcess(
            cmd=["gz", "sim", "-r", gazebo_world],
            output="screen"
        ),

        # Robot State Publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen"
        ),

        # Spawn robot
        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-name", "tortoisebot",
                "-topic", "/robot_description",
                "-z", "0.5"
            ],
            output="screen"
        ),

        # Bridge for cmd_vel
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=[
                "/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist"
            ],
            output="screen"
        ),

        
       # scan
       Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            # GZ lidar topic → ROS LaserScan
            "/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan"
        ],
        output="screen"
    ),
   

 Node(
     package='tortoisebot_gazebo',
     executable='closest_object.py',
     name='closest_object_node',
     output='screen'
 ),
Node(
    package='tortoisebot_gazebo',
    executable='ball_follower.py',
    name='ball_follower',
    output='screen'
)
    ])
