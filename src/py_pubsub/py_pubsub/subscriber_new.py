import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Quaternion

DEAD_ZONE_DEG = 10.0    # di bawah ini dianggap "tidak ada perintah"
YAW_TURN_DEG = 15.0     # |yaw| di atas ini -> robot putar badan
TILT_STOP_DEG = 60.0    # |roll| / |pitch| di atas ini -> berhenti (aman)
LINEAR_SPEED = 0.2      # m/s (hanya untuk ditampilkan di log)
ANGULAR_SPEED = 0.5     # rad/s (hanya untuk ditampilkan di log)


def validate_quaternion(x, y, z, w):
    """Kembalikan pesan error (str) kalau tidak valid, atau None kalau valid."""
    values = (x, y, z, w)
    if not all(math.isfinite(v) for v in values):
        return 'ada nilai NaN/inf'
    if any(abs(v) > 1.0 for v in values):
        return 'ada komponen di luar rentang -1..1'
    if math.sqrt(sum(v * v for v in values)) < 1e-6:
        return 'norma quaternion nol (tidak bisa dinormalisasi)'
    return None


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


def decide_robot_action(roll, pitch, yaw):
    """Tentukan respon robot dari roll/pitch/yaw (derajat).

    Urutan prioritas:
      1. Keselamatan : |roll| atau |pitch| > TILT_STOP_DEG -> DIAM (berhenti)
      2. Putar badan : |yaw| > YAW_TURN_DEG -> putar kiri/kanan dulu
                       (robot harus menghadap arah yang benar sebelum jalan)
      3. Gerak lurus : |pitch| > DEAD_ZONE_DEG -> maju (+) / mundur (-)
      4. Selain itu  : DIAM

    Return: (aksi, penjelasan, linear_x m/s, angular_z rad/s)
    """
    if abs(roll) > TILT_STOP_DEG or abs(pitch) > TILT_STOP_DEG:
        return ('DIAM (BERHENTI AMAN)',
                f'kemiringan ekstrem (roll={roll:.1f}, pitch={pitch:.1f}), '
                'risiko terguling',
                0.0, 0.0)

    if abs(yaw) > YAW_TURN_DEG:
        if yaw > 0:
            return ('PUTAR BADAN KIRI',
                    f'yaw {yaw:+.1f} deg > {YAW_TURN_DEG} deg (CCW)',
                    0.0, +ANGULAR_SPEED)
        return ('PUTAR BADAN KANAN',
                f'yaw {yaw:+.1f} deg < -{YAW_TURN_DEG} deg (CW)',
                0.0, -ANGULAR_SPEED)

    if pitch > DEAD_ZONE_DEG:
        return ('JALAN MAJU',
                f'pitch {pitch:+.1f} deg > {DEAD_ZONE_DEG} deg (condong depan)',
                +LINEAR_SPEED, 0.0)
    if pitch < -DEAD_ZONE_DEG:
        return ('JALAN MUNDUR',
                f'pitch {pitch:+.1f} deg < -{DEAD_ZONE_DEG} deg (condong belakang)',
                -LINEAR_SPEED, 0.0)

    return ('DIAM',
            'semua sudut berada di dead zone',
            0.0, 0.0)


class QuaternionSubscriber(Node):

    def __init__(self):
        super().__init__('quaternion_subscriber')
        self.subscription = self.create_subscription(
            Quaternion,
            'quaternion_topic',
            self.listener_callback,
            10)
        self._warned_not_unit = False

    def listener_callback(self, msg):
        self.get_logger().info(
            f'Received: x={msg.x}, y={msg.y}, z={msg.z}, w={msg.w}'
        )

        error = validate_quaternion(msg.x, msg.y, msg.z, msg.w)
        if error is not None:
            self.get_logger().error(f'Quaternion ditolak: {error}')
            return

        norm = math.sqrt(msg.x ** 2 + msg.y ** 2 + msg.z ** 2 + msg.w ** 2)
        if abs(norm - 1.0) > 0.01 and not self._warned_not_unit:
            self.get_logger().warn(
                f'Quaternion bukan unit (norma={norm:.3f}); '
                'dinormalisasi otomatis sebelum dihitung.'
            )
            self._warned_not_unit = True

        roll, pitch, yaw = quaternion_to_euler(msg.x, msg.y, msg.z, msg.w)
        self.get_logger().info(
            f'Roll={roll:.2f} deg, Pitch={pitch:.2f} deg, Yaw={yaw:.2f} deg'
        )

        action, reason, lin, ang = decide_robot_action(roll, pitch, yaw)
        self.get_logger().info(
            f'Respon robot: {action} | {reason} | '
            f'linear.x={lin:+.2f} m/s, angular.z={ang:+.2f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)

    node = QuaternionSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()