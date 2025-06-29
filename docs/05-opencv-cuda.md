# OpenCV with CUDA Support

Build OpenCV 4.10.0 from source with full CUDA acceleration for high-performance computer vision.

## 🗑️ Remove Existing OpenCV

First, remove any existing OpenCV installations to avoid conflicts:

```bash
# Remove system OpenCV packages
sudo apt remove --purge "libopencv*" "opencv-*" python3-opencv libgstreamer-opencv1.0-0
sudo apt remove --purge libopencv-core4.5d
sudo apt autoremove
sudo apt autoclean

# Verify removal
dpkg -l | grep opencv
# Should show no results or minimal remaining packages
```

## 📦 Install Build Dependencies

Install all required dependencies for building OpenCV with CUDA support:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Essential build tools
sudo apt install -y \
    build-essential \
    cmake \
    cmake-gui \
    git \
    pkg-config \
    libjpeg-dev \
    libtiff5-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libavresample-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgtk2.0-dev \
    libgtk-3-dev \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    libxvidcore-dev \
    libx264-dev \
    libtbb2 \
    libtbb-dev \
    libdc1394-dev \
    libv4l-dev \
    v4l-utils \
    liblapacke-dev \
    libopenblas-dev \
    libatlas-base-dev \
    libeigen3-dev \
    libtheora-dev \
    libvorbis-dev \
    libxine2-dev \
    libfaac-dev \
    libmp3lame-dev \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    x264 \
    unzip \
    yasm

# Python development packages
sudo apt install -y \
    python3-dev \
    python3-pip \
    python3-testresources

# Upgrade pip and install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install numpy matplotlib

# Additional libraries for contrib modules
sudo apt install -y \
    libprotobuf-dev \
    protobuf-compiler \
    libgoogle-glog-dev \
    libgflags-dev \
    libgphoto2-dev \
    libeigen3-dev \
    libhdf5-dev \
    libtesseract-dev \
    libleptonica-dev
```

## 📥 Download OpenCV Source

Download OpenCV and the contrib modules:

```bash
# Create build directory
cd ~
mkdir opencv_build && cd opencv_build

# Download OpenCV 4.10.0 and contrib modules
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.10.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.10.0.zip

# Extract archives
unzip opencv.zip
unzip opencv_contrib.zip

# Create build directory
mkdir -p opencv-4.10.0/build
cd opencv-4.10.0/build
```

## ⚙️ Configure Build

Configure the OpenCV build with CUDA support and optimizations:

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

### Verify Configuration

Check the configuration output for important settings:

```bash
# Look for these key confirmations in the CMake output:
# ✅ CUDA: YES (ver 12.6)
# ✅ CUDNN: YES (ver 8.x)
# ✅ Python 3: YES
# ✅ GStreamer: YES
# ✅ V4L/V4L2: YES

# If any critical features show "NO", install missing dependencies and reconfigure
```

## 🔨 Build OpenCV

Compile OpenCV (this takes 2-3 hours):

```bash
# Build using all cores (shouldn't be an issue as we increased swap memory: see 03-performance-tuning.md)
make -j6
```

### Build Monitoring

While building, you can monitor system resources:

```bash
# Monitor CPU and memory usage
htop

# Monitor GPU usage (OpenCV build will use CUDA)
nvidia-smi

# Check build progress (in another terminal)
ps aux | grep make
```

## 📦 Install OpenCV

After successful compilation, install OpenCV:

```bash
# Install OpenCV
sudo make install

# Update library cache
sudo ldconfig

# Verify installation directories
ls -la /usr/local/lib/libopencv*
ls -la /usr/local/include/opencv4/
```

## ✅ Verify Installation

Test that OpenCV is properly installed with CUDA support:

```bash
# Test OpenCV Python import and version
python3 -c "
import cv2
print('OpenCV version:', cv2.__version__)
print('OpenCV build info:')
print(cv2.getBuildInformation())
"

# Test CUDA support specifically
python3 -c "
import cv2
print('OpenCV version:', cv2.__version__)
print('CUDA devices:', cv2.cuda.getCudaEnabledDeviceCount())
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    print('✅ CUDA support is working!')
    
    # Test basic CUDA operations
    import numpy as np
    
    # Create test image
    img = np.random.randint(0, 255, (1000, 1000, 3), dtype=np.uint8)
    
    # Upload to GPU
    gpu_img = cv2.cuda_GpuMat()
    gpu_img.upload(img)
    
    # Perform GPU operation
    gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)
    
    # Download result
    result = gpu_gray.download()
    
    print('✅ GPU operations working!')
    print(f'Original shape: {img.shape}')
    print(f'Result shape: {result.shape}')
else:
    print('❌ CUDA not detected')
"
```

### Test pkg-config

```bash
# Test pkg-config for OpenCV
pkg-config --modversion opencv4
# Should show: 4.10.0

pkg-config --cflags opencv4
pkg-config --libs opencv4

# Verify CUDA in build info
pkg-config --cflags opencv4 | grep -i cuda
```

## ➡️ Next Step

Continue to [ROS2 Humble Setup](06-ros2-humble.md) to build ROS2 from source with your custom OpenCV integration.
