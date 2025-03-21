import macropy.activate
from svelte_safelist_builder import get_svelte_safelist

twtags, fontawesome_icons = get_svelte_safelist("ofjustpy_webworks_website.shadcnui_component_library_showcase")

# which font families to include
font_families = ["Geist", "Roboto"]

from  svelte_bundler import  ssr_bundle_builder


ssr_bundle_builder(twtags,
                                    font_families=font_families,
                  
                                    output_dir="./"
                                    )

print(fontawesome_icons)
