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
