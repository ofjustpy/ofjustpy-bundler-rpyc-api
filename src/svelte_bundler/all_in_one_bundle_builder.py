import os
import sys
from string import Template
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
from .app_css_template import build_app_css
from .tailwind_svelte_safelist  import publish_tailwind_svelte_safelist
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
        
        
        publish_shadcn_component_render_svelte(target_module,
                                                   dep_modules,
                                                   ssh_client_manager)
        build_app_css()




        publish_component_render_by_type()
        build_fetch_bundle(output_dir)
        
    pass
