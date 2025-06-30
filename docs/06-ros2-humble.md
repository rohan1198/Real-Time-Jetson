# ROS2 Humble from Source

Build ROS2 Humble from source with complete vision packages and custom CUDA OpenCV integration.

## 🗑️ Complete ROS Removal

**IMPORTANT**: Remove any existing ROS installations to avoid conflicts:

```bash
# Remove all ROS distributions
sudo apt remove --purge ros-humble-* ros-foxy-* ros-galactic-* ros-iron-* ros-rolling-* ros-*
sudo apt autoremove
sudo apt autoclean

# Remove ROS repositories and keys
sudo rm -f /etc/apt/sources.list.d/ros*.list
sudo rm -f /usr/share/keyrings/ros-archive-keyring.gpg

# Remove any ROS workspaces (adjust paths as needed)
rm -rf ~/ros2_ws ~/catkin_ws ~/colcon_ws ~/ros2_humble

# Remove ROS environment variables from shell configs
sed -i '/ros/Id' ~/.bashrc ~/.zshrc 2>/dev/null || true
sed -i '/ROS/Id' ~/.bashrc ~/.zshrc 2>/dev/null || true

# Update package cache
sudo apt update

# Verify no ROS packages remain
dpkg -l | grep ros
# Should show minimal or no results

# Verify no ROS environment variables
printenv | grep -i ROS
# Should be empty
```

## 🌍 Setup Locale and Repositories

Configure the system for ROS2 development:

```bash
# Set up locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add universe repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add ROS2 GPG key and repository (temporary - will be removed after build)
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
```

## 📦 Install Build Dependencies

Install all dependencies needed for building ROS2:

```bash
# Install development tools and ROS tools
sudo apt install -y \
    python3-flake8-docstrings \
    python3-pip \
    python3-pytest-cov \
    ros-dev-tools

# Install additional Python tools
sudo apt install -y \
    python3-flake8-blind-except \
    python3-flake8-builtins \
    python3-flake8-class-newline \
    python3-flake8-comprehensions \
    python3-flake8-deprecated \
    python3-flake8-import-order \
    python3-flake8-quotes \
    python3-pytest-repeat \
    python3-pytest-rerunfailures

# Install additional build dependencies
sudo apt install -y \
    libasio-dev \
    libtinyxml2-dev \
    libcunit1-dev \
    libeigen3-dev \
    libboost-all-dev \
    libceres-dev \
    python3-lark \
    python3-vcstool \
    python3-numpy \
    python3-dev \
    libboost-python-dev \
    libboost-thread-dev

# Install Qt5 and PyQt5 dependencies
sudo apt install -y \
    qtbase5-dev \
    qtdeclarative5-dev \
    qtbase5-dev-tools \
    pyqt5-dev \
    pyqt5-dev-tools \
    python3-pyqt5 \
    python3-pyqt5.sip
```

## 📁 Create ROS2 Workspace

Set up the workspace and download all source code:

```bash
# Create workspace
mkdir -p ~/ros2_humble/src
cd ~/ros2_humble

# Import ROS2 source code
vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src

# Add essential vision and perception packages for SLAM development
cd src

# Vision OpenCV (cv_bridge, image_geometry)
git clone https://github.com/ros-perception/vision_opencv.git -b humble

# Image pipeline (image processing nodes)
git clone https://github.com/ros-perception/image_pipeline.git -b humble

# Image transport plugins (compression, etc.)
git clone https://github.com/ros-perception/image_transport_plugins.git -b humble

# Vision messages (AprilTag, object detection msgs)
git clone https://github.com/ros-perception/vision_msgs.git -b humble

# Note: image_common (camera_info_manager, camera_calibration_parsers, image_transport) 
# is already included in the default ROS2 source
```

## 🔧 Create Custom OpenCV Toolchain

Create a CMake toolchain file to force all packages to use our custom OpenCV:

```bash
cd ~/ros2_humble

# Create the CMake toolchain file
cat > custom_opencv_toolchain.cmake << 'EOF'
# Custom OpenCV CMake Toolchain for ROS2 Humble
# Forces all packages to use CUDA-enabled OpenCV 4.10.0

message(STATUS "=== GLOBAL: Using Custom CUDA OpenCV Toolchain ===")

# Force OpenCV paths to be found first
set(OpenCV_DIR "/usr/local/lib/cmake/opencv4" CACHE PATH "OpenCV Config Directory" FORCE)
set(OpenCV_ROOT "/usr/local" CACHE PATH "OpenCV Root Directory" FORCE)

# Prepend custom OpenCV to all CMake search paths
set(CMAKE_PREFIX_PATH "/usr/local/lib/cmake/opencv4;/usr/local;${CMAKE_PREFIX_PATH}" CACHE STRING "CMake prefix path" FORCE)
set(CMAKE_FIND_ROOT_PATH "/usr/local;${CMAKE_FIND_ROOT_PATH}" CACHE STRING "CMake find root path" FORCE)

# Ensure our OpenCV is found before system OpenCV
list(PREPEND CMAKE_MODULE_PATH "/usr/local/lib/cmake/opencv4")
list(PREPEND CMAKE_PREFIX_PATH "/usr/local/lib/cmake/opencv4")

# Set pkg-config path for runtime
set(ENV{PKG_CONFIG_PATH} "/usr/local/lib/pkgconfig:$ENV{PKG_CONFIG_PATH}")

# Force CMake to ignore system OpenCV paths
set(CMAKE_IGNORE_PATH "/usr/lib/x86_64-linux-gnu/cmake/opencv4;/usr/lib/aarch64-linux-gnu/cmake/opencv4;/usr/share/opencv4" CACHE STRING "Paths to ignore" FORCE)

# Debug output
message(STATUS "TOOLCHAIN: OpenCV_DIR = ${OpenCV_DIR}")
message(STATUS "TOOLCHAIN: CMAKE_PREFIX_PATH = ${CMAKE_PREFIX_PATH}")
message(STATUS "TOOLCHAIN: Custom CUDA OpenCV 4.10.0 will be used by all packages")
message(STATUS "=================================================")
EOF
```

## 📋 Install Dependencies with rosdep

Install all ROS2 dependencies while excluding OpenCV packages:

```bash
cd ~/ros2_humble

# Initialize and update rosdep
sudo rosdep init
rosdep update

# Install dependencies excluding OpenCV packages to avoid conflicts
rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers libopencv-dev libopencv-contrib-dev libopencv-imgproc-dev opencv2 python3-opencv"
```

## 🔨 Build ROS2 with Custom OpenCV

Build the complete ROS2 system with our custom OpenCV integration:

```bash
# Set environment variables for custom OpenCV
export OpenCV_DIR=/usr/local/lib/cmake/opencv4
export CMAKE_PREFIX_PATH=/usr/local/lib/cmake/opencv4:$CMAKE_PREFIX_PATH
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Verify custom OpenCV is accessible
pkg-config --modversion opencv4
# Should show 4.10.0

# If the above command throws an error, create a symlink to fix the issue
sudo ln -s /usr/local/lib/pkgconfig/opencv.pc /usr/local/lib/pkgconfig/opencv4.pc

# Then run the previous command again
```

```bash
# Build everything with the custom OpenCV toolchain
cd ~/ros2_humble
colcon build --symlink-install \
    --cmake-args \
        -DCMAKE_TOOLCHAIN_FILE=/home/$USER/ros2_humble/custom_opencv_toolchain.cmake \
        -DOpenCV_DIR=/usr/local/lib/cmake/opencv4 \
        -DCMAKE_PREFIX_PATH=/usr/local/lib/cmake/opencv4 \
        -DCMAKE_BUILD_TYPE=Release \
    --parallel-workers 6
```

## 🔒 Freeze Installation

After successful build, remove the ROS2 repository to prevent automatic updates:

```bash
# Remove ROS2 repository and keyring to freeze the installation
sudo rm /etc/apt/sources.list.d/ros2.list
sudo rm /usr/share/keyrings/ros-archive-keyring.gpg

# Update package cache
sudo apt update

echo "✅ ROS2 repository removed - installation is now frozen"
```

## 🌍 Create Environment Setup

Create a comprehensive environment setup script:

```bash
# Create the environment setup script
cat > ~/ros2_humble/setup_custom_ros2.sh << 'EOF'
#!/bin/bash
# Custom ROS2 + CUDA OpenCV environment setup

echo "🚀 Setting up Custom ROS2 Humble with CUDA OpenCV environment..."

# OpenCV environment variables
export OpenCV_DIR=/usr/local/lib/cmake/opencv4
export OpenCV_ROOT=/usr/local
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export CMAKE_PREFIX_PATH=/usr/local/lib/cmake/opencv4:/usr/local:$CMAKE_PREFIX_PATH

# Force CMake to find our OpenCV first
export CMAKE_FIND_ROOT_PATH=/usr/local:$CMAKE_FIND_ROOT_PATH

# Ignore system OpenCV paths during CMake configuration
export CMAKE_IGNORE_PATH="/usr/lib/x86_64-linux-gnu/cmake/opencv4:/usr/lib/aarch64-linux-gnu/cmake/opencv4:/usr/share/opencv4"

# ROS2 environment
source ~/ros2_humble/install/setup.bash

echo "📦 OpenCV version: $(pkg-config --modversion opencv4)"

# Test cv_bridge
python3 -c "
try:
    from cv_bridge import CvBridge
    import cv2
    print('✅ cv_bridge working with OpenCV', cv2.__version__)
    print('🎯 CUDA devices available:', cv2.cuda.getCudaEnabledDeviceCount())
except Exception as e:
    print('❌ cv_bridge not available:', e)
" 2>/dev/null

echo "🎯 Environment ready for building with custom OpenCV!"
EOF

chmod +x ~/ros2_humble/setup_custom_ros2.sh

# Copy to config directory for easy access
mkdir -p ~/Real-Time-Jetson/config
cp ~/ros2_humble/setup_custom_ros2.sh ~/Real-Time-Jetson/config/setup_environment.sh
```

## ✅ Verify Installation

Test the complete ROS2 installation with vision packages:

```bash
# Source the environment
source ~/ros2_humble/setup_custom_ros2.sh

# Test basic ROS2 functionality
ros2 run demo_nodes_cpp talker &
sleep 2
ros2 run demo_nodes_py listener &
sleep 5
killall talker listener

echo "✅ ROS2 core functionality verified"

# Test vision packages
python3 -c "
print('=== Testing Vision Packages with CUDA OpenCV ===')
try:
    from cv_bridge import CvBridge
    import cv2
    import numpy as np
    from sensor_msgs.msg import Image
    
    print('✅ cv_bridge imported successfully!')
    print('✅ OpenCV version in cv_bridge:', cv2.__version__)
    print('✅ CUDA devices available:', cv2.cuda.getCudaEnabledDeviceCount())
    
    # Test CvBridge functionality
    bridge = CvBridge()
    print('✅ CvBridge instance created successfully')
    
    # Test conversion
    cv_image = np.zeros((480, 640, 3), dtype=np.uint8)
    ros_image = bridge.cv2_to_imgmsg(cv_image, 'bgr8')
    converted_back = bridge.imgmsg_to_cv2(ros_image, 'bgr8')
    
    print('✅ Image conversion test passed')
    print('✅ cv_bridge is fully functional with CUDA-enabled OpenCV!')
    
    # Test CUDA functionality
    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        gpu_mat = cv2.cuda_GpuMat()
        gpu_mat.upload(cv_image)
        cpu_result = gpu_mat.download()
        print('✅ CUDA operations working in OpenCV!')
    
except Exception as e:
    print('❌ Error:', e)
    import traceback
    traceback.print_exc()
"

# Check available vision packages
echo -e "\n=== Available Vision Packages ==="
ros2 pkg list | grep -E "(image_|vision_|camera_)" | head -10

# Check image transport plugins
echo -e "\n=== Image Transport Plugins ==="
ros2 run image_transport list_transports
```

## 💡 Building Additional Packages

For future SLAM packages, use this approach:

```bash
# Source environment
source ~/ros2_humble/setup_custom_ros2.sh

# Example: Add a new vision package
cd ~/ros2_humble/src
git clone <package-repository> -b humble

# Build with custom OpenCV toolchain
cd ~/ros2_humble
colcon build --symlink-install \
    --packages-select <package-name> \
    --cmake-args \
        -DCMAKE_TOOLCHAIN_FILE=/home/$USER/ros2_humble/custom_opencv_toolchain.cmake \
        -DCMAKE_BUILD_TYPE=Release
```

## ➡️ Next Step

Continue to [Verification](07-verification.md) to test the complete system integration.
