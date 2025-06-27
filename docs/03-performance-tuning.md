# Performance Tuning

Optimize CPU performance and set up core isolation for dedicated real-time processing.

## ⚡ CPU Performance Governor

Set all CPU cores to maximum performance mode for consistent processing power.

### Create Performance Service

```bash
# Create systemd service for performance mode
sudo tee /etc/systemd/system/cpu-performance-mode.service > /dev/null << 'EOF'
[Unit]
Description=Set CPU governor to performance mode
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'

[Install]
WantedBy=multi-user.target
EOF
```

### Enable Performance Mode

```bash
# Enable and start the service
sudo systemctl enable cpu-performance-mode.service
sudo systemctl start cpu-performance-mode.service

# Check service status
sudo systemctl status cpu-performance-mode.service

# Verify all CPUs are in performance mode
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
# Should show "performance" for all cores
```

## 💾 Increase Swap Space

Increase swap space to 10GB for building large projects like OpenCV and ROS2.

```bash
# Disable current swap
sudo swapoff -a

# Create 10GB swap file
sudo dd if=/dev/zero of=/swapfile bs=1G count=10

# Set correct permissions
sudo chmod 600 /swapfile

# Format as swap
sudo mkswap /swapfile

# Enable swap
sudo swapon /swapfile

# Verify swap is active
free -h
```

### Make Swap Permanent

```bash
# Backup fstab
sudo cp /etc/fstab /etc/fstab.backup

,# Add swap to fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify fstab entry
tail -1 /etc/fstab
```

## 🎯 CPU Core Isolation (Core 3)

Isolate CPU core 3 for dedicated real-time processing without OS interference.

### Configure Kernel Boot Parameters

```bash
# Backup current GRUB configuration
sudo cp /boot/extlinux/extlinux.conf /boot/extlinux/extlinux.conf.backup

# Edit GRUB configuration
sudo nano /boot/extlinux/extlinux.conf
```

Find the line starting with `APPEND ${cbootargs} root=PARTUUID=...` and modify it:

```bash
# Append the following to the line:
isolcpus=3 nohz_full=3 rcu_nocbs=3
```

```bash
# This is what the modified line should look like:
APPEND ${cbootargs} root=PARTUUID=e7231ec5-80ed-49bc-b32f-4461146dca28 rw rootwait rootfstype=ext4 mminit_loglevel=4 console=ttyTCU0,115200 firmware_class.path=/etc/firmware fbcon=map:0 nospectre_bhb video=efifb:off console=tty0 nv-auto-config isolcpus=3 nohz_full=3 rcu_nocbs=3
```

**Parameter explanations:**
- `isolcpus=3` - Isolates CPU core 3 from the kernel scheduler
- `nohz_full=3` - Disables periodic timer ticks on core 3 when only one process is running
- `rcu_nocbs=3` - Moves RCU callback processing off core 3

### Reboot

```bash
# Reboot to apply changes
sudo reboot

# Verify configuration was updated
cat /proc/cmdline | grep isolcpus
```

### Using the Isolated Core

**Method 1: Command-line applications**
```bash
# Run any command on isolated core 3
taskset -c 3 your_application

# Example: Run with real-time priority
sudo chrt -f 99 taskset -c 3 your_realtime_application

# Check which core a process is running on
taskset -p <process_id>
```

**Method 2: Python applications**
```python
import os
import psutil

# Set your process to use only isolated core 3
p = psutil.Process()
p.cpu_affinity([3])

# Alternatively, using os module
os.sched_setaffinity(0, {3})

# Your real-time sensor processing code here
```

**Method 3: Set real-time priority**
```bash
# Run with real-time scheduling and core isolation
sudo chrt -f 99 taskset -c 3 your_realtime_application

# Explanation:
# chrt -f 99: Set FIFO real-time scheduling with priority 99 (highest)
# taskset -c 3: Pin to isolated core 3
```

## ➡️ Next Step

Continue to [Development Environment](04-development-environment.md) for optional shell and development tools setup.
