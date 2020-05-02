import sys
import os
import subprocess
from plumbum import cli

class MistbornWifi(cli.Application):
    """
    Simple management for Access Point.
    """
    def main(self):
        """
        Main function for Mistborn managing Access Point.
        """
        wifi_ifaces = subprocess.check_output('iwconfig 2>/dev/null | grep -e "^\w" | awk \'{print $1}\'', shell=True).decode().strip() 
        print(f"WIFI ifaces: {wifi_ifaces}")

