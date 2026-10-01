import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        
        # Initialisation du pont de traduction OpenCV <-> ROS
        self.br = CvBridge()
        
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            self.get_logger().error("Impossible de communiquer avec la webcam.")
            
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        # Capture de la trame vidéo
        ret, frame = self.cap.read()
        
        if ret:
            msg = self.br.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(msg)
            self.get_logger().info('Image publiée sur le réseau DDS')
        else:
            self.get_logger().warning('Échec de lecture matérielle')

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()