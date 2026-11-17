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

        # Marker dictionary
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

        self.get_logger().info('Nœud ArUco prêt')

    def image_callback(self, msg):
        frame = self.br.imgmsg_to_cv2(msg, 'bgr8').copy()

        # Detection is performed in grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = cv2.aruco.detectMarkers(gray, self.dictionary)

        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for i in range(len(ids)):
                # Marker center = average of the 4 corners
                center = corners[i][0].mean(axis=0)
                self.get_logger().info(
                    f'Marqueur {ids[i][0]} : x={center[0]:.0f}, y={center[1]:.0f}')

        # The image is republished (with drawn frames if markers are detected)
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
