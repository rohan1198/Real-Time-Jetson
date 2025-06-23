# Jetson Orin Nano SLAM Development Setup

A comprehensive guide for setting up a complete SLAM (Simultaneous Localization and Mapping) development environment on the NVIDIA Jetson Orin Nano with Ubuntu 22.04, real-time kernel, CUDA-enabled OpenCV, and ROS2 Humble.

## Table of Contents

- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Software Stack](#software-stack)
- [Initial System Setup](#initial-system-setup)
- [Real-Time Kernel Setup](#real-time-kernel-setup)
- [Performance Optimization](#performance-optimization)
- [Development Environment](#development-environment)
- [OpenCV with CUDA Support](#opencv-with-cuda-support)
- [ROS2 Humble from Source](#ros2-humble-from-source)
- [Verification](#verification)
- [Next Steps](#next-steps)
- [Troubleshooting](#troubleshooting)

## Overview

This setup enables high-performance visual-inertial SLAM development by combining:
- **Real-time Ubuntu kernel** for precise timing control
- **CUDA-enabled OpenCV** for GPU-accelerated computer vision
- **ROS2 Humble** built from source to integrate with custom OpenCV
- **Performance optimizations** for embedded development

## Initial System Setup

### 1. Fresh Install Updates

```bash
sudo apt update && apt list --upgradable
sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo reboot

sudo apt autoremove
sudo apt autoclean
```

### 2. Install Essential Packages

```bash
sudo apt install cmake dconf-editor build-essential tilix vlc ubuntu-restricted-extras \
    python3-dev python3-pip python3-venv python3-numba lm-sensors cheese neofetch \
    htop nvtop chrome-gnome-shell gnome-tweaks git stress-ng nano curl gedit wget -y

sudo pip3 install jetson-utils
sudo apt install rt-tests
sudo reboot
```

## Real-Time Kernel Setup

### 1. Enable Ubuntu Pro (Required for RT Kernel)

```bash
sudo apt install apt-utils ubuntu-advantage-tools
sudo mkdir -p /boot/grub
sudo dpkg --configure -a

# Attach your Ubuntu Pro subscription
sudo pro attach

# Enable and install real-time kernel
sudo pro enable realtime-kernel
sudo apt install ubuntu-realtime
sudo reboot
```

### 2. Verify RT Kernel

```bash
uname -r
# Should show something like: 
# Linux ubuntu 5.15.148-tegra #1 SMP PREEMPT Tue Jan 7 17:14:38 PST 2025 aarch64 aarch64 aarch64 GNU/Linux
```

## Performance Optimization

### 1. CPU Performance Governor

Create a systemd service for maximum CPU performance:

```bash
sudo nano /etc/systemd/system/cpu-performance-mode.service
```

Add the following content:

```ini
[Unit]
Description=Set CPU governor to performance mode
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'

[Install]
WantedBy=multi-user.target
```

Enable the service:

```bash
sudo systemctl enable cpu-performance-mode.service
sudo systemctl start cpu-performance-mode.service
sudo systemctl status cpu-performance-mode.service

# Verify all CPUs are in performance mode
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### 2. Increase Swap Space

For building large projects, increase swap to 10GB:

```bash
sudo swapoff -a
sudo dd if=/dev/zero of=/swapfile bs=1G count=10
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
sudo cp /etc/fstab /etc/fstab.backup
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## Development Environment

### 1. Zsh with Oh My Zsh Setup

```bash
sudo apt install zsh -y
sudo chsh -s $(which zsh)

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Install Powerlevel10k theme
git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k

# Download fonts
cd ~/Downloads
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf
cd ~

# Install useful plugins
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```

### 2. GPU Stress Testing Tool

```bash
git clone https://github.com/wilicc/gpu-burn.git
cd gpu-burn
make
cd ~
```

## OpenCV with CUDA Support

### 1. Remove Existing OpenCV

```bash
# Remove any existing OpenCV and ROS installations
sudo apt remove --purge ros-* 
sudo apt autoremove

sudo apt remove --purge "libopencv*" "opencv-*" libgstreamer-opencv1.0-0
sudo apt remove --purge libopencv-core4.5d
sudo apt autoremove
sudo apt autoclean
```

### 2. Install Build Dependencies

```bash
sudo apt update && sudo apt upgrade -y

# Essential build tools
sudo apt install -y \
    build-essential cmake cmake-gui git pkg-config \
    libjpeg-dev libtiff5-dev libpng-dev \
    libavcodec-dev libavformat-dev libswscale-dev libavresample-dev \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    libgtk2.0-dev libgtk-3-dev libcanberra-gtk-module libcanberra-gtk3-module \
    libxvidcore-dev libx264-dev \
    libtbb2 libtbb-dev \
    libdc1394-dev libv4l-dev v4l-utils \
    liblapacke-dev libopenblas-dev libatlas-base-dev \
    libeigen3-dev libtheora-dev libvorbis-dev \
    libxine2-dev libfaac-dev libmp3lame-dev \
    libopencore-amrnb-dev libopencore-amrwb-dev \
    x264 unzip yasm

# Python development
sudo apt install -y python3-dev python3-pip python3-testresources
python3 -m pip install --upgrade pip
python3 -m pip install numpy matplotlib

# Additional libraries for contrib modules
sudo apt install -y \
    libprotobuf-dev protobuf-compiler \
    libgoogle-glog-dev libgflags-dev \
    libgphoto2-dev libeigen3-dev libhdf5-dev \
    libtesseract-dev libleptonica-dev
```

### 3. Download and Build OpenCV

```bash
cd ~
mkdir opencv_build && cd opencv_build

# Download OpenCV 4.10.0 with contrib modules
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.10.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.10.0.zip

unzip opencv.zip
unzip opencv_contrib.zip

# Create build directory
mkdir -p opencv-4.10.0/build
cd opencv-4.10.0/build
```

### 4. Configure Build

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.10.0/modules \
      -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
      -D WITH_OPENCL=OFF \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_BIN=8.7 \
      -D CUDA_ARCH_PTX="" \
      -D WITH_CUDNN=ON \
      -D WITH_CUBLAS=ON \
      -D ENABLE_FAST_MATH=ON \
      -D CUDA_FAST_MATH=ON \
      -D OPENCV_DNN_CUDA=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=OFF \
      -D WITH_OPENGL=ON \
      -D WITH_GSTREAMER=ON \
      -D OPENCV_GENERATE_PKGCONFIG=ON \
      -D OPENCV_PC_FILE_NAME=opencv.pc \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D PYTHON_EXECUTABLE=/usr/bin/python3 \
      -D PYTHON3_EXECUTABLE=/usr/bin/python3 \
      -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
      -D BUILD_opencv_python2=OFF \
      -D BUILD_opencv_python3=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=ON \
      -D BUILD_EXAMPLES=ON \
      ..
```

### 5. Build and Install

```bash
# Build with 4 cores (takes 1.5-2.5 hours)
make -j4

# Install
sudo make install
sudo ldconfig
```

### 6. Verify OpenCV Installation

```bash
python3 -c "
import cv2
print('OpenCV version:', cv2.__version__)
print('CUDA devices:', cv2.cuda.getCudaEnabledDeviceCount())
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print('CUDA support working!')
else:
    print('CUDA not detected')
"
```

## ROS2 Humble from Source

### 1. Add ROS2 Repository

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
```

### 2. Install ROS2 Build Dependencies

```bash
sudo apt install -y \
    python3-flake8-docstrings \
    python3-pip \
    python3-pytest-cov \
    ros-dev-tools \
    python3-flake8-blind-except \
    python3-flake8-builtins \
    python3-flake8-class-newline \
    python3-flake8-comprehensions \
    python3-flake8-deprecated \
    python3-flake8-import-order \
    python3-flake8-quotes \
    python3-pytest-repeat \
    python3-pytest-rerunfailures

sudo apt install -y \
    libasio-dev \
    libtinyxml2-dev \
    libcunit1-dev
```

### 3. Create ROS2 Workspace

```bash
mkdir -p ~/ros2_humble/src
cd ~/ros2_humble

# Download ROS2 Humble source
vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src
```

### 4. Configure Environment for Custom OpenCV

```bash
# Set OpenCV environment variables
export OpenCV_DIR=/usr/local/lib/cmake/opencv4
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Make permanent (adjust for your shell)
echo 'export OpenCV_DIR=/usr/local/lib/cmake/opencv4' >> ~/.zshrc
echo 'export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH' >> ~/.zshrc
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc
```

### 5. Install Dependencies

```bash
# Initialize rosdep
sudo rosdep init
rosdep update

# Install ROS2 dependencies
rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"
```

### 6. Build ROS2

```bash
cd ~/ros2_humble/

# Build with custom OpenCV (takes 2-3 hours)
colcon build --symlink-install --cmake-args -DOpenCV_DIR=/usr/local/lib/cmake/opencv4
```

**Note:** You'll see warnings about unused OpenCV_DIR variables for packages that don't use OpenCV. This is normal and expected.

### 7. Setup ROS2 Environment

```bash
# Add to shell configuration
echo 'source ~/ros2_humble/install/setup.zsh' >> ~/.zshrc
source ~/.zshrc
```

## Verification

### 1. Test ROS2 Installation

```bash
# Terminal 1: Start talker
ros2 run demo_nodes_cpp talker

# Terminal 2: Start listener
ros2 run demo_nodes_py listener
```

### 2. Verify OpenCV Integration

```bash
# Check if cv_bridge uses your custom OpenCV
python3 -c "
import rclpy
rclpy.init()
from cv_bridge import CvBridge
import cv2
print('ROS2 cv_bridge working with OpenCV', cv2.__version__)
print('CUDA support:', cv2.cuda.getCudaEnabledDeviceCount() > 0)
rclpy.shutdown()
"
```

### 3. System Information

```bash
# Check system status
nvidia-smi
tegrastats
htop
```

### Performance Monitoring

```bash
# Monitor GPU usage
nvidia-smi -l 1

# Monitor system resources
tegrastats

# Test RT performance
sudo cyclictest -t1 -p 99 -i 1000 -l 10000
```

## Contributing

If you encounter issues or have improvements, please create an issue or submit pull requests.

## License

This setup guide is provided under MIT License. Individual software components have their own licenses.
