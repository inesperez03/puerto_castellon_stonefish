# puerto_castellon_stonefish — CIRTESU BlueBoat Stonefish Simulation (ROS 2)

This repository contains a specialized **Stonefish** simulation suite developed at **CIRTESU (Castellón, Spain)**.  
It provides assets, scenarios, and ROS 2 launch/configuration to simulate the **BlueBoat** USV in detailed environments replicating CIRTESU facilities.

## Overview

- **High-fidelity maritime simulation** using Stonefish.
- **CIRTESU scenarios** with multiple environment models (including a fully detailed, “complete” CIRTESU model).
- **BlueBoat integration**: robot model + sensors + ROS 2 interfaces ready to use.
- Intended for research on navigation, control, localization, autonomy, and perception.

## Notes on Stonefish modifications

This project is developed against a **modified Stonefish** version that includes support for a **terrestrial (2D) LiDAR** sensor.  
A public upstream release is planned, but it may not be available in the official repositories yet.

## Repository contents

Typical components you will find in this repo:

- **Scenarios / worlds** replicating CIRTESU facilities (multiple variants / detail levels).
- **Meshes / textures** for CIRTESU environments and visualization assets.
- **BlueBoat robot description**:
  - Publishes `/robot_description` using **xacro** (URDF pipeline).
  - Includes relevant links/frames (e.g., `blueboat/base_link`, `blueboat/lidar_front`, `blueboat_camera_link`, `gps_frame`, etc.).
- **Sensor setup** (depending on the scenario/launch):
  - LiDAR point cloud topic (e.g., `/blueboat/lidar_points`)
  - Camera image topic (e.g., `/blueboat/camera/image_raw/image_color`)
- **RViz configuration** (see the `rviz/` folder):
  - Pre-configured to visualize the BlueBoat model, TF tree, LiDAR point cloud, markers, and camera image.

## RViz (ready-to-use visualization)

The provided RViz config is set up to display, out of the box:

- **RobotModel** from `/robot_description` (BlueBoat URDF/xacro)
- **PointCloud2** from `/blueboat/lidar_points`
- **MarkerArray** (e.g., `/blueboat/aruco_map_markers` when used with localization packages)
- **Image** from `/blueboat/camera/image_raw/image_color`
- **TF** frames commonly used in the stack (`world_ned`, `cirtesu_base_link`, `blueboat/base_link`, sensors frames, etc.)

A typical fixed frame for visualization is `world_ned`.

## Odometry and TF bridge (`odom2tf`)

Stonefish provides odometry through its simulator sensor configuration (the Stonefish `<odometry>` sensor).  
In ROS 2, this is typically exposed as a `nav_msgs/Odometry` topic (e.g., `/blueboat/navigator/odometry`).

Many ROS tools and downstream stacks (RViz, localization, navigation) expect **TF transforms**, not only Odometry messages.
For that reason, this repo currently includes an **`odom2tf`** node that:

- **Subscribes** to Stonefish odometry (`nav_msgs/Odometry`)
- **Broadcasts** the corresponding TF transform (e.g., `world_ned -> blueboat/base_link`)
- Ensures the robot pose is available in the TF tree even if Stonefish only publishes odometry as a message

> Important: `odom2tf` does not fuse sensors or estimate state; it simply converts the simulator odometry into TF so the rest of the ROS graph can consume it consistently.

## Prerequisites

Dependencies required in your ROS 2 environment:

- **Stonefish (simulator core)**  
  https://github.com/patrykcieslak/stonefish.git

- **stonefish_ros2 (ROS 2 integration)**  
  https://github.com/patrykcieslak/stonefish_ros2.git

## Installation

```bash
mkdir -p ~/your_ws/src
cd ~/your_ws/src

# Dependencies
git clone https://github.com/patrykcieslak/stonefish.git
git clone https://github.com/patrykcieslak/stonefish_ros2.git

# This package
git clone https://github.com/Mariolopez31/puerto_castellon_stonefish.git

cd ~/your_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install
source install/setup.bash
