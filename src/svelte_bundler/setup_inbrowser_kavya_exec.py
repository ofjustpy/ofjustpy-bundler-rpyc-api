from .config import node_bin_path
from string import Template
from pathlib import Path
from .helper_utils import write_to_bundler_dir
current_dir = Path(__file__).parent.resolve()
def setup_inbrowser_kavya_exec(ssh_client_manager,
                               remote_bundle_dir):
    # install arraybuffer

    
    ssh_client_manager.exec_command("install pyodide",
                                    f"""cd {remote_bundle_dir}; export PATH={node_bin_path}:/home/kabiraatmonallabs/.local/share/pnpm:$PATH;
                                    pnpm install pyodide;
                                    pnpm install vite-plugin-arraybuffer;
                                    pnpm install vite-plugin-static-copy -D
                                    """)
    kavya_modules = ["addict_tracking_changes",
                     "addict_tracking_changes_fixed_attributes",
                     "py_tailwind_utils",
                     "icons_svg",
                     "signing_middleware",
                     "macropy",
                     "kavya",
                     "kavya_plugins",
                     "rst_renderer"
                     ]
    kavya_stack_zip_import_stmts = "\n".join([f"""import {mod_name}Zip from './assets/{mod_name}.zip?arraybuffer';
            """ for mod_name in kavya_modules]
                                                     )

    kavya_unpack_zip_stmts = "\n".join([f"""pyodide.unpackArchive({mod_name}Zip, "zip",)""" for mod_name in kavya_modules])

    all_dependency_whl_info = [("dpath", "dpath-2.2.0-py3-none-any.whl"),
                               ("aenum", "aenum-3.1.15-py3-none-any.whl"),
                               ("astor", "astor-0.8.1-py2.py3-none-any.whl"),
                               ("cachetools", "cachetools-6.2.4-py3-none-any.whl"),
                               ("itsdangerous", "itsdangerous-2.2.0-py3-none-any.whl"),
                               ]

    kavya_dependency_whl_import_stmts = "\n".join([f"""import {whl_info[0]}Wheel from './assets/{whl_info[1]}?arraybuffer';
            """ for whl_info in all_dependency_whl_info])

    kavya_dependency_unpack_archive_stmts = "\n".join([f"""  pyodide.unpackArchive({whl_info[0]}Wheel, "zip");
            """ for whl_info in all_dependency_whl_info]
                                                      )
            

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

    # write rst_renderer 
    ctemplate = rst_renderer_svelte_template = Template(Path(current_dir /'RstRenderer.svelte.template').read_text(encoding='utf-8'))
    cstr = ctemplate.substitute(ingest_file_import_stmts = ingest_file_import_stmts,
                                kavya_dependency_whl_import_stmts = kavya_dependency_whl_import_stmts,
                                kavya_stack_zip_import_stmts = kavya_stack_zip_import_stmts,
                                ingest_file_write_fs_stmts = ingest_file_write_fs_stmts,
                                kavya_dependency_unpack_archive_stmts = kavya_dependency_unpack_archive_stmts,
                                kavya_unpack_zip_stmts = kavya_unpack_zip_stmts
                                )
    write_to_bundler_dir(cstr,
                             "src/RstRenderer.svelte",
                             target_bundler_dir=remote_bundle_dir
                             )
            
    pass
