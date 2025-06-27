from unittest.mock import patch
import importlib
import shadcnui_components
import sys

def list_imported_components_in_module(mod_name):

    all_shadcn_components = set()
    
    def wrapped_ShadcnComponent(f):
        def wrapper(*args, **kwargs):
            res =  f(*args, **kwargs)
            base_class = res.__class__.__bases__[0]
            all_shadcn_components.add(base_class.__name__)
            return res

        return wrapper


    with patch('shadcnui_components.components.Alert', new=wrapped_ShadcnComponent(shadcnui_components.components.Alert)), \
         patch('shadcnui_components.components.AlertDialog', new=wrapped_ShadcnComponent(shadcnui_components.AlertDialog)), \
         patch('shadcnui_components.components.Avatar', new=wrapped_ShadcnComponent(shadcnui_components.components.Avatar)), \
         patch('shadcnui_components.components.Breadcrumb', new=wrapped_ShadcnComponent(shadcnui_components.components.Breadcrumb)), \
         patch('shadcnui_components.components.Collapsible', new=wrapped_ShadcnComponent(shadcnui_components.components.Collapsible)), \
         patch('shadcnui_components.components.Command', new=wrapped_ShadcnComponent(shadcnui_components.components.Command)), \
         patch('shadcnui_components.components.Dialog', new=wrapped_ShadcnComponent(shadcnui_components.components.Dialog)), \
         patch('shadcnui_components.components.Drawer', new=wrapped_ShadcnComponent(shadcnui_components.components.Drawer)), \
         patch('shadcnui_components.components.Button', new=wrapped_ShadcnComponent(shadcnui_components.components.Button)), \
         patch('shadcnui_components.components.DropdownMenu', new=wrapped_ShadcnComponent(shadcnui_components.components.DropdownMenu)), \
         patch('shadcnui_components.components.HoverCard', new=wrapped_ShadcnComponent(shadcnui_components.components.HoverCard)), \
         patch('shadcnui_components.components.Menubar', new=wrapped_ShadcnComponent(shadcnui_components.components.Menubar)), \
         patch('shadcnui_components.components.Pagination', new=wrapped_ShadcnComponent(shadcnui_components.components.Pagination)), \
         patch('shadcnui_components.components.Progress', new=wrapped_ShadcnComponent(shadcnui_components.components.Progress)), \
         patch('shadcnui_components.components.RadioGroup', new=wrapped_ShadcnComponent(shadcnui_components.components.RadioGroup)), \
         patch('shadcnui_components.components.Resizable', new=wrapped_ShadcnComponent(shadcnui_components.components.Resizable)), \
         patch('shadcnui_components.components.ScrollArea', new=wrapped_ShadcnComponent(shadcnui_components.components.ScrollArea)), \
         patch('shadcnui_components.components.Separator', new=wrapped_ShadcnComponent(shadcnui_components.components.Separator)), \
         patch('shadcnui_components.components.Sheet', new=wrapped_ShadcnComponent(shadcnui_components.components.Sheet)), \
         patch('shadcnui_components.components.Skeleton', new=wrapped_ShadcnComponent(shadcnui_components.components.Skeleton)), \
         patch('shadcnui_components.components.Slider', new=wrapped_ShadcnComponent(shadcnui_components.components.Slider)):
        
        target_mod = importlib.import_module(mod_name)

    del sys.modules[mod_name]
    with patch('shadcnui_components.components.Switch', new=wrapped_ShadcnComponent(shadcnui_components.components.Switch)), \
         patch('shadcnui_components.components.Table', new=wrapped_ShadcnComponent(shadcnui_components.components.Table)), \
         patch('shadcnui_components.components.Tabs', new=wrapped_ShadcnComponent(shadcnui_components.components.Tabs)), \
         patch('shadcnui_components.components.Textarea', new=wrapped_ShadcnComponent(shadcnui_components.components.Textarea)), \
         patch('shadcnui_components.components.Label', new=wrapped_ShadcnComponent(shadcnui_components.components.Label)), \
         patch('shadcnui_components.components.Tooltip', new=wrapped_ShadcnComponent(shadcnui_components.components.Tooltip)), \
         patch('shadcnui_components.components.Accordion', new=wrapped_ShadcnComponent(shadcnui_components.components.Accordion)), \
         patch('shadcnui_components.components.Calendar', new=wrapped_ShadcnComponent(shadcnui_components.components.Calendar)), \
         patch('shadcnui_components.components.Carousel', new=wrapped_ShadcnComponent(shadcnui_components.components.Carousel)), \
         patch('shadcnui_components.components.Card', new=wrapped_ShadcnComponent(shadcnui_components.components.Card)), \
         patch('shadcnui_components.components.Checkbox', new=wrapped_ShadcnComponent(shadcnui_components.components.Checkbox)), \
         patch('shadcnui_components.components.Input', new=wrapped_ShadcnComponent(shadcnui_components.components.Input)), \
         patch('shadcnui_components.components.Select', new=wrapped_ShadcnComponent(shadcnui_components.components.Select)):

        
        target_mod = importlib.import_module(mod_name)
        
    print (all_shadcn_components)
