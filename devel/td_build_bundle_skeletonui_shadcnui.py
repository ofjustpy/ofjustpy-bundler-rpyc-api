import macropy.activate
from svelte_safelist_builder import get_svelte_safelist

#target_module = "ofjustpy_webworks_website.skeletonui_component_library_showcase"

target_module = "dummy_oj_webpage_with_shadcnui"
twtags, fontawesome_icons = get_svelte_safelist(target_module)


# # which font families to include
font_families = ["Geist", "Roboto"]

from  svelte_bundler import  all_in_one_bundle_builder, list_shadcn_components_in_module


shadcn_components = list_shadcn_components_in_module(target_module)

print(shadcn_components)
all_in_one_bundle_builder(twtags,
                          font_families=font_families,
                          fontawesome_icons = fontawesome_icons,
                          output_dir="static/skeleton_shadcn_uibundle",
                          shadcn_components = list(shadcn_components)
                          )


