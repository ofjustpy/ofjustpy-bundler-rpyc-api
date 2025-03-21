#. Create bundle and put it in in output dir
   
.. code-block::

   import macropy.activate
   from svelte_safelist_builder import get_svelte_safelist
   twtags, fontawesome_icons = get_svelte_safelist("example_008")


   # which font families to include
   font_families = []

   from  svelte_bundler import hyperui_bundle_builder

   hyperui_bundle_builder(twtags,
				       font_families=font_families,
				       fontawesome_icons = fontawesome_icons,
				       ui_library="hyperui",
				       output_dir="./static/hyperui"
				       )



#. To use the bundle
   
   .. code-block::
      
      wp_endpoint = oj.create_endpoint(key="example_008",
                                 childs = [fa_icons_section,
                                           md_icons_section],
                                 title="example_008"
                                 csr_bundle_dir = "hyperui"
                                 )





   - which will pick the bundle from
     
     .. code-block::
	<script src="/static/{csr_bundle_dir}bundle.iife.js"></script>
