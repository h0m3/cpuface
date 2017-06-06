"""
    This module gets CPU information from the system
    to populate and update the GUI
"""

# TODO: Support for FreeBSD


def get_cpu_info():
    """
        Get and organize CPU information
        from Linux /proc/cpuinfo
    """

    try:
        buf = open("/proc/cpuinfo", "r")
        cpuinfo = list()
        cpu = None

        for line in buf.readlines():
            if "processor" in line:
                cpuinfo.append(cpu)
                cpu = dict()
            else:
                line = line.replace('\t', '').strip().split(':')
                if len(line) is 2:
                    if line[1] is '':
                        cpu[line[0]] = None
                    else:
                        cpu[line[0]] = line[1][1:]
        cpuinfo.append(cpu)

        buf.close()
        return cpuinfo[1:]
    except (IOError, OSError) as err:
        print("[CPUFace] Error while getting CPU online information: %s" % err)
        return None


def is_enabled(cpu=0):
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


def get_governor(cpu=0):
    """
        Return the current governor for a given CPU
    """
    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor" % cpu, "r")
        r = buf.readline()
        buf.close()
        return r
    except (OSError, IOError) as err:
        print("[CPUFace] Error while getting CPU governor information: %s" % err)
        return None


def get_speed(cpu=0):
    """
        Get given CPU current speed in MHz
    """

    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_cur_freq" % cpu, "r")
        r = int(int(buf.readline()) / 1000)
        buf.close()
        return r
    except (OSError, IOError, ValueError) as err:
        print("[CPUFace] Error while getting CPU speed: %s" % err)
        return 0


def get_min_speed(cpu=0):
    """
        Get given CPU minimum speed in MHz
    """

    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_min_freq" % cpu, "r")
        r = int(int(buf.readline()) / 1000)
        buf.close()
        return r
    except (OSError, IOError, ValueError) as err:
        print("[CPUFace] Error while getting CPU minimum speed: %s" % err)
        return 0


def get_max_speed(cpu=0):
    """
        Get given CPU maximum speed in MHz
    """

    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_max_freq" % cpu, "r")
        r = int(int(buf.readline()) / 1000)
        buf.close()
        return r
    except (OSError, IOError, ValueError) as err:
        print("[CPUFace] Error while getting CPU minimum speed: %s" % err)
        return 0


def get_governors(cpu=0):
    """
        Get a list of all available governors
    """

    try:
        buf = open("/sys/devices/system/cpu/cpu%d/cpufreq/scaling_available_governors" % cpu, "r")
        r = buf.readline().split(" ")
        buf.close()
        return r
    except (OSError, IOError, ValueError) as err:
        print("[CPUFace] Error while getting CPU available governors: %s" % err)
        return [get_governor()]


def get_driver(cpu=0):
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
