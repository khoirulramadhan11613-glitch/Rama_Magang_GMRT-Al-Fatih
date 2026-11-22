import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Quaternion
import math


class ArmSubscriber(Node):

    def __init__(self):
        super().__init__('arm_subscriber')

        self.subscription = self.create_subscription(
            Quaternion,
            'quaternion',
            self.quaternion_callback,
            10
        )

    def quaternion_callback(self, msg):

        x = msg.x
        y = msg.y
        z = msg.z
        w = msg.w

        # Quaternion ke Roll
        roll = math.atan2(
            2 * (w * x + y * z),
            1 - 2 * (x * x + y * y)
        )

        # Quaternion ke Pitch
        sin_pitch = 2 * (w * y - z * x)
        sin_pitch = max(-1, min(1, sin_pitch))
        pitch = math.asin(sin_pitch)

        # Quaternion ke Yaw
        yaw = math.atan2(
            2 * (w * z + x * y),
            1 - 2 * (y * y + z * z)
        )

        # Radian ke derajat
        roll = math.degrees(roll)
        pitch = math.degrees(pitch)
        yaw = math.degrees(yaw)

        self.get_logger().info(
            f'Roll: {roll:.2f}°, '
            f'Pitch: {pitch:.2f}°, '
            f'Yaw: {yaw:.2f}°'
        )


def main(args=None):
    rclpy.init(args=args)

    arm_subscriber = ArmSubscriber()

    try:
        rclpy.spin(arm_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        arm_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()