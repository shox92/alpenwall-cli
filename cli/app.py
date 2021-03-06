import sys
import os
import subprocess
from plumbum import cli

class MistbornApp(cli.Application):
    """
    Main CLI App for Mistborn
    """

    home_dir = cli.SwitchAttr("--home-dir", cli.ExistingFile,
                              help="The Mistborn home directory",
                              default=os.path.join('/','opt','mistborn'))
    
    compose_file = cli.SwitchAttr("--compose-file", cli.ExistingFile,
                                 help="The Docker Compose file to use",
                                 default=os.path.join(home_dir, "base.yml"))
    
    env_file = cli.SwitchAttr("--env-file", cli.ExistingFile,
                                 help="The environment variable file to use with docker compose: [KEY]=[VAL] format",
                                 default=os.path.join(home_dir, ".env"),
                                 requires=['--compose-file'])

    def main(self):
        """
        Main function for the Mistborn CLI
        """
        pass

@MistbornApp.subcommand("pullbuild")
class MistbornPullBuild(cli.Application):
    """
    Pull & Build docker images (while DNS is up).
    """
    def main(self):
        """
        Main function for Mistborn pulling and building docker images functionality
        """
        subprocess.run(f'sudo docker-compose -f {self.parent.compose_file} --env-file {self.parent.env_file} pull', shell=True) 
        subprocess.run(f'sudo docker-compose -f {self.parent.compose_file} --env-file {self.parent.env_file} build', shell=True) 

@MistbornApp.subcommand("getconf")
class MistbornConf(cli.Application):
    """
    CONF sub-command
    """
    
    user = cli.SwitchAttr("--user", str,
                            default='admin',
                            help="Specify the user's name")
    
    profile = cli.SwitchAttr("--profile", str,
                            default='default',
                            help="Specify the Wireguard profile name",
                            requires=['--user'])
    
    def main(self):
        """
        Main function for Mistborn CONF cli functionality
        """
        subprocess.run(f'sudo docker-compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm django python manage.py getconf {self.user} {self.profile}', shell=True)

@MistbornApp.subcommand("passwd")
class MistbornPasswd(cli.Application):
    """
    PASSWD sub-command (set/reset Mistborn default password)
    """

    def main(self):
        """
        Main function for Mistborn PASSWD cli functionality
        """
        mistborn_default_password = input("New Mistborn Default Password: ")
        subprocess.run(f"", shell=True)

@MistbornApp.subcommand("update")
class MistbornUpdate(cli.Application):
    """
    UPDATE sub-command
    """
    
    update_script = cli.SwitchAttr("--update_script", cli.ExistingFile,
                                 help="The script to call to update Mistborn",
                                 default="/opt/mistborn/scripts/update.sh")

    def main(self):
        """
        Main function for Mistborn update cli functionality
        """
        return subprocess.check_output(f'sudo {self.update_script}', shell=True)

@MistbornApp.subcommand("ping")
class MistbornPing(cli.Application):
    """
    Subcommand to use for testing purposes.
    """

    def main(self):
        """
        Main function for Mistborn ping
        """
        print("mistborn-cli: pong")

if __name__ == "__main__":
    MistbornApp.run()
