"""
    Show CPU governor and speed information
    Set CPU governor and speed
"""

from subprocess import check_output, STDOUT, CalledProcessError
from cpu_info import is_enabled, get_governor


def set_online(cpu=0, enable=True):
    """
        Enable or disable selected CPU
    """
    if is_enabled() == enable:
        return (0, None)

    try:
        if enable:
            return (0, check_output(["cpuface_helper", "%d" % cpu, "enable"], stderr=STDOUT).decode())
        else:
            return (0, check_output(["cpuface_helper", "%d" % cpu, "disable"], stderr=STDOUT).decode())
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.returncode, err.output.decode())
    except OSError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.errno, err.strerror)


def set_governor(cpu=0, governor="powersave"):
    """
        Set governor for a specific CPU
    """
    if get_governor() == governor:
        return (0, None)

    try:
        return (0, check_output(["cpuface_helper", "%d" % cpu, "governor", governor], stderr=STDOUT).decode())
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.returncode, err.output.decode())
    except OSError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.errno, err.strerror)


def set_speed(cpu=0, speed=800):
    """
        Set speed for a given CPU
    """
    if get_speed() == speed:
        return (0, None)

    try:
        return (0, check_output(["cpuface_helper", "%d" % cpu, "speed" "%d" % speed * 1000], stderr=STDOUT).decode())
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.returncode, err.output.decode())
    except OSError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.errno, err.strerror)
