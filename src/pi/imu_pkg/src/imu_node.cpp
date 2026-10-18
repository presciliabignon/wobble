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

    // Filtre passe-bas du capteur pour limiter le bruit
    uint8_t config[2] = {0x1A, 0x03};
    if (write(fd_, config, 2) != 2) {
      RCLCPP_ERROR(this->get_logger(), "Impossible de régler le filtre");
    }

    calibrate();

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

  void calibrate()
  {
    RCLCPP_INFO(this->get_logger(), "Calibration : ne pas bouger le capteur...");
    usleep(100000);  // on laisse le capteur se stabiliser après le réveil

    double sum_ax = 0, sum_ay = 0, sum_az = 0;
    double sum_gx = 0, sum_gy = 0, sum_gz = 0;
    for (int i = 0; i < 200; i++) {
      sum_ax += read_word(0x3B);
      sum_ay += read_word(0x3D);
      sum_az += read_word(0x3F);
      sum_gx += read_word(0x43);
      sum_gy += read_word(0x45);
      sum_gz += read_word(0x47);
      usleep(5000);  // 5 ms entre deux mesures
    }

    ax_off_ = sum_ax / 200;
    ay_off_ = sum_ay / 200;
    az_off_ = sum_az / 200 - 16384.0;
    gx_off_ = sum_gx / 200;
    gy_off_ = sum_gy / 200;
    gz_off_ = sum_gz / 200;

    RCLCPP_INFO(this->get_logger(), "Calibration terminée");
  }

  void timer_callback()
  {
    double ax = (read_word(0x3B) - ax_off_) / 16384.0;  // en g
    double ay = (read_word(0x3D) - ay_off_) / 16384.0;
    double az = (read_word(0x3F) - az_off_) / 16384.0;
    double gx = (read_word(0x43) - gx_off_) / 131.0;    // en degrés par seconde
    double gy = (read_word(0x45) - gy_off_) / 131.0;
    double gz = (read_word(0x47) - gz_off_) / 131.0;

    RCLCPP_INFO(
      this->get_logger(), "acc [g]: %6.2f %6.2f %6.2f | gyro [°/s]: %7.2f %7.2f %7.2f",
      ax, ay, az, gx, gy, gz);
  }

  int fd_ = -1;
  rclcpp::TimerBase::SharedPtr timer_;

  // Décalages mesurés à l'arrêt, dans l'unité brute du capteur
  double ax_off_ = 0.0;
  double ay_off_ = 0.0;
  double az_off_ = 0.0;
  double gx_off_ = 0.0;
  double gy_off_ = 0.0;
  double gz_off_ = 0.0;

};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ImuNode>());
  rclcpp::shutdown();
  return 0;
}