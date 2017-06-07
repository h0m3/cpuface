# CPUFACE

CPUFace is a simple monitor and tool for your CPU frequency and governor.

![CPUFace Screenshot](https://image.ibb.co/ftJsXa/Screenshot_0607_1426.png)

### What it does?

Its a simple interface to CPUFreq, the CPU Frequency Scaling Manager of your system

You can just call it from your command line with the command `cpuface` or trought your desktop manager menu

With CPUFace you can:

- Monitor your CPU Frequency and Governor
- Set new governor for specific CPU
- Add profiles with predefined setups
- Turn a CPU on and off ondemand

### Dependencies

CPUFace is written in [Python 3](http://python.org) and [Qt5](http://doc.qt.io/qt-5/) and those are the only runtime dependencies.

CPUFace uses a helper written in C to allow unprivileged users to change CPU settings. This helper needs a C compiler to compile and libc, you should have all of this on your computer.

Theres no dependency for KDE or Plasma, this is a pure Qt application.

### Installation

#### Arch Linux Users

CPUFace is available for Arch Users in AUR [here](https://aur.archlinux.org/packages/cpuface-git/).

If you have `yaourt` or any similar tool you can install CPUFace by one command.
```sh
yaourt -S cpuface-git
```

#### Ubuntu Users

I will soon create a package for Ubuntu and derivate systems

#### Other Users

The installation process of CPUFace is really easy, it came with automatic installation scripts. You can follow this steps:

Check if you have the follow dependencies:
- Python (at leats 3.0)
- Python Qt5 Bindings
- gcc (or any C compiler)
- libc (or compatible)
- make
- git

##### Clone this repository to a specific directory and enter it:

```sh
git clone https://github.com/h0m3/cpuface ~/cpuface
cd ~/cpuface
```

##### Compile all necessary files using make:

```sh
make
```

##### Install the package using an administrator:

```sh
sudo make install
```

##### (optional) Clean all unused packages from repository and remove it:

```sh
make clean
cd ~
rm -r ~/cpuface
```

If you want to uninstall CPUFace, you can clone it again and just run `sudo make uninstall` from the cloned directory.

### Licensing information

    Copyright (C) 2017  Artur Paiva

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
