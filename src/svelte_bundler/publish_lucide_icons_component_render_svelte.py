from .helper_utils import write_to_bundler_dir, kebab_lower
store_lucide_iconMap_str = """
import { readable } from 'svelte/store';

import { Home, Library, Cog, EyeOff, Trash2, Eye, Lock, Sparkle, CircleX, CircleAlert, OctagonAlert, TriangleAlert, Lightbulb, Megaphone, Info, Puzzle, Siren, ChevronRight } from '@lucide/svelte';

let iconMap_dict = {
    		 'home': Home,
		 'eye': Eye,
		 'eyeoff': EyeOff,
		 'trash2': Trash2,
		 'lock': Lock,
		 'sparkle': Sparkle,
                 'circlex': CircleX,
                 'circlealert': CircleAlert,
                 'octagonalert': OctagonAlert,
                 'trianglealert': TriangleAlert,
                 'lightbulb': Lightbulb,
                 'megaphone': Megaphone,
                 'info': Info,
                 'puzzle': Puzzle,
                 'siren': Siren,
                 'chevronright': ChevronRight
 
 
        };

export const lucide_iconMap = readable(iconMap_dict);


"""
def publish_lucide_icons_component_render_svelte(target_module,
                                                 dep_modules,
                                                 ssh_client_manager):
    write_to_bundler_dir(store_lucide_iconMap_str,
                         "src/store_lucide_iconMap.ts")
    pass
