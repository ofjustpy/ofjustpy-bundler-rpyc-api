import paramiko
def test_execute_command(hostname, port, username, command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, port=port, username=username)
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print("Command executed successfully!")
        print(stdout.read().decode())
        ssh_client.close()
    except Exception as e:
        print(f"Error in executing command: {e}")

# Test Execute Command with Key-based Authentication
port=8181
hostname="49.205.196.82"
username="kabiraatmonallabs"
test_execute_command(hostname, port, username,  "ls -l")
