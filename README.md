# ROS 2 Autonomous Telemetry & Diagnostics Monitor
**A mechatronics health-monitoring bridge between physical simulation (Gazebo) and visual observability (Foxglove Studio).**

*(Insert your screen recording here showing the robot moving and the gauges reacting)*

## Executive Summary
In autonomous robotics, building the agent is only half the engineering challenge; maintaining operational observability is the other. This project simulates a mobile autonomous agent and calculates real-time hardware diagnostics (motor thermal load and battery discharge) based on physical kinematic states.

The system acts as a "diagnostic node," subscribing to raw physical odometry and publishing calculated hardware health metrics to an industrial-grade telemetry dashboard.
<img width="1920" height="981" alt="image" src="https://github.com/user-attachments/assets/c858eb28-34f9-483e-a185-efdc727f011b" />


## System Architecture
1. **The Physical Layer (Gazebo Classic):** Simulates the kinematics and environmental interactions of a Differential Drive robot (TurtleBot3).
2. **The Middleware (ROS 2 Humble):** Acts as the communication bus, piping raw `/odom` and `/imu` data at 10Hz.
3. **The Mechatronic Logic Node (Python):** A custom node that translates physical velocity into hardware strain. 
   - *Thermal Load:* Modeled proportionally to the square of the motor speed ($P = I^2 R$).
   - *Power Draw:* Calculates continuous base-electronics drain + active kinetic load drain.
4. **The Observability Layer (Foxglove Studio):** A WebSocket bridge streams the custom `/health/motor_temp` and `/health/battery_level` topics to a live, web-based control dashboard.

## Installation & Replication
**1. Source your ROS 2 environment:**
```bash
source /opt/ros/humble/setup.bash
```
**2. Launch the Simulation (Terminal 1):**
```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
```
**3. Run the Diagnostic Node (Terminal 2):**
```bash
cd ~/telemetry_ws
colcon build
source install/setup.bash
ros2 run robot_health_monitor diagnostic_node
```
**4. Start the Telemetry Bridge (Terminal 3):**
```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml
