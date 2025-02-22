def backup_config():
    try:
        config = load_yaml()
        server = config["server"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server["host"],
            username=server["user"],
            key_filename=server["private_key"]
        )
        print("SSH connection established")

        sftp = ssh.open_sftp()
        file_path = server["config_file"]
        backup_path = "/tmp/backup/nginx.conf"
        sftp.get(file_path, backup_path)
        print(f"Backup of {file_path} saved to {backup_path}")

        sftp.close()
        ssh.close()
    except Exception as error:
        print("Error:", error)


def backup_config(ssh_client):
    try:
        sftp = ssh_client.open_sftp()
        remote_path = "/etc/nginx/nginx.conf"
        datetime = date_time()
        backup_dir = "/home/ubuntu/backup" 
        backup_path = f"{backup_dir}/{datetime}_nginx.conf.bak"

        try:
            sftp.stat(backup_dir)
        except FileNotFoundError:
            sftp.mkdir(backup_dir)

        sftp.put(remote_path, backup_path)
        logging.info(f"Backup of {remote_path} saved to {backup_path}")
        sftp.close()
    except Exception as error:
        logging.error(f"Error during backup: {error}")  


        # stdin, stdout, stderr = ssh_client.exec_command(f"sudo mv {temp_path} {remote_server_path}", get_pty=True)
        # stderr_output = stderr.read().decode()
        # if stderr_output:
        #     logging.error(f"Error moving or reloading NGINX {stderr_output}")
        # else:
        #     logging.info(f"NGINX config updated {remote_server_path}")                  