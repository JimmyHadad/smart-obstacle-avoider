import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
import serial

class SerialBridgeNode(Node):
    def __init__(self):
        super().__init__('serial_bridge_node')
        
        # ربط السيريال بالبورت الصحيح
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
            self.get_logger().info("Serial port connected successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to Serial: {e}")
            
        # ناشر (Publisher) لطباعة المسافة
        self.distance_pub = self.create_publisher(Float32, '/sonar_distance', 10)
        
        # مستقبل (Subscriber) لاستقبال أوامر الحركة من المخ
        self.cmd_sub = self.create_subscription(String, '/motor_cmd', self.cmd_callback, 10)
        
        # تايمر سريع جداً (كل 0.05 ثانية) عشان الاستجابة اللحظية
        self.timer = self.create_timer(0.05, self.read_serial)
        self.get_logger().info("Bridge Node Started. Waiting for ESP32 data...")

    def read_serial(self):
        if hasattr(self, 'ser') and self.ser.in_waiting > 0:
            try:
                line = ""
                # اللوب دي بتفضي الطابور كله وتاخد أحدث قراءة لحظية فقط
                while self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                
                if line:
                    distance = float(line)
                    msg = Float32()
                    msg.data = distance
                    self.distance_pub.publish(msg)
            except ValueError:
                pass # تجاهل أي قراءات غير مفهومة في البداية

    def cmd_callback(self, msg):
        # استقبال الأمر (F أو S) وإرساله للـ ESP32
        if hasattr(self, 'ser'):
            command = msg.data
            self.ser.write(command.encode('utf-8'))

def main(args=None):
    rclpy.init(args=args)
    node = SerialBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'ser'):
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
