"""
    This module shows the CPU Face UI
    And add specific function
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from os import path
import cpu_get
import cpu_set
import profiles


class Cpuface(QDialog):

    def __init__(self):
        super(Cpuface, self).__init__()
        data = path.dirname(__file__)
        loadUi(path.realpath(data+'/cpuface.ui'), self)

        self.profiles = profiles.load_profiles()
        self.update_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

        self.show()

    def closeEvent(self, event):
        profiles.save_profiles(self.profiles)

    def update_speed(self):
        self.lab_speed.setText(str(cpu_get.speed(self.cpu)))

    def update_ui(self):
        # Disable all unwanted calls
        try:
            self.sel_profile.currentIndexChanged.disconnect()
            self.sel_cpu.currentIndexChanged.disconnect()
            self.check_online.stateChanged.disconnect()
            self.sel_governor.currentIndexChanged.disconnect()
            self.val_speed.valueChanged.disconnect()
            self.btn_new.clicked.disconnect()
            self.btn_save.clicked.disconnect()
            self.btn_remove.clicked.disconnect()
        except TypeError:
            pass

        # Disable all options
        self.sel_profile.setEnabled(False)
        self.sel_cpu.setEnabled(False)
        self.check_online.setEnabled(False)
        self.sel_governor.setEnabled(False)
        self.val_speed.setEnabled(False)
        self.btn_new.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_remove.setEnabled(False)

        # Update profile selection
        prof_index = self.sel_profile.currentIndex()
        if prof_index == -1:
            prof_index = 0
        self.sel_profile.clear()
        self.sel_profile.addItem("No profile")
        for profile in self.profiles:
            self.sel_profile.addItem(profile)
        self.sel_profile.setCurrentIndex(prof_index)
        self.sel_profile.currentIndexChanged.connect(self.set_profile)
        self.sel_profile.setEnabled(True)

        # Update CPU selection
        self.cpuinfo = cpu_get.cpu_info()
        self.cpu = self.sel_cpu.currentIndex()
        if self.cpu == -1:
            self.cpu = 0
        self.sel_cpu.clear()
        for i, cpu in enumerate(self.cpuinfo):
            self.sel_cpu.addItem("CPU %d: %s" % (i, cpu["name"]))
        self.sel_cpu.setCurrentIndex(self.cpu)
        self.sel_cpu.currentIndexChanged.connect(self.update_ui)
        self.sel_cpu.setEnabled(True)

        # Update current CPU status
        self.check_online.setChecked(cpu_get.online(self.cpu))
        self.check_online.stateChanged.connect(self.set_online)
        self.check_online.setEnabled(self.cpu is not 0)

        # Update current CPU governor
        self.sel_governor.clear()
        for governor in cpu_get.governors(self.cpu):
            self.sel_governor.addItem(governor)
        self.sel_governor.setCurrentIndex(self.sel_governor.findText(cpu_get.governor(self.cpu)))
        self.sel_governor.currentIndexChanged.connect(self.set_governor)
        self.sel_governor.setEnabled(cpu_get.online(self.cpu))

        # Update current speed
        self.val_speed.setMinimum(cpu_get.min_speed(self.cpu))
        self.val_speed.setMaximum(cpu_get.max_speed(self.cpu))
        self.val_speed.setValue(cpu_get.speed(self.cpu))
        self.val_speed.valueChanged.connect(self.set_speed)
        self.val_speed.setEnabled(cpu_get.online(self.cpu) and (self.sel_governor.currentText() == "userspace"))

        # Update additional information
        self.lab_driver.setText(self.cpuinfo[self.cpu]["driver"])
        self.lab_vendor.setText(self.cpuinfo[self.cpu]["vendor"])
        self.lab_cpu_id.setText(self.cpuinfo[self.cpu]["id"])
        self.lab_core_id.setText(self.cpuinfo[self.cpu]["core"])
        self.lab_cache.setText(str(self.cpuinfo[self.cpu]["cache"]))

        # Update buttons action
        self.btn_new.clicked.connect(self.new_profile)
        self.btn_new.setEnabled(True)
        if self.sel_profile.currentText() != "No profile":
            self.btn_save.clicked.connect(self.save_profile)
            self.btn_save.setEnabled(True)
            self.btn_remove.clicked.connect(self.remove_profile)
            self.btn_remove.setEnabled(True)

    def detect_error(self, result):
        if result[0] != 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unable to update CPU Status\n\nError Code: %d" % result[0])
            msg.setDetailedText(result[1])
            msg.setWindowTitle("Unable to update CPU Status")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec_()

    def set_online(self):
        self.detect_error(cpu_set.online(self.cpu, self.check_online.isChecked()))
        self.update_ui()

    def set_governor(self):
        self.detect_error(cpu_set.governor(self.cpu, self.sel_governor.currentText()))
        self.update_ui()

    def set_speed(self):
        self.detect_error(cpu_set.speed(self.cpu, self.val_speed.value()))
        self.update_cpu()

    def new_profile(self):
        input_name = QInputDialog(self)
        input_name.setLabelText("Profile Name")
        input_name.setOkButtonText("Create")
        input_name.exec_()
        name = input_name.textValue()

        if name != '':
            self.save_profile(name)

    def save_profile(self, name=None):
        if type(name) is bool or name is None:
            name = self.sel_profile.currentText()

        self.profiles[name] = list()
        for cpu in range(0, len(self.cpuinfo)):
            self.profiles[name].append(dict())
            self.profiles[name][cpu]["online"] = cpu_get.online(cpu)
            if cpu_get.online(cpu):
                self.profiles[name][cpu]["governor"] = cpu_get.governor(cpu)
            else:
                self.profiles[name][cpu]["governor"] = None
            if cpu_get.governor(cpu) == "userspace":
                self.profiles[name][cpu]["speed"] = cpu_get.speed(cpu)
            else:
                self.profiles[name][cpu]["speed"] = None
        self.update_ui()
        self.sel_profile.setCurrentIndex(self.sel_profile.findText(name))

    def remove_profile(self):
        del self.profiles[self.sel_profile.currentText()]
        self.update_ui()
        self.sel_profile.setCurrentIndex(0)

    def set_profile(self):
        if self.sel_profile.currentIndex() > 0:
            profile = self.sel_profile.currentText()
            for cpu in range(0, len(self.cpuinfo)):
                cpu_set.online(cpu, self.profiles[profile][cpu]["online"])
                if self.profiles[profile][cpu]["governor"] is not None:
                    cpu_set.governor(cpu, self.profiles[profile][cpu]["governor"])
                if self.profiles[profile][cpu]["speed"] is not None:
                    cpu_set.speed(cpu, self.profiles[profile][cpu]["speed"])
        self.update_ui()
