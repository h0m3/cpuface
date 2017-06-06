"""
    Show CPU governor and speed information
    Set CPU governor and speed
"""

from subprocess import call, STDOUT, CalledProcessError


def set_enabled(cpu=0, enable=True):
    """
        Enable or disable selected CPU
    """
    try:
        if enable:
            return (0, call(["cpuface-helper", "%d" % cpu, "enable"], stderr=STDOUT))
        else:
            return (0, call(["cpuface-helper", "%d" % cpu, "disable"], stderr=STDOUT))
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU state")
        return (err.returncode, err.output)


def set_governor(cpu=0, governor="powersave"):
    """
        Set governor for a specific CPU
    """
    try:
        return (0, call(["cpuface-helper", "%d" % cpu, "governor", governor], stderr=STDOUT))
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU state")


def set_speed(cpu=0, speed=800):
    """
        Set speed for a given CPU
    """
    try:
        return (0, call(["cpuface-helper", "%d" % cpu, "speed" "%d" % speed * 1000], stderr=STDOUT))
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU speed")
