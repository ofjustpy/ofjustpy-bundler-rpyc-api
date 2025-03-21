# Instantiate SSHClientManager within a with statement to ensure proper resource management
port=8181
hostname="49.205.196.82"
username="kabiraatmonallabs"

from svelte_bundler.ssh_client_manager import SSHClientManager
with SSHClientManager(hostname, port, username) as ssh_manager:
    # Use ssh_manager to execute commands or perform other SSH-related operations
    stdin = ssh_manager.exec_command("list files", "ls -l")
    # Process stdout, stderr, etc.
