import paramiko
import yaml
import logging
from datetime import datetime
import time


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
        return ssh

    except Exception as error:
        print(error)

def backup_config(ssh_client):
    try:
        config = load_yaml()
        server = config["server"]             
        backup_dir = "/home/ubuntu/backup"
        config_file = server["config_file"]
        timedate = date_time()
        backup_path = f"{backup_dir}/{timedate}_nginx.conf.bak"

        stdin, stdout, stderr = ssh_client.exec_command(f"mkdir -p {backup_dir}")
        stderr_output = stderr.read().decode()
        if stderr_output:
            logging.error(f"Error creating backup directory: {stderr_output}")
            return
        
        stdin, stdout, stderr = ssh_client.exec_command(f"cp {config_file} {backup_path}")
        stderr_output = stderr.read().decode()
        if stderr_output:
            logging.error(f"Error during backup: {stderr_output}")
        else:
            logging.info(f"Backup of nginx.conf saved to {backup_path}")

      
    except Exception as error:
        logging.error(f"Error during backup: {error}")

def update_config(ssh_client):
    try:
        config = load_yaml()
        server = config["server"]          
        local_path = "nginx.conf"    
        remote_server_path = server["config_file"]
        sftp = ssh_client.open_sftp()       
        try:
            sftp.put(local_path, remote_server_path)
            logging.info(f"Config file from {local_path} copied to {remote_server_path}")
        except Exception as e:
            logging.error(f"File upload failed: {e}")    
        sftp.close()
        time.sleep(2)

    except Exception as error:
        print(error) 

def restart_nginx(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command("sudo systemctl restart nginx")
        stderr_output = stderr.read().decode()
        if stderr_output:
            logging.error(f"Error restarting service: {stderr_output}")
        else:
            logging.info(f"Service restarted successfully: {stderr_output}")

    except Exception as error:
        print(error) 






logging.basicConfig(level=logging.INFO)

ssh_client = ssh_connect()
if ssh_client:
    backup_config(ssh_client)
    update_config(ssh_client)
    ssh_client.close()