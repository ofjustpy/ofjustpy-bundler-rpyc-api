CSR Bundler
===========

#. Source code dir
   - /mnt/zfs_pool/kabiraatmonallabs_extended/kabiraatmonallabs_skullsaints_home/kabiraatmonallabs/Development/Ofjustpy/ofjustpy-bundler-rpyc-api/src/svelte_bundler/csr
     
#. Nuts and Bolts
   - csr jsons
     - csr_components.js
     - scui_csr_components.js
   - app.css
     - skeleton theme imports 
   

main.ts
~~~~~~~
#. main.ts is build from main.ts.template
#. TODO:
   - Check if $ssr_event_handler_stmt can be replaced with
     - csr_event_handler_stmt

#. stuff that build_csr_svelte_bundle fills in for main.ts
   - $skeleton_theme_selector_stmt
   - $ssr_event_handler_stmt
     - 

RstRenderer
~~~~~~~~~~~

#. $ingest_file_write_fs_stmts
#. $kavya_dependency_unpack_archive_stmts
#. $kavya_unpack_zip_stmts
#.    

Dependencies
------------

#. /home/kabiraatmonallabs/Development/Ofjustpy/py-tailwind-utils/font_bank


#. ssr_bundle_builder
   - fontawesome svg core is included by default
