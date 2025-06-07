import paramiko

def test_sftp_transfer(hostname,
                       port,
                       username,
                       remote_file,
                       local_file):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname, port=port, username=username)
        sftp_client = ssh_client.open_sftp()
        sftp_client.get(remote_file, local_file)
        print("SFTP transfer successful!")
        sftp_client.close()
        ssh_client.close()
    except Exception as e:
        print(f"Error in SFTP transfer: {e}")





# Test SSH Tunneling with Key-based Authentication
port=8181
hostname="49.205.196.82"
username="kabiraatmonallabs"
remote_file = "/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Ofjustpy-Svelte-Tailwind-Skeleton-Bundler/dist/bundle.iife.js"
local_file = "/tmp/bundle.iife.js"
test_sftp_transfer(hostname, port, username, remote_file, local_file)
