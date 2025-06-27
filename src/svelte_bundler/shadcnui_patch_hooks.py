from unittest.mock import patch
import importlib
import shadcnui_components
import shadcnui_components as SCUI
import sys
import inspect



    
def list_imported_components_in_module(mod_name,
                                       dep_modules):

    all_shadcn_components = set()
    all_shadcn_components_parts = set()
    class ShadcnWrapper:
        def __init__(self, original_component):
            self._original = original_component

            # --- Documentation Note ---
            #
            # **Understanding `assign_id` and Component Recovery**
            #
            # The `assign_id` function takes an `html_component_generator` (hc_gen, our 'y')
            # and applies an `@id_assigner` decorator to an inner `func`.
            # The function returned by `assign_id` (our 'x') is actually the *wrapper*
            # function created by the `@id_assigner` decorator.
            #
            # Due to Python's closures, the original `hc_gen` ('y') is nested within
            # two levels of closures:
            #
            # 1. The outermost function (`x`) is the decorator's wrapper. Its closure
            #    contains the `func` that was originally decorated.
            # 2. This `func` (the one captured by the decorator's wrapper) has its
            #    own closure, which contains the original `hc_gen` ('y').
            #
            # Therefore, to recover 'y' from 'x':
            #
            # `y = x.__closure__[0].cell_contents.__closure__[0].cell_contents`
            #
            # This sequence accesses the first captured variable in the wrapper's
            # closure (which is the decorated 'func'), and then accesses the first
            # captured variable in that 'func's closure (which is the original 'hc_gen').
            #
            # ---
            if inspect.isfunction(original_component):
                id_assigner_func = original_component.__closure__[0].cell_contents
                comp_class = id_assigner_func.__closure__[0].cell_contents
            
                self.tag_label = comp_class.__bases__[0].__name__
            elif inspect.isclass(original_component):
                self.tag_label = original_component.__bases__[0].__name__
            else:
                assert False

        def __call__(self, *args, **kwargs):
            res =  self._original(*args, **kwargs)
            base_class = res.__class__.__bases__[0]
            print("now adding component = ", base_class.__name__)
            
            all_shadcn_components.add(base_class.__name__)
            all_shadcn_components_parts.add((base_class.__name__, None))

        def __getattr__(self, name):
            # Forward everything else to the original
            all_shadcn_components.add(self.tag_label)
            all_shadcn_components_parts.add((self.tag_label, name))
            return getattr(self._original, name)
    
    # def wrapped_ShadcnComponent(f):
    #     def wrapper(*args, **kwargs):
    #         print("wrapper invoked")
    #         res =  f(*args, **kwargs)
    #         base_class = res.__class__.__bases__[0]
    #         all_shadcn_components.add(base_class.__name__)
    #         print ("found = ", base_class.__name__)
    #         return res

    #     return wrapper


    # get_svelte_safelist may have already
    # imported the target module 
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]
        
    with patch('shadcnui_components.Alert', new=ShadcnWrapper(shadcnui_components.components.Alert)), \
         patch('shadcnui_components.AlertDialog', new=ShadcnWrapper(shadcnui_components.AlertDialog)), \
         patch('shadcnui_components.Badge', new=ShadcnWrapper(shadcnui_components.components.Badge)), \
         patch('shadcnui_components.Breadcrumb', new=ShadcnWrapper(shadcnui_components.components.Breadcrumb)), \
         patch('shadcnui_components.Collapsible', new=ShadcnWrapper(shadcnui_components.components.Collapsible)), \
         patch('shadcnui_components.ContextMenu', new=ShadcnWrapper(shadcnui_components.components.ContextMenu)), \
         patch('shadcnui_components.Command', new=ShadcnWrapper(shadcnui_components.components.Command)), \
         patch('shadcnui_components.Dialog', new=ShadcnWrapper(shadcnui_components.Dialog)), \
         patch('shadcnui_components.Drawer', new=ShadcnWrapper(shadcnui_components.Drawer)), \
         patch('shadcnui_components.Button', new=ShadcnWrapper(shadcnui_components.Button)), \
         patch('shadcnui_components.DropdownMenu', new=ShadcnWrapper(shadcnui_components.DropdownMenu)), \
         patch('shadcnui_components.HoverCard', new=ShadcnWrapper(shadcnui_components.HoverCard)), \
         patch('shadcnui_components.Menubar', new=ShadcnWrapper(shadcnui_components.Menubar)), \
         patch('shadcnui_components.NavigationMenu', new=ShadcnWrapper(shadcnui_components.NavigationMenu)), \
         patch('shadcnui_components.Popover', new=ShadcnWrapper(shadcnui_components.Popover)), \
         patch('shadcnui_components.Pagination', new=ShadcnWrapper(shadcnui_components.Pagination)), \
         patch('shadcnui_components.Progress', new=ShadcnWrapper(shadcnui_components.Progress)), \
         patch('shadcnui_components.RadioGroup', new=ShadcnWrapper(shadcnui_components.RadioGroup)), \
         patch('shadcnui_components.Resizable', new=ShadcnWrapper(shadcnui_components.Resizable)), \
         patch('shadcnui_components.ScrollArea', new=ShadcnWrapper(shadcnui_components.ScrollArea)), \
         patch('shadcnui_components.Separator', new=ShadcnWrapper(shadcnui_components.Separator)):

        
        target_mod = importlib.import_module(mod_name)

    del sys.modules[mod_name]
    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]
        
    with patch('shadcnui_components.Sheet', new=ShadcnWrapper(shadcnui_components.Sheet)), \
         patch('shadcnui_components.Skeleton', new=ShadcnWrapper(shadcnui_components.Skeleton)), \
         patch('shadcnui_components.Switch', new=ShadcnWrapper(shadcnui_components.Switch)), \
         patch('shadcnui_components.Slider', new=ShadcnWrapper(shadcnui_components.Slider)), \
         patch('shadcnui_components.Table', new=ShadcnWrapper(shadcnui_components.Table)), \
         patch('shadcnui_components.Avatar', new=ShadcnWrapper(shadcnui_components.Avatar)), \
         patch('shadcnui_components.Tabs', new=ShadcnWrapper(shadcnui_components.Tabs)), \
         patch('shadcnui_components.Textarea', new=ShadcnWrapper(shadcnui_components.Textarea)), \
         patch('shadcnui_components.Label', new=ShadcnWrapper(shadcnui_components.Label)), \
         patch('shadcnui_components.Tooltip', new=ShadcnWrapper(shadcnui_components.Tooltip)), \
         patch('shadcnui_components.Accordion', new=ShadcnWrapper(shadcnui_components.Accordion)), \
         patch('shadcnui_components.Calendar', new=ShadcnWrapper(shadcnui_components.Calendar)), \
         patch('shadcnui_components.Carousel', new=ShadcnWrapper(shadcnui_components.Carousel)), \
         patch('shadcnui_components.Card', new=ShadcnWrapper(shadcnui_components.Card)), \
         patch('shadcnui_components.Checkbox', new=ShadcnWrapper(shadcnui_components.Checkbox)
               ):

        
        
        target_mod = importlib.import_module(mod_name)
         
    del sys.modules[mod_name]
    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]

    
    with patch('shadcnui_components.Select', new=ShadcnWrapper(shadcnui_components.Select)),\
         patch('shadcnui_components.Input', new=ShadcnWrapper(shadcnui_components.Input)):
        target_mod = importlib.import_module(mod_name)
        
    return all_shadcn_components, all_shadcn_components_parts
