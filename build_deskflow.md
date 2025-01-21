# Building Deskflow on Nvidia Jetson Orin Nano

This guide provides step-by-step instructions for building Deskflow from source on the Nvidia Jetson Orin Nano.

** Make sure that you have al least 40GB of free disk space **

# 1. Base Dependencies

```bash
sudo apt update
sudo apt install \
    build-essential \
    cmake \
    ninja-build \
    meson\
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

# 2. Build and install libei

```bash
cd ~/Downloads
git clone https://gitlab.freedesktop.org/libinput/libei.git
cd libei
pip3 install Jinja2
meson setup build
ninja -C build
sudo ninja -C build install
cd
```

# 3. Build and install tomlplusplus

```bash
cd ~/Downloads
git clone https://github.com/marzer/tomlplusplus.git
cd tomlplusplus
mkdir build && cd build
cmake ..
make -j4
sudo make install
cd
```

# 4. Build and install libportal

```bash
cd ~/Downloads
pip3 install typogrify tomli
git clone https://github.com/flatpak/libportal.git
cd libportal
meson setup build
ninja -C build
sudo ninja -C build install
cd
```

# 5. Configure Swap Space

Increase swap space for building QT

```bash
sudo swapoff -a
sudo dd if=/dev/zero of=/swapfile bs=1G count=32
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

# 6. Build QT 6.7.0

```bash
cd ~/Downloads
wget https://download.qt.io/official_releases/qt/6.7/6.7.0/single/qt-everywhere-src-6.7.0.tar.xz
tar xvf qt-everywhere-src-6.7.0.tar.xz
rm qt-everywhere-src-6.7.0.tar.xz
cd qt-everywhere-src-6.7.0
mkdir build && cd build

../configure -prefix /usr/local/qt6.7.0 \
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

cmake --build . --parallel 4
sudo cmake --install .
```

# 7. Configure QT Environment

```bash
# Add to your shell's rc file (.bashrc or .zshrc)
echo 'export PATH=/usr/local/qt6.7.0/bin:$PATH' >> ~/.zshrc
echo 'export LD_LIBRARY_PATH=/usr/local/qt6.7.0/lib:$LD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc  # or source ~/.bashrc if using bash
```

# 8. Resize swap

Resize swap to 10GB (change it to whatever you feel like)

```bash
sudo swapoff -a
sudo dd if=/dev/zero of=/swapfile bs=1G count=10
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make swap permanent
sudo cp /etc/fstab /etc/fstab.backup
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

# 9. Build Deskflow

```bash
cd ~/Downloads
git clone https://github.com/deskflow/deskflow.git
cd deskflow
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j6
cd
```

# 10. Make Deskflow a Desktop Application

```bash
nano ~/.local/share/applications/deskflow.desktop
```

- Add the following content (Adjust paths as needed):

```
[Desktop Entry]
Version=1.0
Type=Application
Name=Deskflow
Icon=/home/jetson/Downloads/deskflow/src/apps/res/deskflow.ico
Exec=/home/jetson/Downloads/deskflow/build/bin/deskflow
Comment=Start Synergy to share keyboard and mouse
Categories=Utility;
Terminal=false
```

- Make it executable

```bash
chmod +x ~/.local/share/applications/deskflow.desktop
```
