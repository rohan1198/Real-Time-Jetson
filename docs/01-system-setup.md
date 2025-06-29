# System Setup

Initial system configuration with updates and essential packages.


## 🔄 Updates

Start with a fresh system update:

```bash
# Update package lists and upgrade system
sudo apt update && apt list --upgradable
sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo reboot

# Clean up after updates
sudo apt autoremove
sudo apt autoclean
```

## 📦 Essential Development Packages

Install core development tools and utilities:

```bash
# Development tools and utilities
sudo apt install -y \
    cmake \
    dconf-editor \
    build-essential \
    tilix \
    vlc \
    ubuntu-restricted-extras \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-numba \
    lm-sensors \
    cheese \
    neofetch \
    htop \
    nvtop \
    chrome-gnome-shell \
    gnome-tweaks \
    git \
    stress-ng \
    nano \
    curl \
    gedit \
    wget \
    rt-tests
```

## 🐍 Python Development Setup

Set up Python environment and essential packages:

```bash
# Install jetson-utils for GPU monitoring
sudo pip3 install jetson-utils

# Install pytest for our testing framework
pip3 install pytest psutil numpy

# Verify Python setup
python3 --version
pip3 --version
```

## 🔧 System Configuration

Configure some useful system settings:

```bash
# Install sensors for hardware monitoring
sudo apt install lm-sensors
sudo sensors-detect --auto

# Test system stress capabilities (optional)
stress-ng --help > /dev/null && echo "✅ Stress testing tools ready"
```

## 🔍 Verification Commands

Run these commands to verify the installation:

```bash
# Test essential development tools
gcc --version
cmake --version
python3 -c "import numpy; print('NumPy:', numpy.__version__)"

# Test hardware monitoring
sensors
htop --version
nvtop --version

# Verify Git configuration (set if needed)
git --version
# git config --global user.name "Your Name"
# git config --global user.email "your.email@example.com"
```

## ⚠️ Troubleshooting

**Issue**: Package installation fails with dependency errors
```bash
# Solution: Fix broken packages
sudo apt --fix-broken install
sudo dpkg --configure -a
```

**Issue**: CUDA not found
```bash
# Solution: Verify JetPack installation
sudo apt list --installed | grep nvidia
# Reinstall JetPack if needed
sudo apt install nvidia-jetpack

# Solution 2: Add cuda to ~/.zshrc
echo 'export PATH="/usr/local/cuda-12.6/bin:$PATH"' >> ~/.zshrc
echo 'export LD_LIBRARY_PATH="/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH"' >> ~/.zshrc
# Source
source ~/.zshrc
```

**Issue**: Python packages fail to install
```bash
# Solution: Update pip and retry
python3 -m pip install --upgrade pip
pip3 install pytest psutil numpy
```

## ➡️ Next Step

Continue to [Real-Time Kernel Setup](02-realtime-kernel.md) to install the Ubuntu Pro real-time kernel.
