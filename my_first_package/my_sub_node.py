import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

class BrainNode(Node):
    def __init__(self):
        super().__init__('brain_node')
        
        # بتسمع للمسافة اللي جاية من الكوبري
        self.subscription = self.create_subscription(Float32, '/sonar_distance', self.distance_callback, 10)
        
        # بتبعت القرار (أمر الحركة) للكوبري
        self.publisher_ = self.create_publisher(String, '/motor_cmd', 10)
        self.get_logger().info("Brain Node Started. Waiting for distance data...")

    def distance_callback(self, msg):
        distance = msg.data
        cmd_msg = String()
        
        # الشرط بتاعك: 15 سم
        if distance <= 15.0:
            cmd_msg.data = 'S'
            self.publisher_.publish(cmd_msg)
            self.get_logger().warn(f'Obstacle! Distance: {distance:.1f} cm -> STOP (S)')
        else:
            cmd_msg.data = 'F'
            self.publisher_.publish(cmd_msg)
            self.get_logger().info(f'Safe. Distance: {distance:.1f} cm -> FORWARD (F)')

def main(args=None):
    rclpy.init(args=args)
    node = BrainNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
