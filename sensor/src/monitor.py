import subprocess
import os
import sys
import logging


def is_monitoring(interface):
    network_interfaces = os.listdir('/sys/class/net/')
    if interface not in network_interfaces:
        return False
    return True


def start_monitoring(interface):
    try:
        return subprocess.call(['startmon'])
    except OSError:
        # this envvar will be set in the init.d script if running as a service
        return subprocess.call([os.path.join(os.getenv('WIFIBIN', ''), 'startmon')])
