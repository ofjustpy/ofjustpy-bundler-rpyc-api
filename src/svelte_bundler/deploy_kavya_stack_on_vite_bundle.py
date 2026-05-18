"""
creat 
"""
import subprocess
import os
import zipfile
from config import ssr_style_css_dir
from ssh_client_manager import SSHClientManager
from config import (hostname,
                     port,
                     username,
                     bundler_base_directory,
                     csr_bundle_style_css_dir
                     )


BASE_DIR = """/mnt/zfs_pool/kabiraatmonallabs_extended/kabiraatmonallabs_skullsaints_home/kabiraatmonallabs/Development/Kavya"""
THIRDPARTY_BASEDIR = """/mnt/zfs_pool/kabiraatmonallabs_extended/kabiraatmonallabs_skullsaints_home/kabiraatmonallabs/Development/ThirdParty/"""
modules = [("addict-tracking-changes", "addict_tracking_changes"),
           ("addict-tracking-changes-fixed-attributes", "addict_tracking_changes_fixed_attributes"),
            ("py-tailwind-utils", "py_tailwind_utils"),
            ("kavya-icons-svg", "icons_svg"),
            ("kavya-signing-middleware", "signing_middleware"),
            ("kavya-plugins", "kavya_plugins"),
            ("kavya-engine-core", "kavya")
           ]
MONALCMS_BASE_DIR = """/mnt/zfs_pool/kabiraatmonallabs_extended/kabiraatmonallabs_skullsaints_home/kabiraatmonallabs/Development/MonalCMS/"""
monalcms_modules = [("monalcms-rst-kavya-renderer", "rst_renderer"
                     )
                    ]
third_party_modules = [("macropy", "macropy")

                       ]

current_working_dir = os.getcwd()
ingest_files = [(os.path.join(MONALCMS_BASE_DIR, "monalcms-rst-kavya-renderer",  "devel", "custom_render_directives.py"), "custom_render_directives.py"),
                (os.path.join(MONALCMS_BASE_DIR, "monalcms-rst-kavya-renderer",  "devel", "rst_sample_bullet_list.rst"), "rst_sample_bullet_list.rst"),

                (os.path.join(current_working_dir, "the_app.py"), "the_app.py")
                
            

                ]

# wheels
# dpath-2.2.0-py3-none-any.whl
# https://www.piwheels.org/simple/dpath/dpath-2.2.0-py3-none-any.whl#sha256=04814b14e16776bf9bc7456099ae1aca97603da5ca4ee5176c8d46a986ad7eef

#. aenum-3.1.15-py3-none-any.whl
#. https://www.piwheels.org/simple/aenum/aenum-3.1.15-py3-none-any.whl#sha256=623825bcae6d938728a8d7fa552e68cf04f84cf77cb7d11ea3be5362618f02e7

#. astor
#. https://www.piwheels.org/simple/astor/astor-0.8.1-py2.py3-none-any.whl#sha256=070a54e890cefb5b3739d19f30f5a5ec840ffc9c50ffa7d23cc9fc1a38ebbfc5

#. cachetools
#. https://www.piwheels.org/simple/cachetools/cachetools-6.2.4-py3-none-any.whl#sha256=8b4f305a2d48024c76a528f425b4ee378d4a3cb3154f37b86b1eaaae15bb9039

#. itsdangerous
#.  https://www.piwheels.org/simple/itsdangerous/itsdangerous-2.2.0-py3-none-any.whl#sha256=e7425c8d02b704ede8efa14c517e29b81cc42e47ac7eaf4a11fde48720b0ac20

#. typing_extensions
#. https://www.piwheels.org/simple/typing-extensions/typing_extensions-4.15.0-py3-none-any.whl#sha256=f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548

#. anyio
#. 
#. starlette
#.  https://www.piwheels.org/simple/itsdangerous/itsdangerous-2.2.0-py3-none-any.whl#sha256=e7425c8d02b704ede8efa14c517e29b81cc42e47ac7eaf4a11fde48720b0ac20


# urls for all the python wheels that kavya stack uses 
all_dep_wheel_urls = [
    ("dpath", 
    "https://www.piwheels.org/simple/dpath/dpath-2.2.0-py3-none-any.whl#sha256=04814b14e16776bf9bc7456099ae1aca97603da5ca4ee5176c8d46a986ad7eef"), 
#. aenum-3.1.15-py3-none-any.whl
("aenum", 
"https://www.piwheels.org/simple/aenum/aenum-3.1.15-py3-none-any.whl#sha256=623825bcae6d938728a8d7fa552e68cf04f84cf77cb7d11ea3be5362618f02e7"), 

#. astor
("astor", 
"https://www.piwheels.org/simple/astor/astor-0.8.1-py2.py3-none-any.whl#sha256=070a54e890cefb5b3739d19f30f5a5ec840ffc9c50ffa7d23cc9fc1a38ebbfc5"),

#. cachetools
("cachetools", 
"https://www.piwheels.org/simple/cachetools/cachetools-6.2.4-py3-none-any.whl#sha256=8b4f305a2d48024c76a528f425b4ee378d4a3cb3154f37b86b1eaaae15bb9039"),

#. itsdangerous
("itsdangerous", 
"https://www.piwheels.org/simple/itsdangerous/itsdangerous-2.2.0-py3-none-any.whl#sha256=e7425c8d02b704ede8efa14c517e29b81cc42e47ac7eaf4a11fde48720b0ac20"),

#. typing_extensions
("typing_extensions", 
"https://www.piwheels.org/simple/typing-extensions/typing_extensions-4.15.0-py3-none-any.whl#sha256=f0fa19c6845758ab08074a0cfa8b7aecb71c999ca73d62883bc25cc018c4e548"),

#. anyio
#. 
#. starlette
("starlette", "https://www.piwheels.org/simple/itsdangerous/itsdangerous-2.2.0-py3-none-any.whl#sha256=e7425c8d02b704ede8efa14c517e29b81cc42e47ac7eaf4a11fde48720b0ac20")

]


                
def create_module_zips(remote_svelte_bundle_dir = csr_bundle_style_css_dir  ):
    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        def zip_n_ship(mod_name, src_path, content_dir="."):
            output_zip = os.path.join(current_working_dir, f"{mod_name}.zip")
            # Define the output filename

            #command = f"cd '{src_path}' && zip -r '{output_zip}' ."
            command = f"cd '{src_path}' && zip -r '{output_zip}' {content_dir} -x '*__pycache__*' -x '*.pyc' -x '*~'"
            # 1. Remove existing zip if it exists
            if os.path.exists(output_zip):
                try:
                    os.remove(output_zip)
                    print(f"🗑️  Removed existing file: {output_zip}")
                except OSError as e:
                    print(f"❌ Error removing file {output_zip}: {e}")


            try:
                # Run the command
                subprocess.run(command, shell=True, check=True)
                print(f"✅ Successfully created: {output_zip}\n")

                ssh_client_manager.put_file(output_zip,
                                            f"{remote_svelte_bundle_dir}/src/assets/{mod_name}.zip"
                                            )


            except subprocess.CalledProcessError as e:
                print(f"❌ Error zipping {mod_name}: {e}")

        # end func
        
        for mod_dir_name, mod_name in third_party_modules:
            src_path = os.path.join(THIRDPARTY_BASEDIR,  mod_dir_name)
            zip_n_ship(mod_name, src_path, content_dir=mod_name)
        for mod_dir_name, mod_name in modules:
            src_path = os.path.join(BASE_DIR, mod_dir_name, "src")
            zip_n_ship(mod_name, src_path)
            
        for mod_dir_name, mod_name in monalcms_modules:
            src_path = os.path.join(MONALCMS_BASE_DIR, mod_dir_name, "src")
            zip_n_ship(mod_name, src_path)


        #ship ingest files
        ssh_client_manager.exec_command("create assets dir", 
                                        f"mkdir -p {remote_svelte_bundle_dir}/src/assets/"
                                        )

        for mod_name, mod_wheel_url in all_dep_wheel_urls:
            ssh_client_manager.exec_command(f"download wheel {mod_name}", 
                                            f"cd {remote_svelte_bundle_dir}/src/assets/; wget {mod_wheel_url}"
                                            )

        

        for ingest_file_info in ingest_files:
            src_file = ingest_file_info[0]
            target_name =  ingest_file_info[1]
            ssh_client_manager.put_file(src_file,
                                            f"{remote_svelte_bundle_dir}/src/assets/{target_name}"
                                            )
        

if __name__ == "__main__":
    create_module_zips()            
