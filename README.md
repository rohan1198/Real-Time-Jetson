# Real-Time Jetson

A comprehensive guide for setting up a high-performance, real-time development environment on the NVIDIA Jetson Orin Nano with Ubuntu 22.04, real-time kernel, CPU core isolation, CUDA-enabled OpenCV, and ROS2 Humble with custom OpenCV+CUDA.

## 🎯 Overview

- **Real-time Ubuntu kernel** for precise timing control
- **CPU core isolation** for dedicated real-time processing
- **CUDA-enabled OpenCV** for GPU-accelerated computer vision
- **ROS2 Humble** built from source with custom OpenCV+CUDA integration
- **Performance optimizations** for embedded development


## 🚀 Installation

| Step | Documentation | Description | Test Command |
|------|---------------|-------------|--------------|
| 1 | [System Setup](docs/01-system-setup.md) | Updates & essential packages | `pytest tests/test_system_setup.py` |
| 2 | [Real-Time Kernel](docs/02-realtime-kernel.md) | Ubuntu Pro & RT kernel | `pytest tests/test_realtime_kernel.py` |
| 3 | [Performance Tuning](docs/03-performance-tuning.md) | CPU governor, swap, core isolation | `pytest tests/test_performance.py` |
| 4 | [Development Environment](docs/04-development-environment.md) | Zsh, tools (optional) | Manual verification |
| 5 | [OpenCV with CUDA](docs/05-opencv-cuda.md) | Custom OpenCV 4.10.0 build | `pytest tests/test_opencv_cuda.py` |
| 6 | [ROS2 Humble](docs/06-ros2-humble.md) | ROS2 from source + vision packages | `pytest tests/test_ros2_vision.py` |
| 7 | [Verification](docs/07-verification.md) | Complete system testing | `pytest tests/test_integration.py` |

### Quick Commands

```bash
# Clone the repository
git clone https://github.com/rohan1198/Real-Time-Jetson.git
cd Real-Time-Jetson

# Install pytest for testing
pip3 install pytest psutil

# Follow docs/ in order, testing after each step
# Example:
pytest tests/test_system_setup.py -v
```

## 🧪 Testing

Each component includes comprehensive pytest validation:

```bash
# Test individual components
pytest tests/test_opencv_cuda.py -v
pytest tests/test_ros2_vision.py -v

# Test everything
pytest tests/ -v

# Test with detailed output
pytest tests/ -v -s
```

## 📚 Additional Documentation

- **[Troubleshooting](docs/troubleshooting.md)** - Solutions for common issues
- **[Coordinate Systems](docs/coordinate-systems.md)** - RealSense vs EuRoC analysis for VI sensor development

## 🎯 What You'll Have After Setup

- ✅ **Real-time kernel** with microsecond-precision timing
- ✅ **Isolated CPU core 3** for dedicated real-time processing
- ✅ **CUDA-accelerated OpenCV 4.10.0** with GPU operations
- ✅ **Complete ROS2 Humble** with vision packages (`cv_bridge`, `image_pipeline`, etc.)
- ✅ **Performance-optimized system** for SLAM development
- ✅ **Professional development environment** with proper testing

## 💡 Real-Time Development Example

```bash
# Source the custom environment
source config/setup_environment.sh

# Run real-time processing on isolated core 3
sudo chrt -f 99 taskset -c 3 ros2 run your_package sensor_node

# Monitor system performance
htop  # Check core 3 isolation
nvidia-smi  # Monitor GPU usage
```
