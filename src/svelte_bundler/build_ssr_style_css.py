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
from twtags_safelist import get_twtags_safelist
from . import runtime_context
from .helper_utils import build_fetch_bundle, write_to_bundler_dir
from .config import ssr_style_css_dir, node_bin_path
from .event_handler_ssr import ajax_event_handling


def kebab_lower(label):
    modstr = "".join(c if c.islower() else f"-{c.lower()}" for c in label[1:])
    return f"""{label[0].lower()}{modstr}"""

    

                        
import_preset_stmt = ""
import_themes_stmt = ""
include_tailwind_forms_stmt = ""



def build_ssr_style_css(target_module,
                        #dep_modules,

                        output_dir = "./",
                 ):
    enable_fontawesome = False
    fontawesome_app_css_import_stmt = ""
    enable_event_handling = False
    
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        runtime_context.ssh_client_manager = ssh_client_manager


        res  = get_twtags_safelist(target_module)
        print("get twtags list = ", res)
        if len(res.fontawesome_components) > 0:
            enable_fontawesome = True
            fontawesome_app_css_import_stmt = """@import "@fortawesome/fontawesome-free/css/all.min.css";
svg.svg-inline--fa {
  display: inline-block;
  height: 1em;
  vertical-align: -.125em;
}

            
"""
                    
        safelist_svelte_str= "\n".join(res.all_twsty_tags)
        write_to_bundler_dir(safelist_svelte_str,
                             "safelist.txt",
                             target_bundler_dir = ssr_style_css_dir
                             )
        

        # ==================== build_ssr_app_css() ===================
        skeleton_ui_css = ""
        skeleton_ui_import = ""
        skeleton_app_css = ""
        skeleton_theme_selector_stmt = ""
        if res.use_skeleton_ui:

            skeleton_ui_import = f"""@import '@skeletonlabs/skeleton';
@import '@skeletonlabs/skeleton/optional/presets';
@import '@skeletonlabs/skeleton/themes/{res.skeleton_ui_theme}';
@source '../node_modules/@skeletonlabs/skeleton-svelte/dist';            
"""
            skeleton_app_css ="""
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

"""
            
            
        app_css_str = f"""
@import "tailwindcss";
{skeleton_ui_import}        
@plugin "@tailwindcss/typography";
@source "safelist.txt";    
{fontawesome_app_css_import_stmt}
{skeleton_app_css}        
"""
        write_to_bundler_dir(app_css_str,
                             "src/app.css",
                             target_bundler_dir=ssr_style_css_dir
                             )

        # ============================== end =============================
        

        runtime_context.ssh_client_manager.exec_command("build bundle",
                                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:$PATH;
                                                        pnpm remove @fortawesome/fontawesome-free
                                                        """
                                                        )
            
        # install fontawesome
        if enable_fontawesome:
            runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:$PATH;
                                        pnpm install @fortawesome/fontawesome-free
""")
                    
            pass

        main_ts_body = """import { mount } from 'svelte'
import './app.css'
"""
            
        if res.enable_event_handling:
            # TODO: check if websockets is enabled
            write_to_bundler_dir(ajax_event_handling,
                                 "src/event_handler.js",
                                 target_bundler_dir=ssr_style_css_dir
                                 )
            main_ts_body = f"""import {{ mount }} from 'svelte'
import './app.css'
import './event_handler.js';
{skeleton_theme_selector_stmt}            
"""
            
            
            
        write_to_bundler_dir(main_ts_body,
                             "src/main.ts",
                             target_bundler_dir=ssr_style_css_dir
                             )


    

        try:
            os.remove(f"{output_dir}/style.css")
        except:
            pass

        runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:$PATH;
                                        pnpm run build
""")        
        runtime_context.ssh_client_manager.get_file(f"""{ssr_style_css_dir}/dist/bundle.css""",
                                                    f"{output_dir}/style.css"
                                                    )

        runtime_context.ssh_client_manager.get_file(f"""{ssr_style_css_dir}/dist/bundle.iife.js""",
                                                    f"{output_dir}/bundle.iife.js"
                                                    )

        runtime_context.ssh_client_manager.get_file(f"""{ssr_style_css_dir}/dist/bundle.iife.js.map""",
                                                    f"{output_dir}/bundle.iife.js.map"
                                                    )

        

        
        pass
