#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import math

class HealthMonitorNode(Node):
    def __init__(self):
        super().__init__('diagnostic_node')
        
        # Subscribe to physical movement data
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        # Publish virtual health telemetry
        self.temp_pub = self.create_publisher(Float32, '/health/motor_temp', 10)
        self.batt_pub = self.create_publisher(Float32, '/health/battery_level', 10)
        
        # Initial Mechatronic States
        self.motor_temp = 25.0  # Starts at room temperature (Celsius)
        self.battery_level = 100.0  # Starts fully charged
        
        # Timer to publish telemetry at 2Hz (every 0.5 seconds)
        self.timer = self.create_timer(0.5, self.publish_health)

    def odom_callback(self, msg):
        # Extract linear and angular velocity
        linear_vel = msg.twist.twist.linear.x
        angular_vel = msg.twist.twist.angular.z
        
        # Calculate total absolute speed
        total_speed = math.sqrt(linear_vel**2 + angular_vel**2)
        
        # MECHATRONICS MODELING: 
        # 1. Thermal Load: Motors heat up proportionally to the square of their speed (Power = I^2 * R)
        thermal_increase = (total_speed ** 2) * 2.5
        cooling_rate = 0.5  # Ambient cooling
        
        self.motor_temp += thermal_increase - cooling_rate
        
        # Clamp temperature to a realistic floor
        if self.motor_temp < 25.0:
            self.motor_temp = 25.0
            
        # 2. Battery Drain: Base drain for electronics + active drain for motor movement
        base_drain = 0.01
        active_drain = total_speed * 0.05
        self.battery_level -= (base_drain + active_drain)

    def publish_health(self):
        # Create and publish the messages
        temp_msg = Float32()
        temp_msg.data = self.motor_temp
        self.temp_pub.publish(temp_msg)
        
        batt_msg = Float32()
        batt_msg.data = self.battery_level
        self.batt_pub.publish(batt_msg)
        
        self.get_logger().info(f'Telemetry -> Temp: {self.motor_temp:.1f}°C | Battery: {self.battery_level:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = HealthMonitorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
