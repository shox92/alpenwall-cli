import sys
import re
import os
import subprocess
from plumbum import cli

def get_wg_ifs():
    return subprocess.check_output("sudo wg show interfaces", shell=True).decode('utf-8').strip().split(" ")

def get_wg_confs():
    rawfnames = [os.path.basename(x).split('.')[0] for x in subprocess.check_output("sudo find /etc/wireguard -maxdepth 1 -type f", shell=True).decode('utf-8').strip().split('\n')]

    return [re.sub(r'\W+', '', fname) for fname in rawfnames if fname == re.sub(r'\W+', '', fname)]

class WGApp(cli.Application):
    """
    WireGuard App for AlpenWall
    """

    def main(self):
        pass


@WGApp.subcommand("ensureon")
class WGEnsureOn(cli.Application):
    """
    Ensure all WireGuard interfaces exist
    """

    def main(self):
        """
        WGEnsureOn main method
        """

        active_ifaces = get_wg_ifs()
        for iface in get_wg_confs():
            if iface not in active_ifaces:
                subprocess.run(f"sudo systemctl restart wg-quick@{iface}", shell=True)


