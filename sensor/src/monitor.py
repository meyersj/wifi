import subprocess
import os


def is_monitoring(interface):
    network_interfaces = os.listdir('/sys/class/net/')
    if interface not in network_interfaces:
        return False
    return True


def start_monitoring(interface):
    return subprocess.call(['startmon'])
