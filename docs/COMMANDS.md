# Wobble

## 1. Communication ROS 2

### Raspberry Pi

```bash
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### PC

```bash
echo "export ROS_DOMAIN_ID=42" >> ~/.bashrc
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Test de communication

Sur la Raspberry Pi :

```bash
ros2 multicast send
```

Sur le PC :

```bash
ros2 multicast receive
```

## 2. Dépendances

### Raspberry Pi

```bash
sudo apt install ros-jazzy-cv-bridge python3-opencv -y
```

### PC

```bash
sudo apt install ros-jazzy-cv-bridge python3-opencv -y
```

## 3. Caméra

### Raspberry Pi

```bash
sudo usermod -aG video <username>
newgrp video
sudo reboot
```

```bash
cd ~/wobble
colcon build --packages-select camera_pkg --symlink-install
echo "source ~/wobble/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### PC

```bash
ros2 run rqt_image_view rqt_image_view
```

## 4. Vision

### PC

```bash
cd ~/Documents/Project/wobble_pc
colcon build --packages-up-to vision_pkg --symlink-install
echo "source ~/Documents/Project/wobble_pc/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

```bash
ros2 run vision_pkg processor
```

## 5. Développement (non nécessaire pour l'utilisation)

### Raspberry Pi

```bash
ros2 pkg create --build-type ament_python camera_pkg --dependencies rclpy sensor_msgs cv_bridge
```

### PC

```bash
ros2 pkg create --build-type ament_python vision_pkg --dependencies rclpy sensor_msgs cv_bridge
```