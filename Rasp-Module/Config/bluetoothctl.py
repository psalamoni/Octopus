# Based on ReachView code from Egor Fedorov (egor.fedorov@emlid.com)
# Updated for Python 3.6.8 on a Raspberry  Pi


import time
import pexpect


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        self.process = pexpect.spawnu("sudo bluetoothctl")
        self.send("agent on")
        self.send("default-agent")

    def send(self, command, pause=0):
        self.process.send(f"{command}\n")
        time.sleep(pause)

    def start_scan(self):
        """Start bluetooth scanning process."""
        self.send("scan on", 3)

    def make_discoverable(self):
        """Make device discoverable."""
        self.send("discoverable on")

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        if not any(keyword in info_string for keyword in block_list):
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2],
                    }
        return device

    def pair(self, mac_address, psswd):
        """Try to pair with a device by mac address."""
        self.send(f"pair {mac_address}\n{psswd}")

    def trust(self, mac_address):
        self.send(f"trust {mac_address}")

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        self.send(f"remove {mac_address}")
        
    def sp_init(self, mac_address):
        """Bind bt device specified in mac_address to /dev/rfcomm0 port"""
        self._secondary = pexpect.spawnu("sudo rfcomm bind /dev/rfcomm0 " + mac_address + " 1")