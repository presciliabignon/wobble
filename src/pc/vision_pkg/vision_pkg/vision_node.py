import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.image_callback, 10)
        self.publisher_ = self.create_publisher(Image, 'vision/aruco_tracker', 10)
        self.br = CvBridge()

        # Dictionnaire des marqueurs ArUco (grille 4x4, 50 marqueurs)
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

        self.get_logger().info('Nœud ArUco prêt')

    def image_callback(self, msg):
        # Message ROS -> image OpenCV (.copy() pour pouvoir dessiner dessus)
        frame = self.br.imgmsg_to_cv2(msg, 'bgr8').copy()

        # La détection se fait en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, self.dictionary)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for i in range(len(ids)):
                # Centre du marqueur = moyenne des 4 coins
                center = corners[i][0].mean(axis=0)
                self.get_logger().info(
                    f'Marqueur {ids[i][0]} : x={center[0]:.0f}, y={center[1]:.0f}')

        # On republie l'image (avec les cadres dessinés s'il y a des marqueurs)
        out = self.br.cv2_to_imgmsg(frame, encoding='bgr8')
        out.header = msg.header
        self.publisher_.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
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