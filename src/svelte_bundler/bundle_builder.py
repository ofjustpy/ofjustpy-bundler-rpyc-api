
import paramiko
import os
import sys
from string import Template
from font_css_config_by_family import fonts_by_family

from .ssh_client_manager import SSHClientManager, font_family_twcfg_mapping

# Example usage:

from .config import bundler_base_directory
from .config import (hostname,
                     port,
                     username
                     )


# =========================== font mappings ===========================
# adding fonts requires configuration at two places
#. 1. in app.postcss
#. 2. in tailwind.config.ts in the fontFamily section
        


# ====================================================================
safelist_svelte_template= Template("""<script lang="ts">
safe_twsty_arr = $twsty_str;
let concString = safe_twsty_arr.join(' ');



</script>

<div class={concString}></div>

<div class='$fontString'></div>

    """
                                   )

app_postcss_template = Template("""
@tailwind base;
@tailwind components;
@tailwind utilities;
@tailwind variants;

@layer base {
$font_config
}
""")


fontawesome_icons_storeMap_template = Template("""
import { readable } from 'svelte/store';
${import_icons_solid_svg_stmts}
${import_icons_regular_svg_stmts}
${import_icons_brands_svg_stmts}
${solid_iconMap_stmt}
${regular_iconMap_stmt}
${brands_iconMap_stmt}

export const solid_iconMap = readable(solid_iconMap_dict);
export const regular_iconMap = readable(regular_iconMap_dict);
export const brands_iconMap = readable(brands_iconMap_dict);

""")

tailwind_config_ts_template = {}

tailwind_config_ts_template['hyperui'] = Template("""
import { join } from 'path';
import type { Config } from 'tailwindcss';
import forms from '@tailwindcss/forms';
import plugin from 'tailwindcss/plugin';
import typography from '@tailwindcss/typography';
import { fontFamily } from "tailwindcss/defaultTheme";

export default {
   darkMode: 'class',
   content: ['./src/**/*.{html,js,svelte,ts}',
   ],
   safelist: [],
   theme: {
   extend: {
	   fontFamily: {$tw_ff_cfg}
	   ,       
	   fontWeight: {
		   '100': 100,
		   '200': 200,
		   '300': 300,
		   '400': 400,
		   '500': 500,
		   '600': 600,
		   '700': 700,
		   '800': 800,
		   '900': 900,
	   },
   },
},
plugins: [
	forms,
	typography,
]
} satisfies Config;


""")
    
local_script_path = "./build_bundle.sh"
remote_script_path = "/tmp/build_bundle.sh"
remote_files = ["/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Ofjustpy-Svelte-Tailwind-Skeleton-Bundler/dist/bundle.iife.js",
                "/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Ofjustpy-Svelte-Tailwind-Skeleton-Bundler/dist/bundle.iife.js.map",
                "/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Ofjustpy-Svelte-Tailwind-Skeleton-Bundler/dist/style.css"]  # List of remote files to SCP back
local_destination_path = "/tmp"


def build_bundle(twsty_str,
                 font_families=[],
                 fontawesome_icons = [],
                 ui_library="hyperui"):
    """
    ui_library_options: hyperui, skeletonui, shadcnui, hyperui+skeletonui, shadcnui+skeletonui, hyperui+shadcnui+skeletonui
    """

    bundler_dir = bundler_base_directory + "/" + ui_library
    
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        # Perform SSH operations using ssh_client
        ssh_client_manager.exec_command("delete bundle",
                                        """cd /home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Ofjustpy-Svelte-Tailwind-Skeleton-Bundler/dist

                                        rm bundler.iife.js bundler.iife.js.map style.css""")

        # ======================== TwSafelist ========================
        fontString = " ".join([f"font-{ff.lower()}" for ff in font_families])
        print ("fontString = ", fontString)
        safelist_svelte_str = safelist_svelte_template.substitute(twsty_str=twsty_str,
                                                                  fontString=fontString
                                                                  )
        temp_file_path = "/tmp/temp_file.txt"
        with open(temp_file_path, "w") as f:
            f.write(safelist_svelte_str)


        ssh_client_manager.put_file(temp_file_path,
                                    f"{bundler_dir}/src/TwSafelist.svelte")
        # ============================ end ===========================


        # ======================== app.postcss font config =======================

        font_config = ""

        for font_family in font_families:
            font_config += "\n".join(fonts_by_family[font_family])
            
        app_postcss_str = app_postcss_template.substitute(font_config = font_config)

        app_postcss_path = "/tmp/app_postcss.txt"
        with open(app_postcss_path, "w") as f:
            f.write(app_postcss_str)

        ssh_client_manager.put_file(app_postcss_path,
                                    f"{bundler_dir}/src/app.postcss")

        # ============================ end ===========================

        # ========== config fontFamily in tailwind.config.ts =========
        
        tw_ff_cfg = ""
        all_cfgs = []
        for font_family in font_families:
            all_cfgs.append(f"'{font_family.lower()}':" + str(font_family_twcfg_mapping[font_family.lower()]))

        tw_ff_cfg = ",\n".join(all_cfgs)
        tw_cfg_str = tailwind_config_ts_template[ui_library].substitute(tw_ff_cfg = tw_ff_cfg)
        
        tw_cfg_path = "/tmp/tailwind.cfg.ts.txt"
        with open(tw_cfg_path, "w") as f:
            f.write(tw_cfg_str)

        ssh_client_manager.put_file(tw_cfg_path,
                                    f"{bundler_dir}/tailwind.config.ts")



        # ============================ end ===========================

        # ===================== icons fontawesome ====================
        import_icons_solid_svg_stmts = ""
        import_icons_regular_svg_stmts = ""
        import_icons_brands_svg_stmts = ""
        solid_iconMap_pairs = []
        regular_iconMap_pairs = []
        brands_iconMap_pairs = []
        
        
        for  icon_label, icon_style, in fontawesome_icons:

            match icon_style:
                case "solid":
                    import_icons_solid_svg_stmts +=f"""import {{ {icon_label} }} from '@fortawesome/free-solid-svg-icons';\n"""
                    solid_iconMap_pairs.append( f"""'{icon_label}': {icon_label}""")
                    
                    pass
                case "regular":
                    import_icons_regular_svg_stmts +=f"""import {{ {icon_label} }} from '@fortawesome/free-regular-svg-icons';\n
                    """
                    regular_iconMap_pairs.append( f"""'{icon_label}': {icon_label}""")
                    
                case "brands":
                    import_icons_brands_svg_stmts +=f"""import {{ {icon_label} }} from '@fortawesome/free-brands-svg-icons';\n
                    """
                    brands_iconMap_pairs.append( f"""'{icon_label}': {icon_label}""")
                    pass
                

        solid_iconMap_stmt = ",".join(solid_iconMap_pairs)
        
        solid_iconMap_stmt = f"""let solid_iconMap_dict = {{
        {solid_iconMap_stmt}
        }};"""

        regular_iconMap_stmt = ",".join(regular_iconMap_pairs)
        regular_iconMap_stmt = f"""let regular_iconMap_dict = {{
        {regular_iconMap_stmt}
        }};"""

        brands_iconMap_stmt = ",".join(brands_iconMap_pairs)
        brands_iconMap_stmt = f"""let brands_iconMap_dict = {{
        {brands_iconMap_stmt}
        }};"""

        fontawesome_icons_storeMap_str = fontawesome_icons_storeMap_template.substitute(import_icons_solid_svg_stmts = import_icons_solid_svg_stmts,
                                                                                        import_icons_regular_svg_stmts = import_icons_regular_svg_stmts,
                                                                                        import_icons_brands_svg_stmts = import_icons_brands_svg_stmts,
                                                                                        solid_iconMap_stmt = solid_iconMap_stmt,
                                                                                        regular_iconMap_stmt = regular_iconMap_stmt,
                                                                                        brands_iconMap_stmt = brands_iconMap_stmt
                                                                                        )

        fontawesome_store_path = "/tmp/fontawesome_store.txt"
        with open(fontawesome_store_path, "w") as f:
            f.write(fontawesome_icons_storeMap_str)
        ssh_client_manager.put_file(fontawesome_store_path,
                                    f"{bundler_dir}/src/store_iconMaps.ts")


        # ============================ end ===========================

        ssh_client_manager.exec_command("build bundle",
                                        f"""cd {bundler_dir}

                                        npm run build""")

        try:
            os.remove("/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/bundle.iife.js")
        except:
            pass

        try:
            os.remove("/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/bundle.iife.js.map")
        except:
            pass

        try:
            os.remove("/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/style.css")

        except:
            pass
        

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js""",
                                    "/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/bundle.iife.js"
                                    )

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js.map""",
                                    "/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/bundle.iife.js.map"
                                    )

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/style.css""",
                                    "/home/kabiraatmonallabs/Development/Ofjustpy/core-engine/src/ofjustpy_engine/templates/js/svelte/style.css"
                                    )
