import sys
import os
import subprocess
from plumbum import cli
        
def get_wifi_ifaces():
    return [iface.strip() for iface in subprocess.check_output('iwconfig 2>/dev/null | grep -e "^\w" | awk \'{print $1}\'', shell=True).decode().splitlines()]

class MistbornWifi(cli.Application):
    """
    Simple management for Access Point.
    """
    def main(self):
        """
        Main function for Mistborn managing Access Point.
        """
        wifi_ifaces = get_wifi_ifaces()
        print(f"WIFI ifaces: {wifi_ifaces}")

    def dependencies(self):
        """
        Install system dependencies.
        """
        # hostapd
        # stop and disable services
        os.system("sudo apt-get update && sudo apt-get install -y hostapd && sudo systemctl stop hostapd && sudo systemctl disable hostapd")
