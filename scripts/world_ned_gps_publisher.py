#!/usr/bin/env python3
"""Publish a fixed GPS reference for the Puerto Castellon Stonefish world."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, NavSatStatus


class WorldNedGpsPublisher(Node):
    """Publish the world reference position at a low, fixed rate."""

    def __init__(self):
        super().__init__("world_ned_gps_publisher")

        self.declare_parameter("topic", "/world_ned_frame/gps")
        self.declare_parameter("frame_id", "world_enu")
        self.declare_parameter("publish_period", 10.0)
        self.declare_parameter("latitude", 39.96820067602396)
        self.declare_parameter("longitude", 0.019901428203244895)
        self.declare_parameter("altitude", 2.0)

        topic = self.get_parameter("topic").value
        period = self.get_parameter("publish_period").value
        if period <= 0.0:
            raise ValueError("publish_period must be greater than zero")

        self.publisher = self.create_publisher(NavSatFix, topic, 1)
        self.timer = self.create_timer(period, self.publish_fix)
        self.publish_fix()

        self.get_logger().info(
            f"Publishing fixed GPS reference on {topic} every {period:.1f} seconds"
        )

    def publish_fix(self):
        """Build and publish the NavSatFix message for the simulated world."""
        fix = NavSatFix()
        fix.header.stamp = self.get_clock().now().to_msg()
        fix.header.frame_id = self.get_parameter("frame_id").value
        fix.status.status = NavSatStatus.STATUS_FIX
        fix.status.service = NavSatStatus.SERVICE_GPS
        fix.latitude = self.get_parameter("latitude").value
        fix.longitude = self.get_parameter("longitude").value
        fix.altitude = self.get_parameter("altitude").value
        fix.position_covariance = [0.25, 0.0, 0.0,
                                   0.0, 0.25, 0.0,
                                   0.0, 0.0, 1.0]
        fix.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

        self.publisher.publish(fix)


def main(args=None):
    rclpy.init(args=args)
    node = WorldNedGpsPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
