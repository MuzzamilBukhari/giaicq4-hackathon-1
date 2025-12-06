import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from std_msgs.msg import String

class QoSSubscriber(Node):

    def __init__(self):
        super().__init__('qos_subscriber')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.subscription = self.create_subscription(
            String,
            'qos_topic',
            self.listener_callback,
            qos_profile)
        self.get_logger().info('Subscriber created with QoS profile')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    qos_subscriber = QoSSubscriber()
    rclpy.spin(qos_subscriber)
    qos_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()