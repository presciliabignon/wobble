import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        # S'abonne au flux publié par la Raspberry Pi
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()
        self.get_logger().info('Nœud de vision démarré. En attente d\'images...')

    def image_callback(self, msg):
        try:
            # Traduction du message ROS 2 en image OpenCV (matrice NumPy)
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Traitement OpenCV (niveau de gris)
            processed_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Affichage à l'écran
            cv2.imshow("Flux Brut", cv_image)
            cv2.imshow("Filtre OpenCV", processed_image)
            
            # Pause de 1 ms
            cv2.waitKey(1)
            
        except Exception as e:
            self.get_logger().error(f'Erreur de traitement OpenCV : {e}')

def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()