"""
    Show CPU governor and speed information
    Set CPU governor and speed
"""

from subprocess import run

def set_enabled(cpu=0, enabled=True):
    """
        Enable or disable selected CPU
    """

def set_governor(cpu=0, governor="powersave"):
    try:
        call(["sudo", "cpuface-helper", "governor", "%s" % governor])


def set_speed(cpu=0, speed=800):
    try:
        call(["sudo", "cpuface-helper", "speed", "%d" % speed])
