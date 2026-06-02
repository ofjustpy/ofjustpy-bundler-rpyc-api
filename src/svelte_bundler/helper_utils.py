import tempfile
import os

from .config import bundler_dir, node_bin_path
from . import runtime_context
def write_to_bundler_dir(content_str,
                         target_rel_dir,
                         target_bundler_dir=bundler_dir):
    print("now writing to + ", target_bundler_dir, " ", target_rel_dir)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(content_str)
        #TODO: move to logging 
        #print(f"Data written to temporary file: {app_css_temp_file.name}")

    runtime_context.ssh_client_manager.put_file(temp_file.name,
                                    f"{target_bundler_dir}/{target_rel_dir}")










    
def kebab_lower(label):
    modstr = "".join(c if c.islower() else f"-{c.lower()}" for c in label[1:])
    return f"""{label[0].lower()}{modstr}"""


def build_fetch_bundle(output_dir, remote_bundler_dir = bundler_dir):
    runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {remote_bundler_dir}; export PATH={node_bin_path}:$PATH;
                                        pnpm run build""")

    try:
        os.remove(f"{output_dir}/bundle.iife.js")
    except:
        pass

    try:
        os.remove(f"{output_dir}/bundle.iife.js.map")
    except:
        pass

    
    try:
        os.remove(f"{output_dir}/style.css")
    except:
        pass

        
    runtime_context.ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js""",
                                f"{output_dir}/bundle.iife.js"
                                )
    runtime_context.ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js.map""",
                                        f"{output_dir}/bundle.iife.js.map"
                                )


    runtime_context.ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.css""",
                                f"{output_dir}/style.css"
                                )


def fetch_style_css(output_dir, remote_bundler_dir = bundler_dir):
    runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {remote_bundler_dir}; export PATH={node_bin_path}:$PATH;
                                        pnpm run build""")


    try:
        os.remove(f"{output_dir}/style.css")
    except:
        pass

        


    runtime_context.ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.css""",
                                f"{output_dir}/style.css"
                                )

    
