## étape 1 : Comm + Test ##

echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc (PI + PC)

echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc (PI + PC)

source ~/.bashrc -> actualiser PI + PC

ros2 multicast receive -> PC
ros2 multicast send -> PI

-----------------------------------------------------

sudo apt install ros-jazzy-cv-bridge python3-opencv -y

----------------------------------------------------

sudo usermod -aG video <username>

newgrp video 

sudo reboot

source install/setup.bash

source ~/wobble/install/setup.bash (dans fichier bashrc)

colcon build --packages-select camera_pkg --symlink-install

-----------------------------------------------------

## étape 2 : caméra ##

ros2 pkg create --build-type ament_python camera_pkg --dependencies rclpy sensor_msgs cv_bridge --création package


ros2 run rqt_image_view rqt_image_view -- visualiseur sur PC