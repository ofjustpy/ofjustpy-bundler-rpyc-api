import macropy.activate
from svelte_safelist_builder import get_svelte_safelist

twtags, fontawesome_icons = get_svelte_safelist("ofjustpy_webworks_website.hyperui_component_library_showcase")

# which font families to include
font_families = ["Geist", "Roboto"]

from  svelte_bundler import hyperui_bundle_builder


hyperui_bundle_builder(twtags,
                                    font_families=font_families,
                                    fontawesome_icons = fontawesome_icons,
                                    ui_library="hyperui",
                                    output_dir="./"
                                    )

print(fontawesome_icons)
