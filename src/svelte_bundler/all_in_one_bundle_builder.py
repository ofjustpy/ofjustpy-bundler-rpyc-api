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
@custom-variant dark (&:is(.dark *));

@import "tw-animate-css";

$shadcn_theme_stmt
""")

shadcn_neutral_theme_stmt = """
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
preset_themes = [
    "catppuccin", "cerberus", "concord", "crimson", "fennec",
    "hamlindigo", "legacy", "mint", "modern", "mona",
    "nosh", "nouveau", "pine", "reign", "rocket",
    "rose", "sahara", "seafoam", "terminus", "vintage",
    "vox", "wintry"
]

bundler_dir = f"{bundler_base_directory}/all_in_one" 
def build_bundle(twsty_str,
                 font_families=[],
                 fontawesome_icons = [],
                 ui_library="skeletonui",
                 output_dir = "./",
                 use_tailwind_forms = True,
                 skui_themes = ["crimson"],
                 
                 skui_preset_import = True,
                 shadcn_theme = "neutral"
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

    # ========================= shadcn_theme =========================

    assert shadcn_theme == "neutral"
    shadcn_theme_stmt = shadcn_neutral_theme_stmt
    # ============================== end =============================

    # ============================ app.css ===========================
    app_css_str = app_css_template.substitute(import_preset_stmt=import_preset_stmt,
                                              import_themes_stmt=import_themes_stmt,
                                              include_tailwind_forms_stmt=include_tailwind_forms_stmt,
                                              shadcn_theme_stmt = shadcn_theme_stmt
                                              )
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
        
