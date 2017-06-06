"""
    This module shows the CPU Face UI
    And add specific function
"""

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
import cpu_get
# import cpu_set


class Cpuface(QDialog):

    def __init__(self):
        super(Cpuface, self).__init__()
        loadUi('cpuface.ui', self)
        self.cpuinfo = cpu_get.get_cpu_info()

        cont = 0
        for cpu in self.cpuinfo:
            self.sel_cpu.addItem("CPU %d: %s" % (cont, cpu["name"]))
            cont += 1

        self.update_cpu_info()
        self.sel_cpu.currentIndexChanged.connect(self.update_cpu_info)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(2000)

        self.show()

    def update_speed(self):
        cpu = self.sel_cpu.currentIndex()
        self.lab_speed.setText(str(cpu_get.get_speed(cpu)))

    def update_cpu_info(self):
        cpu = self.sel_cpu.currentIndex()

        self.check_online.setEnabled(False)
        self.sel_governor.setEnabled(False)
        self.val_speed.setEnabled(False)

        # Define CPU OnLine Status
        self.check_online.setEnabled(cpu is not 0)
        self.check_online.setChecked(cpu_get.is_online(cpu))

        # Define CPU Governor
        self.sel_governor.clear()
        for gov in cpu_get.get_governors(cpu):
            self.sel_governor.addItem(gov)
        index = self.sel_governor.findText(cpu_get.get_governor(cpu))
        if index is not -1:
            self.sel_governor.setCurrentIndex(index)
        self.sel_governor.setEnabled(cpu_get.is_online(cpu))

        # Define CPU speed
        self.val_speed.setMinimum(cpu_get.get_min_speed(cpu))
        self.val_speed.setMaximum(cpu_get.get_max_speed(cpu))
        self.val_speed.setValue(cpu_get.get_speed(cpu))
        self.val_speed.setEnabled(cpu_get.is_online(cpu) and (self.sel_governor.currentText() == "userspace"))

        # Define other CPU information
        self.lab_driver.setText(self.cpuinfo[cpu]["driver"])
        self.lab_vendor.setText(self.cpuinfo[cpu]["vendor"])
        self.lab_cpu_id.setText(self.cpuinfo[cpu]["id"])
        self.lab_core_id.setText(self.cpuinfo[cpu]["core"])
        self.lab_speed.setText(str(cpu_get.get_speed(cpu)))
        self.lab_cache.setText(str(self.cpuinfo[cpu]["cache"]))
    #
    # def set_cpu_ui(self):
    #     """
    #         This function enable or disable a CPU based on UI calls
    #     """
    #     cpu = self.sel_cpu.currentIndex()
    #     enabled = self.check_enabled.isChecked()
    #     rs = set_enabled(cpu, enabled)
    #     if rs[0] is not 0:
    #         msg = QMessageBox(self)
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setText("CPUFace was unable to update this CPU Status\n\nError Code: %d" % rs[0])
    #         msg.setDetailedText(rs[1])
    #         msg.setWindowTitle("Unable to update CPU Status")
    #         msg.setStandardButtons(QMessageBox.Close)
    #         msg.exec_()
    #     enabled = is_enabled(cpu)
    #     self.check_enabled.setChecked(enabled)
    #     self.sel_governor.setEnabled(enabled)
    #     self.val_speed.setEnabled(enabled and (self.sel_governor.currentText() == "userspace"))
    #
    # def set_governor_ui(self):
    #     """
    #         This function set CPU governor
    #     """
    #     cpu = self.sel_cpu.currentIndex()
    #     governor = self.sel_governor.currentText()
    #     rs = set_governor(cpu, governor)
    #     print(governor)
    #     if rs[0] is not 0:
    #         msg = QMessageBox(self)
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setText("CPUFace was unable to update CPU Governor\n\nError Code: %d" % rs[0])
    #         msg.setDetailedText(rs[1])
    #         msg.setWindowTitle("Unable to update CPU Governor")
    #         msg.setStandardButtons(QMessageBox.Close)
    #         msg.exec_()
    #     self.update_governor()
    #     self.val_speed.setEnabled(self.check_enabled.isChecked() and (self.sel_governor.currentText() == "userspace"))
    #
    # def set_speed_ui(self):
    #     """
    #         This function set CPU speed
    #     """
    #     cpu = self.sel_cpu.currentIndex()
    #     speed = self.val_speed.value()
    #     rs = set_speed(cpu, speed)
    #     if rs[0] is not 0:
    #         msg = QMessageBox(self)
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setText("CPUFace was unable to update CPU Speed\n\nError Code: %d" % rs[0])
    #         msg.setDetailedText(rs[1])
    #         msg.setWindowTitle("Unable to update CPU Speed")
    #         msg.setStandardButtons(QMessageBox.Close)
    #         msg.exec_()
    #
    # def update_cpu(self):
    #     """
    #         Update CPU information based on selected CPU
    #     """
    #
    #     self.sel_governor.currentIndexChanged.disconnect()
    #     self.check_enabled.stateChanged.disconnect()
    #     self.val_speed.valueChanged.disconnect()
    #
    #     cpu = self.sel_cpu.currentIndex()
    #     if cpu is 0:
    #         self.check_enabled.setEnabled(False)
    #     else:
    #         self.check_enabled.setEnabled(True)
    #     self.check_enabled.setChecked(is_enabled(cpu))
    #
    #     self.sel_governor.clear()
    #     c = 0
    #     for gov in get_governors(cpu):
    #         self.sel_governor.insertItem(c, gov)
    #         c += 1
    #
    #     self.val_speed.setMinimum(get_min_speed(cpu))
    #     self.val_speed.setMaximum(get_max_speed(cpu))
    #     self.val_speed.setValue(get_speed(cpu))
    #     self.lab_driver.setText(get_driver(cpu))
    #     self.lab_vendor.setText(self.cpuinfo[cpu]["vendor_id"])
    #     self.cpu_id.setText(self.cpuinfo[cpu]["physical id"])
    #     self.core_id.setText(self.cpuinfo[cpu]["core id"])
    #     self.lab_cache.setText(self.cpuinfo[cpu]["cache size"])
    #     self.update_governor()
    #
    #     self.val_speed.valueChanged.connect(self.set_speed_ui)
    #     self.check_enabled.stateChanged.connect(self.set_cpu_ui)
    #     self.sel_governor.currentIndexChanged.connect(self.set_governor_ui)
    #
    # def update_governor(self):
    #     """
    #         Update governor information
    #     """
    #
    #     cpu = self.sel_cpu.currentIndex()
    #
    #
    #     index = self.sel_governor.findText(get_governor(cpu))
    #     if index is not -1:
    #         self.sel_governor.setCurrentIndex(index)
