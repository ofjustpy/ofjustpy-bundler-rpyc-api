import macropy.activate
from svelte_safelist_builder import get_svelte_safelist

twtags, fontawesome_icons = get_svelte_safelist("ofjustpy_webworks_website.shadcnui_component_library_showcase")

# which font families to include
font_families = ["Geist", "Roboto"]

from  svelte_bundler import  shadcnui_bundle_builder


shadcnui_bundle_builder(twtags,
                                    font_families=font_families,
                                    fontawesome_icons = fontawesome_icons,
                                    output_dir="./"
                                    )

print(fontawesome_icons)
