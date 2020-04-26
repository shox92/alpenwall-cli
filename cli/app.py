import sys
import os
import subprocess
from plumbum import cli

class MistbornApp(cli.Application):

    def main(self):
        """
        Main function for the Mistborn CLI
        """
        print('test')



if __name__ == "__main__":
    MistbornApp.run()
