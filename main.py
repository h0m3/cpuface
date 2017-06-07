#!/usr/bin/env python
# CPUFace - A CPU governor control for unix systems
# Copyright (C) 2017 Artur Paiva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

try:
    from PyQt5.QtWidgets import QApplication
except ModuleNotFoundError:
    print("[CPUFace] Missing PyQt5 module, you may need to install Python Qt5")
    quit(2)

import cpuface
from sys import version, version_info, argv


def show_help():
    print("Usage: %s" % argv[0])
    print("\nCPUFace is a manager for your CPU, you can set and monitor speed, status and governor.\n")
    print("Qt Arguments:")
    print(" --style=[style]\t\tSets the application GUI style. Possible values depend on your system configuration.")
    print(" --stylesheet=[sheet]\t\tSets the application styleSheet.")
    print(" --widgetcount\t\t\tPrints debug message at the end about number of widgets left undestroyed.")
    print(" --reverse\t\t\tSets the application's layout direction to RightToLeft.")
    print(" --qmljsdebugger=[port]\t\tActivates the QML/JS debugger with a specified port.")
    print()
    quit(0)


if __name__ == "__main__":
    if version_info[0] < 3:
        print("[CPUFace] Python 3 is required to run CPUFace, your Python version is outdated (%s)" % version)
        quit(3)
    if len(argv) > 1 and (argv[1] == "--help" or argv[1] == "-h"):
        show_help()
    app = QApplication(argv)
    window = cpuface.Cpuface()
    quit(app.exec_())
