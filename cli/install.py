import sys
import os
import subprocess
from plumbum import cli

class MistbornInstall(cli.Application):
    """
    Subcommand for installation and customization
    """

    def main(self):
        """
        Main function for Mistborn installation
        """
        print("mistborn-cli: install")

    
    def docker(self):
        """
        Install docker and docker compose
        """
        subprocess.check_output("ansible-playbook -i localhost playbooks/docker.yml", shell=True)
