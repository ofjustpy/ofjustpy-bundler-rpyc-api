from unittest.mock import patch
import importlib
import shadcnui_components
import shadcnui_components as SCUI
import sys
import inspect



    
def list_shadcn_components_in_module(mod_name,
                                       dep_modules):

    print("in list_shadcn_components_in_module")
    all_shadcn_components = set()
    all_shadcn_components_parts = set()
    # map from component id
    # to javascript expression of
    # its value
    bind_value_map = {}
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
            
            assert 'value' in kwargs

            jsexpr_value = kwargs.pop('value')

            res =  self._original(*args, **kwargs)
            id = res.id
            
            print(f"got value for id = {id} : ", jsexpr_value)
            bind_value_map[id] = jsexpr_value
            base_class = res.__class__.__bases__[0]
            all_shadcn_components.add(base_class.__name__)
            all_shadcn_components_parts.add((base_class.__name__, None))

            
            return res
        def __getattr__(self, name):
            # Forward everything else to the original
            all_shadcn_components.add(self.tag_label)
            all_shadcn_components_parts.add((self.tag_label, name))
            return getattr(self._original, name)
    
    # get_svelte_safelist may have already
    # imported the target module 
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]
        
    with patch('shadcnui_components.Calendar', new=ShadcnWrapper(shadcnui_components.Calendar)), patch('shadcnui_components.RangeCalendar', new=ShadcnWrapper(shadcnui_components.RangeCalendar)), patch('shadcnui_components.Slider', new=ShadcnWrapper(shadcnui_components.Slider)):

        
        target_mod = importlib.import_module(mod_name)

    del sys.modules[mod_name]
    for dep_mod in dep_modules:
        if dep_mod in sys.modules:
            del sys.modules[dep_mod]
        
        
    return all_shadcn_components, all_shadcn_components_parts, bind_value_map
