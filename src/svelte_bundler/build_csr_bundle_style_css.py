from .ssh_client_manager import SSHClientManager
from . import runtime_context
from .config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir
                     )

from twtags_safelist import get_csr_components
from .helper_utils import build_fetch_bundle, write_to_bundler_dir

def build_csr_bundle_style_css(target_module,
                            output_dir="./"
                            ):
    res = get_csr_components(target_module)
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        runtime_context.ssh_client_manager = ssh_client_manager
        print(csr_bundle_style_css_dir)
        write_to_bundler_dir(f"""var scui_CSR_components = {res};""",
                             "src/scui_csr_components.js",
                             target_bundler_dir = csr_bundle_style_css_dir

                             )
        print (res)

