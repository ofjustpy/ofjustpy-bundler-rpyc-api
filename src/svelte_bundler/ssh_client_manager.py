import paramiko
import sys

font_family_twcfg_mapping = {
		   'poppins': ['Poppins', 'sans-serif'],
		   'roboto': ['Roboto', 'sans-serif'],
		   'lato': ['Lato', 'sans-serif'],
		   'montserrat': ['Montserrat', 'sans-serif'],
		   'raleway': ['Raleway', 'sans-serif'],
		   'merriweather': ['Merriweather', 'serif'],
		   'oswald': ['Oswald', 'sans-serif'],
		   'robot-condensed': ['Roboto Condensed', 'sans-serif'],
		   'lora': ['Lora', 'serif'],
		   'geist': ['Geist', 'sans-serif'],

		   'georgia': ['Georgia', 'serif'],
		   'times-new-roman': ['Times New Roman', 'serif'],
		   'baskerville': ['Baskerville', 'serif'],
		   'playfair-display': ['Playfair Display', 'serif'],
		   'libre-baskerville': ['Libre Baskerville', 'serif'],
		   'crimson-text': ['Crimson Text', 'serif'],
		   'cardo': ['Cardo', 'serif'],

		   'arial': ['Arial', 'sans-serif'],
		   'helvetica': ['Helvetica', 'sans-serif'],
		   'open-sans': ['Open Sans', 'sans-serif'],
		   'futura': ['Futura', 'sans-serif'],
		   'avenir': ['Avenir', 'sans-serif'],
		   'nunito-sans': ['Nunito Sans', 'sans-serif'],
		   'source-sans-pro': ['Source Sans Pro', 'sans-serif'],
		   'pt-sans': ['PT Sans', 'sans-serif'],

        'courier-new': ['Courier New', 'monospace'],
        'roboto-mono': ['Roboto Mono', 'monospace'],
        'inconsolata': ['Inconsolata', 'monospace'],
        'monaco': ['Monaco', 'monospace'],
        'source-code-pro': ['Source Code Pro', 'monospace'],

        'pacifico': ['Pacifico', 'cursive'],
        'raleway-dots': ['Raleway Dots', 'cursive'],
        'sacramento': ['Sacramento', 'cursive'],
        'anton': ['Anton', 'cursive'],
        'cinzel': ['Cinzel', 'cursive'],
        'dancing-script': ['Dancing Script', 'cursive'],
        'great-vibes': ['Great Vibes', 'cursive'],
        'kaushan-script': ['Kaushan Script', 'cursive'],
        'josefin-sans': ['Josefin Sans', 'cursive'],
        'abril-fatface': ['Abril Fatface', 'cursive'],

    'brush-script-mt': ['Brush Script MT', 'cursive'],
        'comic-sans-ms': ['Comic Sans MS', 'cursive'],
        'kristen-itc': ['Kristen ITC', 'cursive'],
        'lobster': ['Lobster', 'cursive'],
        'shadows-into-light': ['Shadows Into Light', 'cursive'],
        'patrick-hand': ['Patrick Hand', 'cursive'],
        'permanent-marker': ['Permanent Marker', 'cursive'],
        'indie-flower': ['Indie Flower', 'cursive'],
        'satisfy': ['Satisfy', 'cursive'],

  
        'inter': ['Inter', 'sans-serif'],
        'gotham': ['Gotham', 'sans-serif'],
        'proxima-nova': ['Proxima Nova', 'sans-serif'],
}


class SSHClientManager:
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def __enter__(self):
        self.ssh_client.connect(self.hostname, port=self.port, username=self.username)
        self.sftp_client = self.ssh_client.open_sftp()

        return self

    def exec_command(self, cmd_desc, command, ):
        try:
            print ("Now executing command ", cmd_desc, " ", command)
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=420)
            
            for line in stdout:
                sys.stdout.write(line)

            for line in stderr:
                sys.stderr.write(line)

        except paramiko.SSHException as e:
            print (f"SSH error: {e}")
        except paramiko.PipeTimeout:
            print("Timeout error: The read operation timed out.")
            
            
    def get_file(self, remote_file_path, local_file_path):
        self.sftp_client.get(remote_file_path, local_file_path)

    def put_file(self, local_file_path,  remote_file_path):
        # Write the string to a temporary local file

        # Ship the temporary local file to the remote server
        self.sftp_client.put(local_file_path, remote_file_path)

        
    def __exit__(self, exc_type, exc_value, traceback):
        if self.sftp_client:
            self.sftp_client.close()
        self.ssh_client.close()
