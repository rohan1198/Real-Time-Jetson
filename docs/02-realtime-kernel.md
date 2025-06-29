# Real-Time Kernel Setup

Install Ubuntu Pro real-time kernel for precise timing control.

## 🔑 Ubuntu Pro Subscription

Ubuntu Pro is **free for personal use** and required for the real-time kernel.

### Get Your Ubuntu Pro Token

1. Visit [Ubuntu Pro](https://ubuntu.com/pro)
2. Click "Get Ubuntu Pro for free on up to 5 machines"
3. Sign up/login and copy your token

### Install Ubuntu Pro Tools

```bash
# Install Ubuntu Pro tools
sudo apt install -y apt-utils ubuntu-advantage-tools

# Create GRUB directory if it doesn't exist
sudo mkdir -p /boot/grub

# Configure any pending packages
sudo dpkg --configure -a
```

### Attach Your Subscription

```bash
# Attach your Ubuntu Pro subscription (replace YOUR_TOKEN)
sudo pro attach YOUR_TOKEN

# Verify subscription status
sudo pro status
```

Expected output should show your subscription is active.

## ⚡ Real-Time Kernel Installation

### Enable and Install

```bash
# Enable the real-time kernel repository
sudo pro enable realtime-kernel

# Install the real-time kernel
sudo apt install ubuntu-realtime

# Reboot to load the new kernel
sudo reboot
```

### Verify Installation

After reboot, verify the RT kernel is active:

```bash
# Check kernel version - should show PREEMPT
uname -r

# Should show something like:
# 5.15.148-tegra #1 SMP PREEMPT Tue Jan 7 17:14:38 PST 2025 aarch64

# Verify PREEMPT_RT is enabled
uname -a | grep PREEMPT
```

## 🔧 Real-Time Configuration

### Test Real-Time Capabilities

```bash
chmod +x tests/stress_test.sh

sudo ./stress_test
```

## 💡 Real-Time Development Notes

With the RT kernel installed, you can now:

- Use `chrt -f 99` for highest priority real-time scheduling
- Achieve microsecond-level timing precision
- Run deterministic sensor fusion algorithms
- Eliminate timing jitter in critical paths

Example real-time process:
```bash
# Run a process with real-time priority on isolated core
sudo chrt -f 99 taskset -c 3 your_realtime_application
```

## ➡️ Next Step

Continue to [Performance Tuning](03-performance-tuning.md) to optimize CPU performance and set up core isolation.
