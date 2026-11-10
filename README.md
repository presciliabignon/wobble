# Wobble

Wobble is a quadruped robot built with ROS 2, a Raspberry Pi 4, a few sensors and 8 servo motors.

> **Status: building...** The core software already works. The mechanical parts are based on the [SpotMicro](https://www.thingiverse.com/thing:3445283) design: some are currently being printed, the others need a few modifications to fit my hardware.

*Picture of the current stage: coming very soon.*

## Project status

| Function | Status |
|---|---|
| Camera on the Pi, images published on the network | Done |
| ArUco marker detection on the PC | Done |
| MPU-6050 IMU reading (acceleration in g, rotation in °/s, calibration) | Done |
| Servo control through the PCA9685 | Centering test done |
| Publishing the IMU data on a ROS topic | To do |
| HC-SR04 ultrasonic sensor | To do |
| 3D-printed mechanical parts | In progress |
| Walking gait | To do |

## Architecture

Everything that has to react quickly (sensors, servos) runs on the Pi, to avoid Wi-Fi latency. Vision, which is more demanding, runs on the PC.

| Package | Machine | Language | Role |
|---|---|---|---|
| `camera_pkg` | Pi | Python | Publishes the camera images |
| `vision_pkg` | PC | Python | Detects ArUco markers and publishes the annotated image |
| `imu_pkg` | Pi | C++ | Reads the MPU-6050 over I2C and converts the values to physical units |
| Others | Pi / PC | C++ | Coming soon (servos, ultrasonic sensor, ...) |

## Hardware

- 1× Raspberry Pi 4 (Ubuntu 24.04, ROS 2 Jazzy) and a PC (ROS 2 Jazzy)
- 1× MPU-6050 IMU
- 1× PCA9685 servo controller
- 8× MG996R servos
- 1× HC-SR04 ultrasonic sensor (coming soon)
- Power: 2S 5200 mAh LiPo battery, charge/discharge module, 5 V 4 A buck converter (for the Pi), D4184 MOSFET module and 6 V 10 A UBEC (for the servos)

The power wiring diagram is in [`docs/schematics/`](docs/schematics/).

## Repository structure

```
wobble/
├── src/
│   ├── pi/        packages that run on the Raspberry Pi (camera_pkg, imu_pkg, servo_pkg)
│   ├── pc/        packages that run on the PC (vision_pkg)
│   └── shared/    code shared by both machines
├── docs/          commands and notes (work in progress)
└── schematics/    wiring diagrams
```

## Quick start

On each machine, from the root of the repository:

```bash
colcon build
source install/setup.bash
```

Then, depending on the machine:

```bash
ros2 run camera_pkg camera        # Pi: publishes the images
ros2 run vision_pkg processor     # PC: detects the ArUco markers
ros2 run imu_pkg imu_node         # Pi: prints the IMU measurements
```

The Pi and the PC must be on the same network. More commands will be listed in [`docs/commands.md`](docs/COMMANDS.md) (work in progress).

## Next steps

1. Publish the IMU data and estimate the tilt
2. Make the servo node listen to commands
3. Connect the ultrasonic sensor (voltage divider on the ECHO pin)
4. Assemble the robot, then write the walking gait

## Credits

The mechanical design is based on [SpotMicro](https://www.thingiverse.com/thing:3445283) by Kim Deok-Yeon (KDY0523). See the original page for the terms of use of the 3D files.

## License

The code is released under the Apache License 2.0 (see [`LICENSE`](LICENSE)). The mechanical parts derived from SpotMicro follow the terms of the original design.
