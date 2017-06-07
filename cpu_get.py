"""
    This module gets CPU information from the system
    to populate and update the GUI
"""

# TODO: Support for FreeBSD

from os import listdir


def read_file(path):
    try:
        buf = open(path, "r")
        r = buf.readlines()
        buf.close()
        return r
    except (OSError, IOError) as err:
        print("[CPUFace] Unable to read '%s': %s" % (path, err.strerror))
        return None


def driver(cpu=0):
    r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_driver" % cpu)
    if r is None:
        return "Unknown"
    else:
        return r[0][:-1]


def cpu_info():
    cpuinfo = list()

    # Append all CPUs to the list
    try:
        cpus = listdir("/sys/devices/system/cpu/cpufreq")
        for cpu in cpus:
            if "policy" in cpu:
                cpu = dict()
                cpu["name"] = "Disabled"
                cpu["id"] = "unknown"
                cpu["core"] = "unknown"
                cpu["vendor"] = "unknown"
                cpu["cache"] = 0
                cpu["driver"] = driver(len(cpuinfo))
                cpuinfo.append(cpu)
    except (OSError, IOError) as err:
        print("[CPUFace] Unable to get CPU information")
        exit(2)

    r = read_file("/proc/cpuinfo")
    if r is not None:
        processor = None
        cpu = dict()
        for line in r:
            if "processor" in line:
                if processor is not None:
                    cpuinfo[processor] = cpu
                processor = int(line.split(":")[1])
                cpu = cpuinfo[processor]
            elif "model name" in line:
                cpu["name"] = line.split(":")[1][1:-1]
            elif "physical id" in line:
                cpu["id"] = line.split(":")[1][1:-1]
            elif "core id" in line:
                cpu["core"] = line.split(":")[1][1:-1]
            elif "cache size" in line:
                cpu["cache"] = int(line.split(":")[1].replace("KB", ""))
            elif "vendor_id" in line:
                cpu["vendor"] = line.split(":")[1][1:-1]
        cpuinfo[processor] = cpu

    return cpuinfo


def online(cpu=0):
    if cpu is 0:
        return True
    r = read_file("/sys/devices/system/cpu/cpu%d/online" % cpu)
    return (r is None) or (r[0][:-1] == '1')


def governor(cpu=0):
    if online(cpu):
        r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor" % cpu)
        if r is None:
            return "Unknown"
        else:
            return r[0][:-1]
    else:
        return "Disabled"


def speed(cpu=0):
    if online(cpu):
        r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq" % cpu)
        if r is None:
            return 0
        else:
            return int(int(r[0]) / 1000)
    else:
        return 0


def min_speed(cpu=0):
    if online(cpu):
        r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_min_freq" % cpu)
        if r is None:
            return 0
        else:
            return int(int(r[0]) / 1000)
    else:
        return 0


def max_speed(cpu=0):
    if online(cpu):
        r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_max_freq" % cpu)
        if r is None:
            return 0
        else:
            return int(int(r[0]) / 1000)
    else:
        return 0


def governors(cpu=0):
    if online(cpu):
        r = read_file("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_available_governors" % cpu)
        if r is None:
            return [governor(cpu)]
        else:
            return r[0][:-1].split(" ")
    else:
        return [governor(cpu)]
