# Safety Node Documentation

## Overview

The `Safety` class is a ROS2 node written in C++ that provides emergency braking functionality for autonomous vehicles. It subscribes to `LaserScan` data from LIDAR and `Odometry` data to calculate Time To Collision (TTC) and, if necessary, issues an emergency brake command.

## ROS Topics

### Subscribed Topics
1. **`/scan`** (`sensor_msgs/msg/LaserScan`):  
   Provides LIDAR scan data to detect obstacles around the vehicle.
   
2. **`/odom` or `/ego_racecar/odom`** (`nav_msgs/msg/Odometry`):  
   Provides the odometry data for the vehicle. The linear velocity (`twist.twist.linear.x`) is used to determine the vehicle's current speed.

### Published Topics
1. **`/drive`** (`ackermann_msgs/msg/AckermannDriveStamped`):  
   Publishes drive commands. If an obstacle is detected within a critical TTC, the speed is set to 0 to trigger emergency braking.

## Parameters

1. **`ttc`**:  
   Time To Collision (TTC) threshold. When the TTC is below this value, an emergency brake is triggered.
   
2. **`mode`**:  
   Sets the mode to either "sim" (simulation) or "real" for a physical vehicle. In "sim" mode, the node subscribes to `/ego_racecar/odom`, otherwise it subscribes to `/odom`.

## Callbacks

### `drive_callback`
This method is triggered upon receiving odometry data. It updates the current speed of the vehicle based on the x-component of the linear velocity (`twist.twist.linear.x`).

### `scan_callback`
This method is triggered when a new LIDAR scan is received. It calculates the TTC using the LIDAR ranges and compares it to the set threshold. If TTC is below the threshold, an emergency brake message (speed set to 0) is published.

## Methods

### `calculate_TTC`
Calculates the Time To Collision (TTC) for the vehicle based on LIDAR scan data and current speed. It only considers a specific range of angles and ignores readings outside the defined min and max range. If TTC is below the set threshold, the method triggers an emergency brake by publishing a message to the `/drive` topic.

### `radian_to_degree`
Converts an angle in radians to degrees for easier interpretation of LIDAR scan data.

### `calculate_angle`
Calculates the angle of each LIDAR scan point based on its index and the scan's angle increment.

## Usage

To use the `Safety` node, compile and run it in a ROS2 workspace. Make sure to provide the necessary parameters for `ttc` and `mode` either via a launch file or directly on the command line.

Example:
```bash
ros2 run <your_package> <node_name> --ros-args -p ttc:=0.5 -p mode:=sim
