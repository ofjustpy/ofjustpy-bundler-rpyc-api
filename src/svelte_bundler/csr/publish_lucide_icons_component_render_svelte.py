from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

from ..helper_utils import write_to_bundler_dir
store_lucide_iconMap_str = """
import { readable } from 'svelte/store';

import { Home, Library, Cog, EyeOff, Trash2, Eye, Lock, Sparkle, CircleX, CircleAlert, OctagonAlert, TriangleAlert, Lightbulb, Megaphone, Info, Puzzle, Siren, ChevronRight, ChevronsUpDown, Settings, CreditCard, User, Smile, Calendar, Calculator } from '@lucide/svelte';

let iconMap_dict = {
    		 'home': Home,
		 'eye': Eye,
		 'eye-off': EyeOff,
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
                 'chevronright': ChevronRight,
                 'chevrons-up-down': ChevronsUpDown,
                 'settings': Settings,
                 'credit-card': CreditCard,
                 'user': User,
                 'smile': Smile,
                 'calendar': Calendar,
                 'calculator': Calculator
 
 
        };

export const lucide_iconMap = readable(iconMap_dict);


"""
def publish_lucide_icons_component_render_svelte():
    write_to_bundler_dir(store_lucide_iconMap_str,
                         "src/store_lucide_iconMap.ts",
                         target_bundler_dir = remote_svelte_bundle_dir)
    pass
