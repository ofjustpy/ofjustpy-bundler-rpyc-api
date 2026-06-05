"""
devel guide
===========

Order of concerns
- get_csr_components
- get_twtags_safelist
- shadcn components (write json)
- csr components (write json)
- safelist
- skeleton ui theme
- app.css
- event handling
- main.ts
- pyodide setup
- npm add shadcn components
- ShadcnComponent.svelte
- install_csr_components
- build and copy bundle


"""
from pathlib import Path
from string import Template

from ..ssh_client_manager import SSHClientManager
from .. import runtime_context
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )
from ..config import node_bin_path
from twtags_safelist import (get_csr_components, 
                             get_twtags_safelist
                             )
from ..helper_utils import  write_to_bundler_dir
from .helper_utils import build_and_fetch_bundle
from ..setup_inbrowser_kavya_exec import setup_inbrowser_kavya_exec
from ..event_handler_ssr import ajax_event_handling
from .publish_component_render_by_type import publish_component_render_by_type
from .publish_lucide_icons_component_render_svelte import publish_lucide_icons_component_render_svelte
from .publish_store_shadcn_bindvalue import publish_store_shadcn_bindvalue
# Get the directory of the current file
current_dir = Path(__file__).parent.resolve()

skeleton_theme_selector_stmt = f"""
function set_skui_theme(selectedTheme) {{
console.log("start setting");

// We already have the value passed in as 'selectedTheme'
const html = document.querySelector('html');
html.setAttribute('data-theme', selectedTheme);

console.log("Done setting theme to:", selectedTheme);
}}

window.set_skui_theme = set_skui_theme
"""
            
def install_csr_components(runtime_context,
                           csr_components_html_tag):
    for html_tag in csr_components_html_tag:
        print("TODO: now installing ", html_tag)
        # pnpm add ace-builds
        pass
    
def kebab_to_pascal(text: str) -> str:
    """Converts a kebab-case string to PascalCase.
    
    Args:
        text (str): The string to convert (e.g., "alert-dialog").
        
    Returns:
        str: The converted PascalCase string (e.g., "AlertDialog").
    """
    return "".join(word.capitalize() for word in text.split("-"))

def build_csr_svelte_bundle(target_module,
                            enable_skui_theme_selector = False, 
                            enable_inbrowser_exec=False,
                            additional_skui_themes = []
                            ):
    # get the list of all shadcn and csr components used by the page 
    page_csr_components = get_csr_components(target_module)
    res  = get_twtags_safelist(target_module)
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        runtime_context.ssh_client_manager = ssh_client_manager
        # ===================== shadcn components ====================
        # TODO: install the used shadcn components
        # the .json is actually a list
        write_to_bundler_dir(f"""export const scui_CSR_components = {[*page_csr_components.shadcn_components.json,
        *page_csr_components.shadcn_bindvalue_components.json
        ]};""",
                             "src/scui_csr_components.js",
                             target_bundler_dir = remote_svelte_bundle_dir

                             )
        # TODO: install the used csr components

        # ============================ end ===========================

        # ============= write json for lucide components =============
        # we don't need lucide_csr_icons.js
        # lucide icons are captured as csr components 
        # write_to_bundler_dir(f"""export const lucide_CSR_components = {page_csr_components.lucide_icons.json};""",
        #                      "src/lucide_csr_icons.js",
        #                      target_bundler_dir = remote_svelte_bundle_dir
        #                      )

        # ============================ end ===========================
        
        # ============= csr components (like ace editor) =============
        write_to_bundler_dir(f"""export const csr_components = {page_csr_components.csr_components.json};""",
                             "src/csr_components.js",
                             target_bundler_dir = remote_svelte_bundle_dir
                             )

        # ============================ end ===========================
        
        # ========================= safelist =========================
        safelist_svelte_str= "\n".join(res.all_twsty_tags)
        write_to_bundler_dir(safelist_svelte_str,
                             "safelist.txt",
                             target_bundler_dir = remote_svelte_bundle_dir
                             )
        
        # ============================ end ===========================
        
        # ====================================================================
        # =================== skeleton ui and theme ==================
        skeleton_ui_css = ""
        skeleton_ui_import = ""
        skeleton_app_css = ""
        skeleton_theme_selector_stmt = ""
        additional_skui_themes_stmt = "\n".join([f"@import '@skeletonlabs/skeleton/themes/{skeleton_ui_theme}';" for skeleton_ui_theme in additional_skui_themes

                                                  ]
                                                 )

        
        if not enable_skui_theme_selector:
            skeleton_theme_selector_stmt = ""

        if res.use_skeleton_ui:

            skeleton_ui_import = f"""@import '@skeletonlabs/skeleton';
@import '@skeletonlabs/skeleton/optional/presets';
@import '@skeletonlabs/skeleton/themes/{res.skeleton_ui_theme}';
@import '@skeletonlabs/skeleton/themes/cerberus';
@import '@skeletonlabs/skeleton/themes/mint';
{additional_skui_themes_stmt}
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
            # ========================== end =========================
            # ========================================================
            # ==================== app css ====================
            # ========================================================
        shadcn_app_css = """
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.556 0 0);
}

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
  }
}
        
        """
        
        # TODO: {fontawesome_app_css_import_stmt}
        # testing to remove all shadcn directives
        shadcn_app_css = ""
        app_css_str = f"""
@import "tailwindcss";
{skeleton_ui_import}        
@plugin "@tailwindcss/typography";
@source "safelist.txt";    

{skeleton_app_css}

{shadcn_app_css}        
"""
        write_to_bundler_dir(app_css_str,
                             "src/app.css",
                             target_bundler_dir=remote_svelte_bundle_dir
                             )

        # ============================== end =============================
        # TODO: websocket based event handling
        # ==================== ssr event handling ====================
        ssr_event_handler_stmt = ""
        # if res.enable_event_handling:
        #     write_to_bundler_dir(ajax_event_handling,
        #                          "src/ssr_event_handler.js",
        #                          target_bundler_dir=remote_svelte_bundle_dir
        #                          )
        #     ssr_event_handler_stmt = "import './ssr_event_handler.js';"
                        
        # ============================ end ===========================
        

        # ============================================================
        # ========================== main.ts =========================
        # ============================================================
        main_ts_template = Template(Path(current_dir / 'main.ts.template').read_text(encoding='utf-8'))
        
        main_ts_cstr = main_ts_template.substitute(skeleton_theme_selector_stmt = skeleton_theme_selector_stmt,
                                                   ssr_event_handler_stmt = ssr_event_handler_stmt
            )
        write_to_bundler_dir(main_ts_cstr,
                                 "src/main.ts",
                                 target_bundler_dir=remote_svelte_bundle_dir
                                 )
                    
        # ============================ end ===========================

        


        # ========================== pyodide =========================
        if enable_inbrowser_exec:
            setup_inbrowser_kavya_exec(ssh_client_manager, remote_svelte_bundle_dir )
        
        # ============================ end ===========================

        # ============================================================
        # =================== add shadcn components ==================
        # ============================================================
        shadcn_component_install_stmt = ";".join([f"""pnpm dlx shadcn-svelte@latest add {_.lower()} --yes"""
                                                  for _ in [*page_csr_components.shadcn_components.labels, *page_csr_components.shadcn_bindvalue_components.labels]
                                                  ]
                                                 )


        # ============================ end ===========================

        # ============== prepare ShadcnComponent.svelte ==============
        # shadcn_component_import_stmt = "\n".join([f"""  

        # import * as {kebab_to_pascal(_)} from "$lib/components/ui/{_.lower()}/index.js";
        
        # """ for _ in page_csr_components.shadcn_components.labels])
        shadcn_component_import_stmt = "\n".join(page_csr_components.shadcn_components.import_stmts
        )
        
        
        kv_label_to_shadcn_comp_map = page_csr_components.shadcn_components.kv_label_to_shadcn_comp_map
        

        # scr:shadcn_component_renderer
        scr_template = Template(Path(current_dir / 'ShadcnComponent.svelte.template').read_text(encoding='utf-8'))
        # cstr: code string
        scr_cstr = scr_template.substitute(shadcn_component_import_stmt = shadcn_component_import_stmt,
                                          
                                          kv_label_to_shadcn_comp_map = kv_label_to_shadcn_comp_map                           
                                           )

        
        write_to_bundler_dir(scr_cstr,
                             "src/ShadcnComponent.svelte",
                             target_bundler_dir = remote_svelte_bundle_dir
                             )
        # ============================ end ===========================

        # ============== prepare ShadcnComponentBindValue.svelte ==============

        shadcn_bindvalue_component_import_stmts = "\n".join(page_csr_components.shadcn_bindvalue_components.import_stmts
        )
        
        
        shadcn_bindvalue_kv_label_to_shadcn_comp_map = page_csr_components.shadcn_bindvalue_components.kv_label_to_shadcn_comp_map
        

        # scr:shadcn_component_renderer
        scr_template = Template(Path(current_dir / 'ShadcnBindValueComponent.svelte.template').read_text(encoding='utf-8'))
        # cstr: code string
        scr_cstr = scr_template.substitute(shadcn_component_import_stmts = shadcn_bindvalue_component_import_stmts,
                                          
                                          kv_label_to_shadcn_comp_map = shadcn_bindvalue_kv_label_to_shadcn_comp_map                           
                                           )

        
        write_to_bundler_dir(scr_cstr,
                             "src/ShadcnBindValueComponent.svelte",
                             target_bundler_dir = remote_svelte_bundle_dir
                             )

        #. build store_shadcn_bindvalue

        publish_store_shadcn_bindvalue()
        # ============================ end ===========================

        
        

        # ============================================================
        # install csr components 
        # ============================================================
        install_csr_components(runtime_context, page_csr_components.csr_components.html_tag)

        # ============================================================
        # ======================= lucide icons =======================
        # ============================================================
        enable_lucide_icons_components = True
        publish_lucide_icons_component_render_svelte()

        

        
        # ============================================================
        # =================== ComponentRenderByType ==================
        # TODO: enable_lucide_icons_components should come for twtags_safelist
        #. TODO:  enable_shadcn_bindvalue_components = False,
        publish_component_render_by_type(enable_svg_components=True,
                                         enable_lucide_icons_components = True,
                                         enable_shadcn_bindvalue_components = True
                                         )
        
        # ============================================================

        print("Done")
        build_and_fetch_bundle(res.svelte_bundle_dir, shadcn_component_install_stmt)
        pass
