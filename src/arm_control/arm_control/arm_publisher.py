import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Quaternion

PUBLISH_PERIOD = 0.1


class ArmPublisher(Node):

    def __init__(self):
        super().__init__('arm_publisher')

        self.arm_pub = self.create_publisher(
            Quaternion,
            'quaternion',
            10
        )

        self.timer = self.create_timer(
            PUBLISH_PERIOD,
            self.publish_quaternion
        )

    def publish_quaternion(self):
        msg = Quaternion()

        # Nilai quaternion
        msg.x = 0.1
        msg.y = 0.2
        msg.z = 0.3
        msg.w = 1.0

        self.arm_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    arm_publisher = ArmPublisher()

    try:
        rclpy.spin(arm_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        arm_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()