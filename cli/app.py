import sys
import os
import re
import time
import subprocess
from plumbum import cli

from cli.util.wg import WGApp

def sanitize_string(path):
    # Define a regex pattern for allowed characters
    pattern = r'[^\w\-\.]'
    
    # Replace any character not in the allowed set with an empty string
    sanitized_path = re.sub(pattern, '', path)
    
    return sanitized_path

class AlpenWallApp(cli.Application):
    """
    Main CLI App for AlpenWall
    """
    
    compose_file = cli.SwitchAttr("--compose-file", cli.ExistingFile,
                                 help="The Docker Compose file to use",
                                 default="/opt/alpenwall/base.yml")
    
    env_file = cli.SwitchAttr("--env-file", cli.ExistingFile,
                                 help="The environment variable file to use with docker compose: [KEY]=[VAL] format",
                                 default="/opt/alpenwall/.env",
                                 requires=['--compose-file'])

    def main(self):
        """
        Main function for the AlpenWall CLI
        """
        pass

AlpenWallApp.subcommand("wg", WGApp)

@AlpenWallApp.subcommand("pullbuild")
class AlpenWallPullBuild(cli.Application):
    """
    Pull & Build docker images (while DNS is up).
    """
    def main(self):
        """
        Main function for AlpenWall pulling and building docker images functionality
        """
        # cheat here while pullbuild is present in older update.sh scripts
        subprocess.run(f'sudo systemctl stop AlpenWall-base', shell=True)
        subprocess.run(f'echo "nameserver 1.1.1.2" | sudo tee /etc/resolv.conf', shell=True)
        ret = subprocess.run(f'sudo alpenwall-cli dbbackup', shell=True) 

        subprocess.run(f'sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} pull', shell=True) 
        subprocess.run(f'sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} build', shell=True) 

        if ret.returncode == 0:
            subprocess.run(f'sudo alpenwall-cli dbupgrade', shell=True)

@AlpenWallApp.subcommand("dbbackup")
class AlpenWallDBBackup(cli.Application):
    """
    Backup the current database
    """
    def main(self):
        ret = subprocess.run(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} down && \
                         sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} up -d postgres && \
                         sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm postgres backup && \
                         sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} down", shell=True) 
        
        return ret.returncode

@AlpenWallApp.subcommand("dbupgrade")
class AlpenWallDBUpgrade(cli.Application):
    """
    Check and upgrade the database
    """
    
    backup_filename = cli.SwitchAttr("--backup-filename", str,
                            default='',
                            help="Specify the backup filename")

    def main(self):

        try:
            backup_file = None
            
            # if a filename is given, use it
            if self.backup_filename:
                filename = sanitize_string(self.backup_filename)
                print(f"Searching for file: {filename}")
                
                exists = subprocess.check_output(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm -it postgres bash -c '[ -f {filename} ] && echo \"YES\" || echo \"NO\" '", shell=True).decode('utf-8').strip()

                if exists == "YES":
                    backup_file = filename

            # otherwise use the most recent
            if not backup_file:
                backup_file=subprocess.check_output(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm -it postgres bash -c 'ls -t /backups | head -n 1'", shell=True).decode('utf-8').strip()
            
            if not backup_file:
                print(f"No backup file present")
                return 1
            
            RUNNING_VERSION=subprocess.check_output(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm -it postgres bash -c 'psql -V'", shell=True).decode('utf-8').strip().split(" ")[2].split(".")[0]
            BACKUP_VERSION=subprocess.check_output(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm -it postgres bash -c 'tempfile=$(mktemp /tmp/tempfile.XXXXXXXX); gunzip -c /backups/{backup_file} > $tempfile; grep -oP \"Dumped from database version .*\" $tempfile'", shell=True).decode('utf-8').strip().split(" ")[4].split(".")[0]

            # if the parsing, splits, and indices didn't throw an Exception, we can assume these variables are populated strings
            if RUNNING_VERSION != BACKUP_VERSION:
                print(f"Dump is a different PostgreSQL version ({BACKUP_VERSION}) than currently running ({RUNNING_VERSION})")
                print(f"Restoring database from {backup_file}")

                subprocess.run(f"sudo docker volume rm alpenwall_production_postgres_data && \
                                 sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} up -d postgres", shell=True)
                
                rc = None
                numtries = 0
                while rc != 0 and numtries < 10:
                    out = subprocess.run(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm postgres restore {backup_file}", shell=True)
                    rc = out.returncode
                    numtries += 1
                    print(f"Waiting 5 seconds...")
                    time.sleep(5)
                
                return rc

            else:
                print(f"Dump is the same ({RUNNING_VERSION}) as currently running PostgreSQL. Ignoring.")

        except Exception as e:
            print(f"dbupgrade failed: {e}")
            return 1

        return 0

@AlpenWallApp.subcommand("dbbackuplist")
class AlpenWallDBBackupList(cli.Application):
    """
    List the available database backup files.
    """
    def main(self):

        print(subprocess.check_output(f"sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm -it postgres bash -c 'ls -ahlt /backups'", shell=True).decode('utf-8').strip())

@AlpenWallApp.subcommand("clearsessions")
class AlpenWallClearSessions(cli.Application):
    """
    CLEARSESSIONS sub-command
    """

    def main(self):
        """
        Main function for AlpenWall CLEARSESSIONS cli functionality
        """
        subprocess.run(f'sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} exec django /entrypoint python manage.py clear_mfa_sessions', shell=True)

@AlpenWallApp.subcommand("getconf")
class AlpenWallConf(cli.Application):
    """
    GETCONF sub-command
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
        Main function for AlpenWall CONF cli functionality
        """
        subprocess.run(f'sudo docker compose -f {self.parent.compose_file} --env-file {self.parent.env_file} run --rm django python manage.py getconf {self.user} {self.profile}', shell=True)

@AlpenWallApp.subcommand("update")
class AlpenWallUpdate(cli.Application):
    """
    UPDATE sub-command
    """
    
    update_script = cli.SwitchAttr("--update_script", cli.ExistingFile,
                                 help="The script to call to update AlpenWall",
                                 default="/opt/alpenwall/scripts/update.sh")

    def main(self):
        """
        Main function for AlpenWall update cli functionality
        """
        return subprocess.check_output(f'sudo {self.update_script}', shell=True)

@AlpenWallApp.subcommand("ping")
class AlpenWallPing(cli.Application):
    """
    Subcommand to use for testing purposes.
    """

    def main(self):
        """
        Main function for AlpenWall ping
        """
        print("alpenwall-cli: pong")

if __name__ == "__main__":
    AlpenWallApp.run()
