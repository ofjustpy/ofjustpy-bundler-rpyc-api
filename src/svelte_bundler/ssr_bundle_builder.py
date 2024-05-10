import paramiko
from .ssh_client_manager import SSHClientManager
from string import Template
import sys

from .config import (hostname,
                     port,
                     username
                     )

bundler_base_dir = "/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/ofjustpy-tailwind-ssr-bundler/"


safelist_template = Template("""<div class="$twsty_str"></div>
""")

def build_bundle_ssr(twsty_arr,
                 ):

    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        # Perform SSH operations using ssh_client
        ssh_client_manager.exec_command("delete bundle",
                                        f"""cd {bundler_base_dir}/dist;

                                        rm bundler.iife.js bundler.iife.js.map style.css""")

        # ======================== TwSafelist ========================
        

        twsty_str = " ".join(twsty_arr)
        safelist_str = safelist_template.substitute(twsty_str=twsty_str,
                                                                  )
        temp_file_path = "/tmp/temp_file.txt"
        with open(temp_file_path, "w") as f:
            f.write(safelist_str)


        ssh_client_manager.put_file(temp_file_path,
                                    f"{bundler_base_dir}/public/safelist.html")
        # ============================ end ===========================

        #TODO: configure fonts

        ssh_client_manager.exec_command("build bundle",
                                        f"""cd {bundler_base_dir}

                                        npm run build""")

        ssh_client_manager.get_file(f"""{bundler_base_dir}/dist/style.css""",
                                    "/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/style_ssr.css"
                                    )

