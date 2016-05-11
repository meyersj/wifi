""" utility functions for working with network interfaces """


import os
import socket
import fcntl
import struct
import time
import subprocess


def get_mac_address(ifname):
    """
    get hardware address from network interface name

    source: https://gist.github.com/zhenyi2697/6080400
    """
    if not is_available(ifname):
        return False
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(sock.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]


def is_available(ifname):
    """ check if interface provided by name exists """
    network_interfaces = os.listdir('/sys/class/net/')
    if ifname not in network_interfaces:
        return False
    return True


def channel_hopper(ifname):
    """ hop between all channels on provided interface """
    while True:
        for channel in range(1, 12):
            cmd = ['sudo', 'iwconfig', ifname, 'channel', str(channel)]
            ret = subprocess.call(cmd)
            if ret == 0:
                time.sleep(1)
            else:

                time.sleep(10)
