# Surface Performance Indicator
A Python script that provides a tray icon or AppIndicator to switch performance modes for Microsoft Surface, as a replacement of [Windows performance power slider](https://docs.microsoft.com/en-us/surface/maintain-optimal-power-settings-on-surface-devices#windows-performance-power-slider) on Linux

![Surface Performance Indicator](https://i.loli.net/2021/02/07/LS7IQnCu9ARceE5.png)

## What does it actually control?
Depending on Surface Control Utility, it might not have exactly the same behavior as Windows performance power slider does. As far as I observe on Surface Pro 6 (i7), it is likely to control fan speed only, and CPU behavior can be configured independently. For more details, see [this page](https://github.com/linux-surface/surface-aggregator-module/wiki/Performance-Modes).

## Dependency
- Python (>=3.6)
  - pystray
-  Surface Control Utility (>=0.3.1)

## Installation
### Arch-based distro
Install [surface-performance-indicator](https://aur.archlinux.org/packages/surface-performance-indicator-git/) from AUR
### Other distro
1. Install [surface-control](https://github.com/linux-surface/surface-control)
2. Install `pystray`
```
$ pip3 install pystray
```
3. Install `spi.py` to `PATH`
```
# install -Dm755 spi.py /usr/local/bin/spi
```
## Usage
Before running for the first time, add your user to `surface-control` group
```
# usermod -aG surface-control <YOUR_USER_NAME>
```
Then you can start the indicator
```
$ spi &
```
## Autostart
```
$ cp surface-performance-indicator.desktop ~/.config/autostart
```