# Deskflow Setup (Optional)

Build Deskflow from source for mouse and keyboard sharing during development on the NVIDIA Jetson Orin Nano.

## Overview

- This section is completely optional, and a personal preference. Please feel free to skip it.
- Deskflow allows you to share keyboard and mouse between multiple computers, making development more efficient when working with the Jetson alongside other machines.

## 📦 Install Base Dependencies

Install all required development libraries and tools:

```bash
# Update system
sudo apt update

# Install base development dependencies
sudo apt install \
    build-essential \
    cmake \
    ninja-build \
    meson \
    xorg-dev \
    libx11-dev \
    libxtst-dev \
    libssl-dev \
    libglib2.0-dev \
    libgdk-pixbuf-2.0-dev \
    libnotify-dev \
    libxkbfile-dev \
    libgtk-3-dev \
    libgtest-dev \
    libgmock-dev \
    libpugixml-dev \
    libcli11-dev \
    pkg-config \
    libgl1-mesa-dev \
    libvulkan-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    gobject-introspection \
    gtk-doc-tools \
    libxcb1-dev \
    libxcb-util-dev \
    libxcb-image0-dev \
    libxcb-keysyms1-dev \
    libxcb-render-util0-dev \
    libxcb-xinerama0-dev \
    libxcb-xkb-dev \
    libxcb-randr0-dev \
    libxcb-shape0-dev \
    libxcb-sync-dev \
    libxcb-icccm4-dev \
    libxcb-cursor-dev \
    libxcb-composite0-dev \
    libxcb-glx0-dev \
    libxcb-render0-dev \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    fontconfig \
    libgirepository1.0-dev \
    valac \
    perl \
    libfontconfig1-dev \
    libfreetype6-dev \
    libx11-xcb-dev \
    libxext-dev \
    libxfixes-dev \
    libxi-dev \
    libxrender-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    libatspi2.0-dev \
    libxcursor-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxrandr-dev \
    libdbus-1-dev \
    libegl1-mesa-dev \
    libharfbuzz-dev \
    libicu-dev \
    libjpeg-dev \
    libpcre2-dev \
    libpng-dev \
    libsqlite3-dev \
    libzstd-dev \
    libsystemd-dev
```

## 🔧 Build Required Libraries

### Build libei

```bash
# Create downloads directory and clone libei
cd ~/Downloads
git clone https://gitlab.freedesktop.org/libinput/libei.git
cd libei

# Install Python dependency
pip3 install Jinja2

# Build and install
meson setup build
ninja -C build
sudo ninja -C build install

cd ~
```

### Build tomlplusplus

```bash
cd ~/Downloads
git clone https://github.com/marzer/tomlplusplus.git
cd tomlplusplus

# Build and install
mkdir build && cd build
cmake ..
make -j4
sudo make install

cd ~
```

### Build libportal

```bash
cd ~/Downloads

# Install Python dependencies
pip3 install typogrify tomli

# Clone and build libportal
git clone https://github.com/flatpak/libportal.git
cd libportal

# Build and install
meson setup build
ninja -C build
sudo ninja -C build install

cd ~
```

## 💾 Configure Swap Space

Increase swap space for building Qt (this will be large):

```bash
# Disable current swap
sudo swapoff -a

# Create 16GB swap file for Qt build
sudo dd if=/dev/zero of=/swapfile bs=1G count=16
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Verify swap is active
free -h
```

## 🖼️ Build Qt 6.8.0

Build Qt from source with optimized settings for Jetson:

```bash
cd ~/Downloads

# Download Qt source
wget https://download.qt.io/official_releases/qt/6.8/6.8.0/single/qt-everywhere-src-6.8.0.tar.xz
tar xvf qt-everywhere-src-6.8.0.tar.xz
rm qt-everywhere-src-6.8.0.tar.xz

# Configure Qt build
cd qt-everywhere-src-6.8.0
mkdir build && cd build

../configure -prefix /usr/local/qt6.8.0 \
    -release \
    -nomake examples \
    -nomake tests \
    -opensource \
    -confirm-license \
    -no-opengl \
    -no-gtk \
    -no-xcb-xlib \
    -platform linux-g++ \
    -optimize-size

# Build Qt (this takes a long time)
cmake --build . --parallel 4

# Install Qt
sudo cmake --install .
```

## 🌍 Configure Qt Environment

Add Qt to your environment variables:

```bash
# Add Qt to shell configuration
echo 'export PATH=/usr/local/qt6.8.0/bin:$PATH' >> ~/.zshrc
echo 'export LD_LIBRARY_PATH=/usr/local/qt6.8.0/lib:$LD_LIBRARY_PATH' >> ~/.zshrc

# Source the configuration
source ~/.zshrc  # or source ~/.bashrc if using bash

# Verify Qt installation
qmake --version
```

## 🚀 Build Deskflow

Build the main Deskflow application:

```bash
cd ~/Downloads

# Clone Deskflow repository
git clone https://github.com/deskflow/deskflow.git
cd deskflow

# Configure and build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j6

cd ~
```

## 🖥️ Create Desktop Application

Make Deskflow easily accessible from the desktop:

```bash
# Create desktop entry
nano ~/.local/share/applications/deskflow.desktop
```

Add the following content (adjust the username in paths):

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Deskflow
Icon=/home/jetson/Downloads/deskflow/src/apps/res/deskflow.ico
Exec=/home/jetson/Downloads/deskflow/build/bin/deskflow
Comment=Share keyboard and mouse between computers
Categories=Utility;
Terminal=false
```

Make the desktop entry executable:

```bash
chmod +x ~/.local/share/applications/deskflow.desktop
```

## ➡️ Next Step

- Your Jetson Orin Nano is now fully configured for high-performance real-time development with mouse/keyboard sharing capabilities.
- The setup is now complete.
