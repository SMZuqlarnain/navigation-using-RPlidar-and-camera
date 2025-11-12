#!/bin/bash
set -e

echo "=========================================="
echo "🚀 ROS 2 Jazzy + RPLiDAR Installation Script"
echo "=========================================="

# ----- System Preparation -----
echo "🔄 Updating system..."
sudo apt update -y
sudo apt install -y curl gnupg lsb-release git build-essential

# ----- Add ROS 2 Repository -----
echo "🔑 Adding ROS 2 Jazzy repository..."
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update -y

# ----- Install ROS 2 Desktop -----
echo "📦 Installing ROS 2 Jazzy Desktop..."
sudo apt install -y ros-jazzy-desktop

# ----- Source ROS Environment -----
echo "⚙️ Setting up ROS 2 environment..."
source /opt/ros/jazzy/setup.bash
if ! grep -Fxq "source /opt/ros/jazzy/setup.bash" ~/.bashrc; then
  echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
fi

# ----- Create Workspace -----
echo "📁 Creating ROS 2 workspace..."
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# ----- Clone RPLiDAR ROS 2 package -----
echo "🔽 Cloning RPLiDAR ROS 2 package..."
git clone https://github.com/Slamtec/rplidar_ros.git

# ----- Build the package -----
cd ~/ros2_ws
echo "🧱 Building workspace..."
source /opt/ros/jazzy/setup.bash
sudo apt install -y python3-colcon-common-extensions
colcon build --symlink-install

# ----- Source workspace automatically -----
if ! grep -Fxq "source ~/ros2_ws/install/setup.bash" ~/.bashrc; then
  echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
fi

# ----- Permissions for LIDAR -----
echo "🔐 Setting USB permissions..."
sudo usermod -a -G dialout $USER
echo "✅ You may need to log out and back in for permissions to take effect."

# ----- Install RViz2 -----
echo "🧭 Installing RViz2..."
sudo apt install -y ros-jazzy-rviz2

echo "=========================================="
echo "🎉 Installation Complete!"
echo "✅ ROS 2 Jazzy + RPLiDAR ready to use!"
echo "👉 Next steps:"
echo "  1. Plug in your RPLiDAR (check with: ls /dev/ttyUSB*)"
echo "  2. Run:"
echo "       ros2 launch rplidar_ros rplidar_a1_launch.py"
echo "  3. Visualize in RViz2:"
echo "       ros2 run rviz2 rviz2"
echo "=========================================="
