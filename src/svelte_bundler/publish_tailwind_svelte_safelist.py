import os
import sys
from string import Template
from .ssh_client_manager import SSHClientManager
import tempfile
from .config import (hostname,
                     port,
                     username,
                     bundler_base_directory
                     )
from svelte_safelist_builder import get_svelte_safelist
from . import runtime_context

from .tailwind_svelte_safelist  import publish_tailwind_svelte_safelist as publish_tailwind_svelte_safelist_impl

    

                        




def publish_tailwind_svelte_safelist(target_module,
                 dep_modules,

                 ):
    twtags, fontawesome_icons = get_svelte_safelist(target_module)
    print("tailwind tags = ", twtags)
    publish_tailwind_svelte_safelist_impl(twtags)
    
