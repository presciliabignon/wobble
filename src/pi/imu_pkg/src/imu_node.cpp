#include <chrono>
#include <cstdint>
#include <fcntl.h>
#include <functional>
#include <linux/i2c-dev.h>
#include <memory>
#include <sys/ioctl.h>
#include <unistd.h>

#include "rclcpp/rclcpp.hpp"

class ImuNode : public rclcpp::Node
{
public:
  ImuNode()
  : Node("imu_node")
  {
    // Ouvre le bus I2C et choisit le capteur (adresse 0x68)
    fd_ = open("/dev/i2c-1", O_RDWR);
    if (fd_ < 0) {
      RCLCPP_ERROR(this->get_logger(), "Impossible d'ouvrir /dev/i2c-1");
      return;
    }
    ioctl(fd_, I2C_SLAVE, 0x68);

    // Réveille le capteur : on écrit 0 dans le registre 0x6B
    uint8_t wake[2] = {0x6B, 0x00};
    if (write(fd_, wake, 2) != 2) {
      RCLCPP_ERROR(this->get_logger(), "Impossible de réveiller le capteur");
    }

    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      std::bind(&ImuNode::timer_callback, this));
  }

private:
  // Lit une mesure de 16 bits à partir du registre "reg"
  int16_t read_word(uint8_t reg)
  {
    uint8_t bytes[2] = {0, 0};
    if (write(fd_, &reg, 1) != 1 || read(fd_, bytes, 2) != 2) {
      RCLCPP_WARN(this->get_logger(), "Échec de lecture du capteur");
    }
    return static_cast<int16_t>((bytes[0] << 8) | bytes[1]);
  }

  void timer_callback()
  {
    int16_t ax = read_word(0x3B);
    int16_t ay = read_word(0x3D);
    int16_t az = read_word(0x3F);
    int16_t gx = read_word(0x43);
    int16_t gy = read_word(0x45);
    int16_t gz = read_word(0x47);

    RCLCPP_INFO(
      this->get_logger(), "acc: %6d %6d %6d | gyro: %6d %6d %6d",
      ax, ay, az, gx, gy, gz);
  }

  int fd_ = -1;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ImuNode>());
  rclcpp::shutdown();
  return 0;
}