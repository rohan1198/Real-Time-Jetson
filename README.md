# Real-Time Jetson

A guide for setting up a high-performance, real-time development environment on the NVIDIA Jetson Orin Nano with Jetpack 6.2, Ubuntu 22.04, real-time kernel, CPU core isolation, CUDA-enabled OpenCV, and ROS2 Humble with custom OpenCV+CUDA.

## 🎯 Overview

- **Real-time Ubuntu kernel** for precise timing control
- **CPU core isolation** for dedicated real-time processing
- **CUDA-enabled OpenCV** for GPU-accelerated computer vision
- **ROS2 Humble** built from source with custom OpenCV+CUDA integration
- **Performance optimizations** for embedded development


## 🚀 Installation

| Step | Documentation | Description |
|------|---------------|-------------|
| 1 | [System Setup](docs/01-system-setup.md) | Updates & essential packages |
| 2 | [Real-Time Kernel](docs/02-realtime-kernel.md) | Ubuntu Pro & RT kernel |
| 3 | [Performance Tuning](docs/03-performance-tuning.md) | CPU governor, swap, core isolation |
| 4 | [Development Environment](docs/04-development-environment.md) | Zsh, tools (optional) |
| 5 | [OpenCV with CUDA](docs/05-opencv-cuda.md) | Custom OpenCV 4.10.0 build |
| 6 | [ROS2 Humble](docs/06-ros2-humble.md) | ROS2 from source + vision packages |
| 7 | [Build Deskflow](docs/07-deskflow.md) | Keyboard and mouse sharing (optional) |

## 💡 Real-Time Development Example

```bash
# Run real-time processing on isolated core 3
sudo chrt -f 99 taskset -c 3 ros2 run your_package sensor_node

# Monitor system performance
htop  # Check core 3 isolation
nvidia-smi  # Monitor GPU usage
```
