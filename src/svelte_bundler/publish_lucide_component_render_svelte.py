
store_lucide_iconMap_str = """
import { readable } from 'svelte/store';

import { Home, Library, Cog, EyeOff, Trash2, Eye, Lock, Sparkle } from '@lucide/svelte';

let iconMap_dict = {
    		 'home': Home,
		 'eye': Eye,
		 'eyeoff': EyeOff,
		 'trash2': Trash2,
		 'lock': Lock,
		 'sparkle': Sparkle,

        };

export const lucide_iconMap = readable(iconMap_dict);


"""
def publish_lucide_icons_component_render_svelte(target_module,
                                                 dep_modules,
                                                 ssh_client_manager):
    write_to_bundler_dir(store_lucide_iconMap_str,
                         "src/store_lucide_iconMap.ts")
    pass
