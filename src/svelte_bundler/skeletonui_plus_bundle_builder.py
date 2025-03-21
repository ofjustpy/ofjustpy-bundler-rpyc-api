import paramiko
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


import_preset_stmt = ""
import_themes_stmt = ""

app_css_template = Template("""
@import "tailwindcss";
@import '@skeletonlabs/skeleton';
@source './node_modules/@skeletonlabs/skeleton-svelte/dist';

$import_preset_stmt

$import_themes_stmt


""")

preset_themes = [
    "catppuccin", "cerberus", "concord", "crimson", "fennec",
    "hamlindigo", "legacy", "mint", "modern", "mona",
    "nosh", "nouveau", "pine", "reign", "rocket",
    "rose", "sahara", "seafoam", "terminus", "vintage",
    "vox", "wintry"
]

bundler_dir = f"{bundler_base_directory}/skeletonui" 
def build_bundle(twsty_str,
                 font_families=[],
                 fontawesome_icons = [],
                 ui_library="skeletonui",
                 output_dir = "./",
                 skui_themes = ["crimson"],
                 
                 skui_preset_import = True
                 ):
    
    if skui_preset_import:
        import_preset_stmt = """@import '@skeletonlabs/skeleton/optional/presets';"""
    
    for theme in skui_themes:
        assert theme in preset_themes

        
    import_themes_stmt = "\n".join([f"""@import '@skeletonlabs/skeleton/themes/{theme}'; """ for theme in skui_themes]
                                   )

    # ========================= safelist.txt =========================
    safelist_svelte_str= "\n".join(twsty_str)

    # Create a temporary file and write the content
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(safelist_svelte_str)
        print(f"Data written to temporary file: {temp_file.name}")


    # ============================== end =============================

    # ============================ app.css ===========================
    app_css_str = app_css_template.substitute(import_preset_stmt=import_preset_stmt, import_themes_stmt=import_themes_stmt)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as app_css_temp_file:
        app_css_temp_file.write(app_css_str)
        print(f"Data written to temporary file: {app_css_temp_file.name}")

        
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        ssh_client_manager.put_file(temp_file.name,
                                    f"{bundler_dir}/safelist.txt")
    
        ssh_client_manager.put_file(app_css_temp_file.name,
                                    f"{bundler_dir}/src/app.css")

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js""",
                                    f"{output_dir}/bundle.iife.js"
                                    )


        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.css""",
                                    f"{output_dir}/style.css"
                                    )
        
