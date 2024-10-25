# Real-Time-Jetson
Setting up the Jetson for real-time (deterministic) tasks

## Table of Contents

1. [Initial System Updates](#initial-system-updates)
2. [Preempt-RT Kernel Patch](#preempt-rt-kernel-patch)
3. [CPU Performance Mode](#cpu-performance-mode)
4. [Dependencies and Additional Packages](#dependencies-and-additional-packages)
5. [Zsh and Oh My Zsh Setup](#zsh-and-oh-my-zsh-setup)
6. [ROS 2 Humble Installation](#ros-2-humble-installation)
7. [Deskflow Installation (Optional)](#deskflow-installation-optional)

## Initial System Updates

Perform these steps to ensure your system is up-to-date:

```bash
sudo apt update && apt list --upgradable
sudo apt upgrade -y && sudo apt dist-upgrade -y
sudo reboot
sudo apt autoremove -y
sudo apt autoclean -y
```

## Preempt-RT Kernel Patch

To install the real-time kernel packages:

1. Install necessary tools:
   ```bash
   sudo apt install curl wget nano gedit
   ```

2. Edit the NVIDIA L4T APT source list:
   ```bash
   sudo nano /etc/apt/sources.list.d/nvidia-l4t-apt-source.list
   ```

3. Add the following line (replace `<release>` with your Jetson's release):
   ```
   deb https://repo.download.nvidia.com/jetson/rt-kernel <release> main
   ```

4. Install the RT kernel packages:
   ```bash
   sudo apt install nvidia-l4t-rt-kernel nvidia-l4t-rt-kernel-headers nvidia-l4t-rt-kernel-oot-modules nvidia-l4t-display-rt-kernel
   sudo reboot
   ```

## CPU Performance Mode

Set CPU governors to performance mode:

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/cpu-performance-mode.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Set CPU governor to performance mode
   After=multi-user.target

   [Service]
   Type=oneshot
   ExecStart=/bin/sh -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable cpu-performance-mode.service
   sudo systemctl start cpu-performance-mode.service
   sudo systemctl status cpu-performance-mode.service
   ```

4. Verify the changes:
   ```bash
   cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   ```

## Dependencies and Additional Packages

Install essential development tools and utilities:

```bash
sudo apt install cmake dconf-editor ffmpeg build-essential tilix vlc ubuntu-restricted-extras python3-dev python3-pip python3-venv python3-numba lm-sensors cheese neofetch htop nvtop chrome-gnome-shell gnome-tweaks git stress-ng -y
sudo pip3 install jetson-utils
sudo apt install rt-tests
sudo reboot
```

## Zsh and Oh My Zsh Setup

1. Install Zsh and set it as the default shell:
   ```bash
   sudo apt install zsh -y
   sudo chsh -s $(which zsh)
   ```

2. Install Oh My Zsh:
   ```bash
   sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
   ```

3. Install Powerlevel10k theme:
   ```bash
   git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
   ```

4. Download and install Meslo Nerd Font:
   ```bash
   cd ~/Downloads
   wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
   wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
   wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
   wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf
   ```

5. Install Zsh plugins:
   ```bash
   git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
   ```

6. Jetson-GPU-burn
   ```bash
   https://github.com/anseeto/jetson-gpu-burn.git
   cd jetson-gpu-burn
   make
   ```

## ROS 2 Humble Installation

1. Set up repositories:
   ```bash
   sudo apt install software-properties-common
   sudo add-apt-repository universe
   ```

2. Add ROS 2 GPG key:
   ```bash
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
   ```

3. Add ROS 2 repository:
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

4. Update and upgrade:
   ```bash
   sudo apt update && apt list --upgradable
   sudo apt upgrade -y && sudo apt dist-upgrade -y
   ```

5. Install ROS 2 Humble:
   ```bash
   sudo apt install ros-humble-desktop
   ```

6. Add ROS 2 setup to your shell configuration:
   ```bash
   echo "source /opt/ros/humble/setup.zsh" >> ~/.zshrc
   ```

## Deskflow Installation (Optional)

1. Install dependencies:
   ```bash
   sudo apt install libxtst-dev libpugixml-dev libgdk-pixbuf-2.0-dev libnotify-dev qt6-base-dev libgmock-dev libxkbfile-dev
   ```

2. Clone and build Deskflow:
   ```bash
   git clone https://github.com/deskflow/deskflow.git
   cd deskflow
   cmake -B build
   ```

3. Create a desktop entry:
   ```bash
   nano ~/.local/share/applications/deskflow.desktop
   ```

4. Add the following content (adjust paths as necessary):
   ```
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=Deskflow
   Icon=/home/jetson/Downloads/deskflow/res/app.ico
   Exec=/home/jetson/Downloads/deskflow/build/bin/deskflow
   Comment=Start Synergy to share keyboard and mouse
   Categories=Utility;
   Terminal=false
   ```
   
