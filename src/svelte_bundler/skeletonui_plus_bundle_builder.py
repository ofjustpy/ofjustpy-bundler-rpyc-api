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
include_tailwind_forms_stmt = ""
app_css_template = Template("""
@import "tailwindcss";
$include_tailwind_forms_stmt
@import '@skeletonlabs/skeleton';
@source './node_modules/@skeletonlabs/skeleton-svelte/dist';
@source "safelist.txt";
$import_preset_stmt

$import_themes_stmt


.preset-typo-display-4,
  .preset-typo-display-3,
  .preset-typo-display-2,
  .preset-typo-display-1,
  .preset-typo-headline,
  .preset-typo-title,
  .preset-typo-subtitle,
  .preset-typo-caption,
  .preset-typo-menu,
  .preset-typo-button {
    color: var(--heading-font-color);
    font-family: var(--heading-font-family);
    font-weight: var(--heading-font-weight);
    @variant dark {
      color: var(--heading-font-color-dark);
    }
  }

  /* Body */
  .preset-typo-body-1,
  .preset-typo-body-2,
  .preset-typo-caption,
  .preset-typo-menu,
  .preset-typo-button {
    color: var(--heading-font-color);
    @variant dark {
      color: var(--heading-font-color-dark);
    }
  }

  /* Unique Properties */
  .preset-typo-display-4 {
    font-size: var(--text-7xl);
    @variant lg {
      font-size: var(--text-9xl);
    }
  }
  .preset-typo-display-3 {
    font-size: var(--text-6xl);
    @variant lg {
      font-size: var(--text-8xl);
    }
  }
  .preset-typo-display-2 {
    font-size: var(--text-5xl);
    @variant lg {
      font-size: var(--text-7xl);
    }
  }
  .preset-typo-display-1 {
    font-size: var(--text-4xl);
    @variant lg {
      font-size: var(--text-6xl);
    }
  }
  .preset-typo-headline {
    font-size: var(--text-2xl);
    @variant lg {
      font-size: var(--text-4xl);
    }
  }
  .preset-typo-title {
    font-size: var(--text-xl);
    @variant lg {
      font-size: var(--text-3xl);
    }
  }
  .preset-typo-subtitle {
    font-size: var(--text-base);
    font-family: var(--heading-font-family);
    color: var(--color-surface-700-300);
    @variant lg {
      font-size: var(--text-xl);
    }
  }
  .preset-typo-body-1 {
    font-size: var(--text-xl);
    @variant lg {
      font-size: var(--text-3xl);
    }
  }
  .preset-typo-body-2 {
    font-size: var(--text-lg);
    @variant lg {
      font-size: var(--text-xl);
    }
  }
  .preset-typo-caption {
    font-size: var(--text-sm);
    color: var(--color-surface-700-300);
  }
  .preset-typo-menu {
    font-weight: bold;
  }
  .preset-typo-button {
    font-weight: bold;
  }


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
                 use_tailwind_forms = True,
                 skui_themes = ["crimson"],
                 
                 skui_preset_import = True
                 ):
    
    if skui_preset_import:
        import_preset_stmt = """@import '@skeletonlabs/skeleton/optional/presets';"""
    
    for theme in skui_themes:
        assert theme in preset_themes

    if use_tailwind_forms:
        include_tailwind_forms_stmt = """@plugin '@tailwindcss/forms';"""
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
    app_css_str = app_css_template.substitute(import_preset_stmt=import_preset_stmt,
                                              import_themes_stmt=import_themes_stmt,
                                              include_tailwind_forms_stmt=include_tailwind_forms_stmt)
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as app_css_temp_file:
        app_css_temp_file.write(app_css_str)
        print(f"Data written to temporary file: {app_css_temp_file.name}")

        
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        ssh_client_manager.put_file(temp_file.name,
                                    f"{bundler_dir}/safelist.txt")
        
    
        ssh_client_manager.put_file(app_css_temp_file.name,
                                    f"{bundler_dir}/src/app.css")

        ssh_client_manager.exec_command("delete bundle",
                                        f"""cd {bundler_dir}/dist;

                                        rm bundler.iife.js bundle.css""")

        ssh_client_manager.exec_command("build bundle",
                                        f"""cd {bundler_dir}

                                        npm run build""")

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
        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js""",
                                    f"{output_dir}/bundle.iife.js"
                                    )

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js.map""",
                                    f"{output_dir}/bundle.iife.js.map"
                                    )
        

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.css""",
                                    f"{output_dir}/style.css"
                                    )
        
