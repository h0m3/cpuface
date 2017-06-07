"""
    Show CPU governor and speed information
    Set CPU governor and speed
"""

from subprocess import check_output, STDOUT, CalledProcessError
import cpu_get


def run_command(command):
    try:
        return (0, check_output(command.split(" "), stderr=STDOUT).decode())
    except CalledProcessError as err:
        print("[CPUFace] Unable to change CPU information")
        return (err.returncode, err.output.decode())
    except OSError as err:
        print("[CPUFace] Unable to change CPU information")
        return (err.errno, err.strerror)


def governor(cpu=0, governor="powersave"):
    if not(cpu_get.online(cpu)) or (cpu_get.governor(cpu) == governor):
        return (0, None)
    return run_command("cpuface_helper %d governor %s" % (cpu, governor))


def online(cpu=0, online=True):
    if cpu_get.online(cpu) == online:
        return (0, None)
    if online:
        return run_command("cpuface_helper %d online" % cpu)
    else:
        return run_command("cpuface_helper %d offline" % cpu)


def speed(cpu=0, speed=800):
    if not(cpu_get.online(cpu)) or (cpu_get.speed(cpu) == speed):
        return (0, None)
    return run_command("cpuface_helper %d speed %d" % (cpu, speed * 1000))
