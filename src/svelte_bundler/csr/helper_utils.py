from .. import runtime_context
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )
from ..config import node_bin_path


def build_and_fetch_bundle(svelte_bundle_dir, shadcn_component_install_stmt):
    local_svelte_bundle_dir = 'static/' + svelte_bundle_dir
    runtime_context.ssh_client_manager.exec_command("install shadcn components",
                                        f"""cd {remote_svelte_bundle_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                        rm -rf src/lib/components/ui/; {shadcn_component_install_stmt}
""")
                
    runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {remote_svelte_bundle_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                        pnpm run build
""")        
    runtime_context.ssh_client_manager.get_file(f"""{remote_svelte_bundle_dir}/dist/bundle.css""",
                                                    f"{local_svelte_bundle_dir}/style.css"
                                                    )

    runtime_context.ssh_client_manager.get_file(f"""{remote_svelte_bundle_dir}/dist/bundle.iife.js""",
                                                    f"{local_svelte_bundle_dir}/bundle.iife.js"
                                                    )

    runtime_context.ssh_client_manager.get_file(f"""{remote_svelte_bundle_dir}/dist/bundle.iife.js.map""",
                                                    f"{local_svelte_bundle_dir}/bundle.iife.js.map"
                                                    )

        
