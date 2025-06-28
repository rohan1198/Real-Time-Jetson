# Development Environment

Optional setup for enhanced development experience with Zsh, Oh My Zsh, and useful development tools.

## Overview

This section is **completely optional** but enhances the development experience with a modern shell, productivity tools, and system monitoring utilities. Skip this if you prefer to keep the system minimal.

## 🐚 Zsh with Oh My Zsh Setup

### Install Zsh

```bash
# Install Zsh
sudo apt install zsh -y

# Set Zsh as default shell for current user
sudo chsh -s $(which zsh) $USER

# Verify installation
zsh --version
```

### Install Oh My Zsh

```bash
# Install Oh My Zsh (interactive installer)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# The installer will prompt you to switch to Zsh - choose yes
```

### Install Powerlevel10k Theme

```bash
# Install Powerlevel10k theme
git clone https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Edit .zshrc to use the theme
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc
```

### Install Recommended Fonts

```bash
# Create downloads directory
mkdir -p ~/Downloads/fonts
cd ~/Downloads/fonts

# Download MesloLGS NF fonts (recommended for Powerlevel10k)
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# Install fonts
sudo mkdir -p /usr/share/fonts/truetype/meslo
sudo cp *.ttf /usr/share/fonts/truetype/meslo/
sudo fc-cache -f -v

cd ~
```

### Install Useful Zsh Plugins

```bash
# Autosuggestions plugin
git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Syntax highlighting plugin
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Update .zshrc to enable plugins
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc
```

### Configure Zsh

```bash
# Start a new Zsh session to trigger Powerlevel10k configuration
zsh

# This will start the Powerlevel10k configuration wizard
# Follow the prompts to customize your prompt
```

## 🛠️ Development Tools

### GPU Stress Testing Tool

```bash
# Clone and build gpu-burn for GPU testing
git clone https://github.com/wilicc/gpu-burn.git
cd gpu-burn
make
cd ~

# Test GPU stress (run for 30 seconds)
cd gpu-burn
./gpu_burn 30
cd ~
```

### Final Shell Setup

```bash
# Source the new configuration
source ~/.zshrc

# If Powerlevel10k configuration didn't run, trigger it manually
p10k configure
```

## ➡️ Next Step

Continue to [OpenCV with CUDA](05-opencv-cuda.md) to build custom OpenCV with GPU acceleration.
