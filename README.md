# CPUFACE

CPUFace is a simple CPU Governor and Monitor for Unix Systems

![CPUFace Screenshot](https://image.ibb.co/ftJsXa/Screenshot_0607_1426.png)

### What it does?

Its a simple Qt interface for the system CPU Frequency control.

With CPUFace you can:

- Monitor your CPU Frequency and Governor
- Set new governor for specific CPU
- Add and manage CPU profiles
- Switch a CPU on/off ondemand

You can just call it from your command line with the command `cpuface` or trought your desktop manager menu.

### Dependencies

CPUFace is written in [Python 3](http://python.org) and [Qt5](http://doc.qt.io/qt-5/).

CPUFace uses a helper written in C to allow unprivileged users to change CPU settings. This helper needs a C compiler to compile and libc.

Theres no dependency for KDE or Plasma, this is a pure Qt application.

### Supported Systems

CPUFace is compatible with any Linux System that uses CPUFreq to control CPU frequency. So its compatible with `intel-pstate`, `acpi-cpufreq`, `powernow-k8` and others.

We plan to add support for FreeBSD systems in the future.

### Installation

#### Arch Linux Users

CPUFace is available for Arch Users trought AUR [here](https://aur.archlinux.org/packages/cpuface-git/).

If you have `yaourt` or any similar tool you can install CPUFace by one command. Example:

```sh
yaourt -S cpuface-git
```

#### Other Users

The installation process of CPUFace is really easy, it came with installation scripts. You can follow this steps:

##### Install dependencies

- Python (at leats 3.0)
- Python Qt5 Bindings
- gcc (or any C compiler)
- libc (or compatible)
- make
- git

##### Clone this repository to a specific directory

```sh
git clone https://github.com/h0m3/cpuface ~/cpuface
cd ~/cpuface
```

##### Compile all necessary files using make

```sh
make
```

##### Install the package (administrator rights needed)

```sh
sudo make install
```

##### (optional) Clean all unused packages from repository and remove it

```sh
make clean
cd ~
rm -r ~/cpuface
```

If you want to uninstall CPUFace, you can just run `sudo make uninstall`.

### Roadmap

Right now our focus is to Test CPUFace and fix bugs. We are also focused on adding support for FreeBSD.

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
