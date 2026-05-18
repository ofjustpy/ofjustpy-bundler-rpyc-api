import os
import sys
from string import Template
import importlib
from .ssh_client_manager import SSHClientManager
import tempfile
from .config import (hostname,
                     port,
                     username,
                     bundler_base_directory
                     )
from svelte_safelist_builder import get_svelte_safelist
from . import runtime_context
from . import helper_utils
from .helper_utils import build_fetch_bundle
from .config import bundler_dir, node_bin_path
from .app_css_template import build_app_css
from .publish_tailwind_svelte_safelist import publish_tailwind_svelte_safelist
from .publish_lucide_icons_component_render_svelte import publish_lucide_icons_component_render_svelte

import jsexprs.macro_module as jsexprs_mm    
def kebab_lower(label):
    modstr = "".join(c if c.islower() else f"-{c.lower()}" for c in label[1:])
    return f"""{label[0].lower()}{modstr}"""

    

                        
import_preset_stmt = ""
import_themes_stmt = ""
include_tailwind_forms_stmt = ""



# TODO: tailwind forms
# TODO: font_families

from .shadcn_component_render_template import publish_shadcn_component_render_svelte
from .component_render_by_type_template import publish_component_render_by_type
from .publish_shadcn_bind_value_components import publish_shadcn_bind_value_component_render_svelte
def build_bundle(target_module,
                 dep_modules,

                 output_dir = "./",
                 enable_svg_components=False,
                 enable_fontawesome_components = False,
                 enable_skeleton_components = False,
                 enable_lucide_components = False,
                 enable_shadcn_layerchart_components=False
                 ):

    enable_shadcn_components = False
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        runtime_context.ssh_client_manager = ssh_client_manager




        # find the import stmts
        # publish bind_value components
        
        ssh_client_manager.exec_command("remove existing shadcn components",
                                    f"""cd {bundler_dir}; 

                                    rm -rf src/lib/components/ui/* """)

        # ================= shadcn import directives =================
        import_var_stmts = ""
        import_stmts = []
        target_mod = importlib.import_module(target_module)
        for import_directive in jsexprs_mm.import_var_stmts:
            variable_str = import_directive['var_label']
            module_name = import_directive['module']
            statement = f'import {{ {variable_str} }} from "{module_name}";'
            import_stmts.append(statement)

        import_var_stmts = "\n".join(import_stmts)


        has_shadcn_components = publish_shadcn_component_render_svelte(target_module,
                                                   dep_modules,
                                               import_var_stmts,
                                                   ssh_client_manager)
        has_shadcn_bindvalue_components = publish_shadcn_bind_value_component_render_svelte(target_module,
                                                          dep_modules,
                                                          import_var_stmts,
                                                          ssh_client_manager)


        # TBD
        #has_skeleton_components = publish_skeleton_component_render_svelte(target_module, dep_modules, ssh_client_manager)
        build_app_css()

        # ===================== publish safelist =====================
        publish_tailwind_svelte_safelist(target_module,
                                         dep_modules
                                         )

        enable_lucide_icons_components = True
        publish_lucide_icons_component_render_svelte(target_module, dep_modules, ssh_client_manager)

        publish_component_render_by_type(enable_shadcn_components = has_shadcn_components,
                                         enable_shadcn_bindvalue_components = has_shadcn_bindvalue_components ,
                                         enable_lucide_icons_components = enable_lucide_icons_components
                                         )
        build_fetch_bundle(output_dir)
        
    pass
