Steps in csr/__init__.py
------------------------
#. globals
   - set skeleton_theme_selector_stmt
     - window.set_skui_theme
     - so that python can dynamically modify skui theme
       
#. All work is done in `def build_csr_svelte_bundle`

   - set page_csr_components
     - using get_csr_components

   - set `res`
     - using get_twtags_safelist

   - set `local_svelte_bundle_dir`

   - set runtime_context
     
   - shadcn components json 
     - create `src/scui_csr_components.js`
     - using shadcn_components.json

   - csr components json (e.g. ace editor)
     - create src/csr_components.js
       - using csr_components.json
	 


   - create svelte tailwind safelist
     - create `safelist.txt`
       - using res.all_twsty_tags



   - skeleton theme
     - set additional_skui_themes_stmt
       - using additional_skui_themes
	 - which comes from (TODO)

     - set skeleton_ui_import
       - using res.skeleton_ui_theme
       - and additional_skui_themes_stmt

     - set skeleton_app_css

   - set shadcn_app_css
     - TODO: figure out wheter to use shadcn or skeleton


   - set app_css_str
     - using skeleton_ui_import
     - using skeleton_app_css
     - shadcn_app_css

   - write_to_bundler_dir
     - src/app.css
       - using app_css_str

   - ssr event handling
     - turned off for now
       - TODO: for csr look into websockets based event



   - set main_ts_cstr
     - using csr/main.ts.template
       - ssr_event_handler_stmt
       - skeleton_theme_selector_stmt
	 
	 

   - pyodide
     - call setup_inbrowser_kavya_exec
       - if pyodide is enabled

   - add/install shadcn components
     - using page_csr_components.shadcn_components.labels


   - write "src/ShadcnComponent.svelte"
     - using
       - shadcn_components.labels
       - kv_label_to_shadcn_comop_map
     
       


   - install_csr_components
     - TODO: currently does nothing

       
       
