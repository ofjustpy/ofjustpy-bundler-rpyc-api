from string import Template
from .helper_utils import write_to_bundler_dir

# TODO: Font families
def publish_tailwind_svelte_safelist(twsty_str):
    safelist_svelte_str= "\n".join(twsty_str)

    write_to_bundler_dir(safelist_svelte_str,
                         "safelist.txt")
    

