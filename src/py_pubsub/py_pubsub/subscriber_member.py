import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Quaternion


def quaternion_to_euler(x, y, z, w):
    
    norm = math.sqrt(x * x + y * y + z * z + w * w)
    x, y, z, w = x / norm, y / norm, z / norm, w / norm

    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

   
    sinp = 2.0 * (w * y - z * x)
    sinp = max(-1.0, min(1.0, sinp))  
    pitch = math.asin(sinp)

    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


class QuaternionSubscriber(Node):

    def __init__(self):
        super().__init__('quaternion_subscriber')
        
        self.subscription = self.create_subscription(
            Quaternion,
            'quaternion_topic',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        roll, pitch, yaw = quaternion_to_euler(msg.x, msg.y, msg.z, msg.w)
        self.get_logger().info(
            f'Received: x={msg.x}, y={msg.y}, z={msg.z}, w={msg.w}'
        )
        self.get_logger().info(
            f'Roll={roll:.2f} deg, Pitch={pitch:.2f} deg, Yaw={yaw:.2f} deg'
        )


def main(args=None):
    rclpy.init(args=args)

    node = QuaternionSubscriber()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()