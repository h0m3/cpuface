"""
    This module gets CPU information from the system
    to populate and update the GUI
"""

# TODO: Support for FreeBSD

from os import listdir


def driver(cpu=0):
    """
        Get CPU current frequency driver
    """

    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_driver" % cpu, "r")
        r = buf.readline()
        buf.close()
        return r[:-1]
    except (OSError, IOError) as err:
        print("[CPUFace] Error while getting CPU Governor Driver: %s" % err)
        return "unknown"


def cpu_info():
    """
        Get and organize CPU information
    """

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

    # Add specific information about each cpu
    try:
        buf = open("/proc/cpuinfo", "r")
        processor = None
        cpu = dict()

        for line in buf.readlines():
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

        buf.close()
    except (IOError, OSError) as err:
        print("[CPUFace] Error while getting CPU online information: %s" % err)

    return cpuinfo


def online(cpu=0):
    """
        Return if the CPU is enabled
    """
    if cpu is 0:
        return True
    try:
        buf = open("/sys/devices/system/cpu/cpu%d/online" % cpu, "r")
        r = buf.readline()[0] == '1'
        buf.close()
        return r
    except (OSError, IOError) as err:
        print("[CPUFace] Error while getting CPU online information: %s" % err)
        return True


def governor(cpu=0):
    """
        Return the current governor for a given CPU
    """
    if online(cpu):
        try:
            buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor" % cpu, "r")
            r = buf.readline()[:-1]
            buf.close()
            return r
        except (OSError, IOError) as err:
            print("[CPUFace] Error while getting CPU governor information: %s" % err)
            return "unknown"
    else:
        return "disabled"


def speed(cpu=0):
    """
        Get given CPU current speed in MHz
    """
    if online(cpu):
        try:
            buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq" % cpu, "r")
            r = int(int(buf.readline()) / 1000)
            buf.close()
            return r
        except (OSError, IOError, ValueError) as err:
            print("[CPUFace] Error while getting CPU speed: %s" % err)
            return 0
    else:
        return 0


def min_speed(cpu=0):
    """
        Get given CPU minimum speed in MHz
    """
    if online(cpu):
        try:
            buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_min_freq" % cpu, "r")
            r = int(int(buf.readline()) / 1000)
            buf.close()
            return r
        except (OSError, IOError, ValueError) as err:
            print("[CPUFace] Error while getting CPU minimum speed: %s" % err)
            return 0
    else:
        return 0


def max_speed(cpu=0):
    """
        Get given CPU maximum speed in MHz
    """
    if online(cpu):
        try:
            buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_max_freq" % cpu, "r")
            r = int(int(buf.readline()) / 1000)
            buf.close()
            return r
        except (OSError, IOError, ValueError) as err:
            print("[CPUFace] Error while getting CPU minimum speed: %s" % err)
            return 0
    else:
        return 0


def governors(cpu=0):
    """
        Get a list of all available governors
    """
    if online(cpu):
        try:
            buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_available_governors" % cpu, "r")
            r = buf.readline()[:-1].split(" ")
            buf.close()
            return r
        except (OSError, IOError, ValueError) as err:
            print("[CPUFace] Error while getting CPU available governors: %s" % err)
            return [governor(cpu)]
    else:
        return [governor(cpu)]
