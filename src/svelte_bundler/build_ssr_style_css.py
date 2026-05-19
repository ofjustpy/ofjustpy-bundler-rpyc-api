import os
import sys
from string import Template
import importlib
from pathlib import Path
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


current_dir = Path(__file__).resolve().parent
vite_config_ts = Path(current_dir/"vite.config.ts").read_text()
vite_config_ts_pyodide = Path(current_dir/"vite.config.ts.pyodide").read_text()

def kebab_lower(label):
    modstr = "".join(c if c.islower() else f"-{c.lower()}" for c in label[1:])
    return f"""{label[0].lower()}{modstr}"""

    

                        
import_preset_stmt = ""
import_themes_stmt = ""
include_tailwind_forms_stmt = ""



def build_ssr_style_css(target_module,
                        #dep_modules,

                        output_dir = "./",
                        enable_skui_theme_selector = False,
                        additional_skui_themes = []
                 ):
    enable_fontawesome = False
    fontawesome_app_css_import_stmt = ""
    enable_event_handling = False
    enable_inbrowser_exec = False
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
        additional_skui_themes_stmt = "\n".join([f"@import '@skeletonlabs/skeleton/themes/{skeleton_ui_theme}';" for skeleton_ui_theme in additional_skui_themes

                                                  ]
                                                 )

        print("additional_skui_themes = ", additional_skui_themes_stmt)
        if enable_skui_theme_selector:
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
        
        # ========================== inbrowser exec ==========================
        enable_inbrowser_exec = res.enable_inbrowser_exec
        
        # setup vite.config.ts
        if enable_inbrowser_exec:
            write_to_bundler_dir(vite_config_ts_pyodide,
                                 "vite.config.ts",
                                 target_bundler_dir = ssr_style_css_dir

                )
        else:
            write_to_bundler_dir(vite_config_ts, 
                                 "vite.config.ts",
                                 target_bundler_dir = ssr_style_css_dir
                )
            
        
        
        if enable_inbrowser_exec:

            runtime_context.ssh_client_manager.exec_command("remove pyodide",
                                                            f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                                            pnpm install pyodide;
                                                            pnpm install vite-plugin-static-copy -D
                                                            """)
        else:
            
            runtime_context.ssh_client_manager.exec_command("remove pyodide",
                                                            f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                                            pnpm remove pyodide
                                                            """)


        # ========================== end =========================
        

        runtime_context.ssh_client_manager.exec_command("build bundle",
                                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                                        pnpm remove @fortawesome/fontawesome-free
                                                        """
                                                        )
            
        # install fontawesome
        if enable_fontawesome:
            runtime_context.ssh_client_manager.exec_command("build bundle",
                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                        pnpm install @fortawesome/fontawesome-free
""")
                    
            pass

        # TODO: do we need to add: export {{set_skui_theme}};        
        main_ts_body = f"""import {{ mount }} from 'svelte'
import './app.css'
{skeleton_theme_selector_stmt}

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
            
        if res.enable_inbrowser_exec:
            kavya_modules = ["addict_tracking_changes",
                             "addict_tracking_changes_fixed_attributes",
                             "py_tailwind_utils",
                             "icons_svg",
                             "signing_middleware",
                             "macropy",
                             "kavya",
                             "kavya_plugins",
                             "rst_renderer"]
            #mod_name = "addict_tracking_changes"
            kavya_stack_zip_import_stmts = "\n".join([f"""import {mod_name}Zip from './assets/{mod_name}.zip?arraybuffer';
            """ for mod_name in kavya_modules]
                                                     )
            kavya_unpack_zip_stmts = "\n".join([f"""pyodide.unpackArchive({mod_name}Zip, "zip",)""" for mod_name in kavya_modules])

            all_dependency_whl_info = [("dpath", "dpath-2.2.0-py3-none-any.whl"),
                                              ("aenum", "aenum-3.1.15-py3-none-any.whl"),
                                       ("astor", "astor-0.8.1-py2.py3-none-any.whl"),
                                       ("cachetools", "cachetools-6.2.4-py3-none-any.whl"),
                                       ("itsdangerous", "itsdangerous-2.2.0-py3-none-any.whl"),
                                       #("starlette", "starlette-0.50.0-py3-none-any.whl")
                                              ]
            
            #whl_info = dependency_whl_info = 
            kavya_dependency_whl_import_stmts = "\n".join([f"""import {whl_info[0]}Wheel from './assets/{whl_info[1]}?arraybuffer';
            """ for whl_info in all_dependency_whl_info])
            
            kavya_dependency_unpack_archive_stmts = "\n".join([f"""  pyodide.unpackArchive({whl_info[0]}Wheel, "zip");
            """ for whl_info in all_dependency_whl_info]
                                                              )
            # files like kavya.env, custom_render_directive etc. to be imported 
            ingest_files = [("customRenderDirective", "custom_render_directives.py"),
                            ("the_app", "the_app.py"),
                            ("rst_sample_bullet_list", "rst_sample_bullet_list.rst")

                ]

            ingest_file_import_stmts = "\n".join([f"""import {label}Content from './assets/{file_name}?raw';
            """ for label, file_name in ingest_files]
                                                 )
            ingest_file_write_fs_stmts = "\n".join([f"""
            pyodide.FS.writeFile("/home/pyodide/{file_name}", {label}Content);
            """ for label, file_name in ingest_files
                                                    ]
                                                   )
            main_ts_body = f"""import {{ mount }} from 'svelte'
import './app.css'
import {{ loadPyodide }} from 'pyodide';
import cowsayWheel from './assets/python_cowsay-1.2.2-py3-none-any.whl?arraybuffer';
{ingest_file_import_stmts}

            
{kavya_dependency_whl_import_stmts}            
{kavya_stack_zip_import_stmts}            
async function initPython() {{
  const outputDiv = document.getElementById("components");
  
  // 2. Initialize Pyodide
  let pyodide = await loadPyodide({{
    indexURL: "/pyodide"
  }});
  {ingest_file_write_fs_stmts}
  pyodide.FS.mkdir("static")
  pyodide.FS.mkdir("pyodide")            
  await pyodide.loadPackage("micropip");
  const micropip = pyodide.pyimport("micropip");
  await micropip.install([
    "json_fix", "lxml", "starlette", "ssl", "anyio","blake2signer", "fastapi", "addict", "docutils", "pygments"
  ]);
            
  // 3. Unpack the Bundled Buffer
  // No "await fetch()" needed! The data is already here in 'cowsayWheel'
  pyodide.unpackArchive(cowsayWheel, "zip");
  {kavya_dependency_unpack_archive_stmts}            
  {kavya_unpack_zip_stmts}
  console.log("Cowsay unpacked instantly from bundle.");

  // 4. Run Python
  pyodide.setStdout({{
    batched: (msg) => {{
      console.log(msg);

    }}
  }});


const loadingWindow = window.open("", "_blank");
loadingWindow.document.write("<h1>Generating Report... Please Wait.</h1>");
            
// 2. Verify
try {{
  await pyodide.runPythonAsync(`
    import os
    base_dir = "/home/pyodide/svg_data_test"
    os.environ["ICON_SVG_REPO_BASEDIR"] = base_dir
    # 2. Create the directory
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)


    # mock psutils
    import sys
    from unittest.mock import MagicMock

    # 1. Create the main psutil mock
    mock_psutil = MagicMock()

    # 2. Mock the 'cpu_percent' function (if you still need it)
    mock_psutil.cpu_percent.return_value = 10.5

    # --- THE NEW PART: Mocking Process().memory_info().rss ---

    # A. Create a mock object representing the 'Process' instance
    mock_proc_instance = MagicMock()

    # B. Create a mock object for what .memory_info() returns
    mock_mem_info = MagicMock()
    # Set the .rss attribute (e.g., return 50 MB in bytes)
    mock_mem_info.rss = 52428800 

    # C. Wire them together
    # When .memory_info() is called on the process, return our mem_info object
    mock_proc_instance.memory_info.return_value = mock_mem_info

    # D. Wire Process class to the instance
    # When psutil.Process(...) is initialized, return our process instance
    mock_psutil.Process.return_value = mock_proc_instance

    # 3. Inject the complete mock into sys.modules
    sys.modules["psutil"] = mock_psutil
    # end mock            
    import dpath
    import aenum
    import addict_tracking_changes_fixed_attributes
    import cachetools
    import py_tailwind_utils
    import icons_svg
    import lxml
    import itsdangerous
    import docutils
    import kavya
    import rst_renderer
    import pygments
    print(f"✅ rst_renderer version kavya is installed!")

    # the real deal
    import anyio
    import macropy.activate
    from rst_renderer import render_rst
    import kavya as kv
    from pathlib import Path
    from addict import Dict 
    kv.set_style('un')
    app = kv.load_app()
    rst_text = Path("rst_sample_bullet_list.rst").read_text()
    container = render_rst(rst_text)



    wp_endpoint = kv.create_endpoint(key="button",
                                     childs = [container
                                               ],

                                     title="Sample 1",
                                     skeleton_data_theme="sahara",
                                     ssr_bundle_dir = "ssr",
                                     rendering_type="SSR"
                                     )
    from unittest.mock import MagicMock

    # 1. Create the mock object
    mock_request = MagicMock()

    # 2. Setup 'path_params'
    # It must be a dictionary because the code uses **request.path_params
    mock_request.path_params = {{"id": 123}}  # Add keys if your handler needs them

    # 3. Setup 'url_for'
    # The code calls request.url_for("static", path="/"). 
    # We simply tell the mock to return a dummy string when called.
    mock_request.url_for.return_value = "/static/resource/path"

    wp = wp_endpoint(mock_request)
    print(wp.get_response_for_load_page)
    response = await wp.get_response_for_load_page(mock_request)

    html_bytes = response.body 

    # 2. Decode to get the HTML string
    html_string = html_bytes.decode("utf-8")
    import js
    new_window = js.window.open("", "_blank")

    if new_window:
        # 3. Write the HTML content into the new window
        new_window.document.write(html_string)
        
        # 4. Stop the loading spinner
        new_window.document.close()
        
        print("✅ HTML displayed in new window")
    else:
        print("❌ Popup blocked! Please allow popups for this site.")            

            
  `);
}} catch (error) {{
  console.error("❌ Installation failed:", error);
}}
            
}}
initPython();            
            


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
                                        f"""cd {ssr_style_css_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
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
