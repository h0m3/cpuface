"""
    This module shows the CPU Face UI
    And add specific function
"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from cpu_info import *


class Cpuface(QDialog):

    def __init__(self):
        super(Cpuface, self).__init__()
        loadUi('cpuface.ui', self)
        self.cpuinfo = get_cpu_info()

        c = 0
        for cpu in self.cpuinfo:
            self.sel_cpu.insertItem(c, "CPU %d: %s" % (c, cpu["model name"]))
            c += 1

        self.check_enabled.stateChanged.connect(self.set_cpu_enabled)
        self.sel_governor.currentIndexChanged.connect(self.set_governor_props)
        self.sel_cpu.currentIndexChanged.connect(self.update_cpu)
        self.update_cpu()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_governor)
        self.timer.start(2000)

    def set_cpu_enabled(self):
        """
            This function adapt the GUI for when the CPU is enabled or disabled
        """

        enabled = self.check_enabled.isChecked()
        self.sel_governor.setEnabled(enabled)
        self.val_speed.setEnabled(enabled and (self.sel_governor.currentText() == "userspace"))

    def set_governor_props(self):
        """
            This function enables the CPU frequency scalator whe "userspace" is used

        """

        self.val_speed.setEnabled(self.check_enabled.isChecked() and (self.sel_governor.currentText() == "userspace"))

    def update_cpu(self):
        """
            Update CPU information based on selected CPU
        """

        cpu = self.sel_cpu.currentIndex()
        if cpu is 0:
            self.check_enabled.setEnabled(False)
        else:
            self.check_enabled.setEnabled(True)
        self.check_enabled.setChecked(is_enabled(cpu))

        self.sel_governor.clear()
        c = 0
        for gov in get_governors(cpu):
            self.sel_governor.insertItem(c, gov)
            c += 1

        self.val_speed.setMinimum(get_min_speed(cpu))
        self.val_speed.setMaximum(get_max_speed(cpu))
        self.val_speed.setValue(get_speed(cpu))
        self.lab_driver.setText(get_driver(cpu))
        self.lab_vendor.setText(self.cpuinfo[cpu]["vendor_id"])
        self.cpu_id.setText(self.cpuinfo[cpu]["physical id"])
        self.core_id.setText(self.cpuinfo[cpu]["core id"])
        self.lab_cache.setText(self.cpuinfo[cpu]["cache size"])

        self.update_governor()

    def update_governor(self):
        """
            Update governor information
        """

        cpu = self.sel_cpu.currentIndex()

        self.lab_speed.setText(str(get_speed(cpu)))
        index = self.sel_governor.findText(get_governor())
        if index is not -1:
            self.sel_governor.setCurrentIndex(index)
