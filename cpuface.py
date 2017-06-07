"""
    This module shows the CPU Face UI
    And add specific function
"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
import cpu_get
import cpu_set
import profiles


class Cpuface(QDialog):

    def __init__(self):
        super(Cpuface, self).__init__()
        loadUi('cpuface.ui', self)
        self.cpuinfo = cpu_get.cpu_info()
        self.profiles = profiles.load_profiles()

        cont = 0
        for cpu in self.cpuinfo:
            self.sel_cpu.addItem("CPU %d: %s" % (cont, cpu["name"]))
            cont += 1

        self.update_profiles()
        self.update_cpu()
        self.sel_cpu.currentIndexChanged.connect(self.update_cpu)
        self.btn_new.clicked.connect(self.new_profile)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(1000)

        self.show()

    def new_profile(self):
        self.btn_remove.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_new.setEnabled(False)
        self.sel_profile.setEnabled(False)

        input_name = QInputDialog(self)
        input_name.setLabelText("Profile Name")
        input_name.setOkButtonText("Create")
        input_name.exec_()
        name = input_name.textValue()

        if name != '':
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
            self.update_profiles()
            self.sel_profile.setCurrentIndex(self.sel_profile.findText(name))

    def update_profile(self):
        self.btn_remove.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_new.setEnabled(False)
        self.sel_profile.setEnabled(False)

        profile = self.sel_profile.currentText()
        if profile != "No selected profile":
            for cpu in range(0, len(self.cpuinfo)):
                cpu_set.online(cpu, self.profiles[profile][cpu]["online"])
                if self.profiles[profile][cpu]["governor"] is not None:
                    cpu_set.governor(cpu, self.profiles[profile][cpu]["governor"])
                if self.profiles[profile][cpu]["speed"] is not None:
                    cpu_set.speed(cpu, self.profiles[profile][cpu]["speed"])
            self.btn_remove.setEnabled(True)
            self.btn_save.setEnabled(True)

        self.sel_profile.setEnabled(True)
        self.btn_new.setEnabled(True)
        self.update_cpu()

    def update_profiles(self, selected_profile=0):
        self.btn_save.setEnabled(False)
        self.btn_remove.setEnabled(False)
        self.btn_new.setEnabled(False)
        self.sel_profile.setEnabled(False)
        try:
            self.sel_profile.currentIndexChanged.disconnect()
        except TypeError:
            pass

        self.sel_profile.clear()
        self.sel_profile.addItem("No selected profile")
        for item in self.profiles:
            self.sel_profile.addItem(item)

        self.sel_profile.setCurrentIndex(selected_profile)
        self.update_profile()
        self.sel_profile.currentIndexChanged.connect(self.update_profile)

    def update_speed(self):
        self.lab_speed.setText(str(cpu_get.speed(self.cpu)))

    def update_cpu(self):

        # Disconnect all signals to update
        try:
            self.sel_governor.currentIndexChanged.disconnect()
            self.check_online.stateChanged.disconnect()
            self.val_speed.valueChanged.disconnect()
        except TypeError:
            pass

        self.cpu = self.sel_cpu.currentIndex()

        self.check_online.setEnabled(False)
        self.sel_governor.setEnabled(False)
        self.val_speed.setEnabled(False)

        # Define CPU OnLine Status
        self.check_online.setChecked(cpu_get.online(self.cpu))
        self.check_online.setEnabled(self.cpu is not 0)

        # Define CPU Governor
        self.sel_governor.clear()
        for gov in cpu_get.governors(self.cpu):
            self.sel_governor.addItem(gov)
        index = self.sel_governor.findText(cpu_get.governor(self.cpu))
        if index is not -1:
            self.sel_governor.setCurrentIndex(index)
        self.sel_governor.setEnabled(cpu_get.online(self.cpu))

        # Define CPU speed
        self.val_speed.setMinimum(cpu_get.min_speed(self.cpu))
        self.val_speed.setMaximum(cpu_get.max_speed(self.cpu))
        self.val_speed.setValue(cpu_get.speed(self.cpu))
        self.val_speed.setEnabled(cpu_get.online(self.cpu) and (self.sel_governor.currentText() == "userspace"))

        # Define other CPU information
        self.lab_driver.setText(self.cpuinfo[self.cpu]["driver"])
        self.lab_vendor.setText(self.cpuinfo[self.cpu]["vendor"])
        self.lab_cpu_id.setText(self.cpuinfo[self.cpu]["id"])
        self.lab_core_id.setText(self.cpuinfo[self.cpu]["core"])
        self.lab_speed.setText(str(cpu_get.speed(self.cpu)))
        self.lab_cache.setText(str(self.cpuinfo[self.cpu]["cache"]))

        # Connect all signals back again
        self.sel_governor.currentIndexChanged.connect(self.set_governor)
        self.check_online.stateChanged.connect(self.set_online)
        self.val_speed.valueChanged.connect(self.set_speed)

    def set_unable(self, result):
        if result[0] != 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unable to update CPU Status\n\nError Code: %d" % result[0])
            msg.setDetailedText(result[1])
            msg.setWindowTitle("Unable to update CPU Status")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec_()

    def set_governor(self):
        self.set_unable(cpu_set.governor(self.cpu, self.sel_governor.currentText()))
        self.update_cpu()

    def set_online(self):
        self.set_unable(cpu_set.online(self.cpu, self.check_online.isChecked()))
        self.cpuinfo = cpu_get.cpu_info()
        self.update_cpu()

    def set_speed(self):
        self.set_unable(cpu_set.speed(self.cpu, self.val_speed.value()))
        self.update_cpu()

    def closeEvent(self, event):
        profiles.save_profiles(self.profiles)
