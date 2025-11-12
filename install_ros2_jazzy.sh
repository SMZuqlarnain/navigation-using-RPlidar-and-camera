#!/bin/bash
set -e

echo "🔄 Updating system packages..."
sudo apt update -y

echo "📦 Installing dependencies..."
sudo apt install -y curl gnupg lsb-release

echo "🔑 Adding ROS 2 GPG key..."
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "🧩 Adding ROS 2 Jazzy repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

echo "🔁 Updating APT sources..."
sudo apt update -y

echo "🚀 Installing ROS 2 Jazzy Desktop..."
sudo apt install -y ros-jazzy-desktop

echo "⚙️ Sourcing ROS 2 environment..."
source /opt/ros/jazzy/setup.bash

if ! grep -Fxq "source /opt/ros/jazzy/setup.bash" ~/.bashrc
then
  echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
  echo "✅ Added ROS 2 source line to ~/.bashrc"
else
  echo "ℹ️ ROS 2 source line already exists in ~/.bashrc"
fi

echo "🎉 ROS 2 Jazzy installation complete!"
echo "👉 Run: source ~/.bashrc"
echo "👉 Test with: ros2 run demo_nodes_cpp talker"
