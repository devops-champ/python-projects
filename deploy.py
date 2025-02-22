import paramiko
import yaml
import os
import logging
from datetime import datetime


def date_time():
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return time_stamp


def load_yaml():
    with open("config.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
    
def ssh_connect():
    try:
        config = load_yaml()
        server = config["server"]               
        #print(server)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server["host"],
            username=server["user"],
            key_filename=server["private_key"]
        )
        print("SSH connection established")

    except Exception as error:
        print(error)

def backup_config(ssh_connect):
    try:
        backup_dir = "/home/ubuntu/backup"
        config_file = "/etc/nginx/nginx.conf"
        date_time = date_time()
        backup_path = f"{backup_dir}/{date_time}_nginx.conf.bak"

        stdin, stdout, stderr = ssh_connect.exec_command(f"mkdir -p {backup_dir}")
        stderr_output = stderr.read().decode()
        if stderr_output:
            logging.error(f"Error creating backup directory: {stderr_output}")
            return
        
        stdin, stdout, stderr = ssh_connect.exec_command(f"cp {config_file} {backup_path}")
        stderr_output = stderr.read().decode()
        if stderr_output:
            logging.error(f"Error during backup: {stderr_output}")
        else:
            logging.info(f"Backup of nginx.conf saved to {backup_path}")

      
    except Exception as error:
        logging.error(f"Error during backup: {error}")

logging.basicConfig(level=logging.INFO)

ssh_connect()

