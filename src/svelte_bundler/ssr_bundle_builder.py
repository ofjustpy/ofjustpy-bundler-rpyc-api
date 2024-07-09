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

tailwind_config_ts_template = {}
tailwind_config_ts_template['ssr'] = Template("""
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


#bundler_dir = bundler_base_directory + "/" + ui_library
bundler_dir = "/home/kabiraatmonallabs/to_githubcodes/org-ofjustpy/Bundler_By_UI/ssr"

def build_bundle(twsty_str,
                 font_families=[],
                 ui_library="ssr",
                 output_dir = "./"
                 ):
    """
    ui_library_options: hyperui, 
    """


    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        # Perform SSH operations using ssh_client
        ssh_client_manager.exec_command("delete bundle",
                                        f"""cd {bundler_dir}/dist;

                                        rm bundler.iife.js bundler.iife.js.map style.css""")

        # ======================== TwSafelist ========================
        fontString = " ".join([f"font-{ff.lower()}" for ff in font_families])
        safelist_svelte_str = safelist_svelte_template.substitute(twsty_str=twsty_str,
                                                                  fontString=fontString
                                                                  )
        temp_file_path = "/tmp/temp_file.txt"
        with open(temp_file_path, "w") as f:
            f.write(safelist_svelte_str)


        ssh_client_manager.put_file(temp_file_path,
                                    f"{bundler_dir}/src/TwSafelist.svelte")
        os.remove(temp_file_path)
        # ============================ end ===========================


        # ======================== app.postcss font config =======================

        # directives to import fonts in app.postcss
        font_config = ""

        for font_family in font_families:
            font_config += "\n".join(fonts_by_family[font_family])
            
        app_postcss_str = app_postcss_template.substitute(font_config = font_config)

        app_postcss_path = "/tmp/app_postcss.txt"
        with open(app_postcss_path, "w") as f:
            f.write(app_postcss_str)

        ssh_client_manager.put_file(app_postcss_path,
                                    f"{bundler_dir}/src/app.postcss")

        os.remove(app_postcss_path)
        
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

        os.remove(tw_cfg_path)

        # ============================ end ===========================


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

        ssh_client_manager.get_file(f"""{bundler_dir}/dist/style.css""",
                                    f"{output_dir}/style.css"
                                    )
