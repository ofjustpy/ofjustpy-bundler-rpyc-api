import sys
import importlib
from string import Template
from .helper_utils import write_to_bundler_dir, kebab_lower
from .config import bundler_dir, node_bin_path
from .scui_patch_hooks import list_shadcn_components_in_module

shadcn_component_map_stmt = ""
shadcn_component_import_stmt = ""

component_render_src_template = Template("""
<script lang="ts">
  import { initComponentMapStore, addKVIdRef } from './store_componentMap.ts';
  import ComponentRenderByType from './ComponentRenderByType.svelte';

$shadcn_component_import_stmt
$import_var_stmts
let { jp_props, comp_ref } = $$props();
let other_ref = null;
let event_props = {};
event_props['jp_props'] = jp_props;

let components =  {
                      $shadcn_component_map_stmt
                       }

let myself_ref;

$$effect(() => {
  if (comp_ref && jp_props.id !== undefined) {
    myself_ref = comp_ref;
    addKVIdRef(jp_props.id, myself_ref);
    console.log("adding schadcn to KVIdref");
    console.log(jp_props.id);
    console.log(myself_ref);
    console.log(other_ref);
  }
   });


  function eventHandlerWrapper(eventType) {
    return function (event) {
        if (jp_props.events.includes(eventType)) {
        eventHandler_CSR(event_props, event, false);
      }
    };
  }

 function handleDoubleClick(event) {
        //console.log("Double-clicked!");
        
        // You can perform additional actions here
    }
    
  const eventHandlers = {
    click: eventHandlerWrapper('click'),
    change: eventHandlerWrapper('change'),
    submit: eventHandlerWrapper('submit'),
    mouseover: eventHandlerWrapper('mouseover'),
    mouseenter: eventHandlerWrapper('mouseenter'),
    mouseleave: eventHandlerWrapper('mouseleave'),
    mouseout: eventHandlerWrapper('mouseout'),
    dblclick: eventHandlerWrapper('dblclick'),
  };



let descriptionObject = {
    ...jp_props.attrs,
    style: jp_props.style,
    class: jp_props.classes, 
  };

export function updateTwClass(twClassStr){
  descriptionObject.class=twClassStr;
  console.log("updating shadcn component : ", jp_props.html_tag);
  console.log(twClassStr);
}

let value = $state("to-be-decided")

let Component = components[jp_props.html_tag];

$$effect(() => {
  // This code runs whenever 'value' changes.
  // We check if 'value' is defined to avoid running on initial component setup.

    
    // Create a mock event object with the required structure.
    const mockEvent = { 
      type: 'change',
      data: null, // You can put any custom data you need here
      target: { 
        value: value
      }};

 console.log("here");
    // Call your change handler with the crafted event object.
    eventHandlers.change(mockEvent);
  }
);

</script>


<Component  {...descriptionObject} bind:value type="single" bind:this={other_ref}>
{#if jp_props.text}{jp_props.text}{/if}
  {#each jp_props.object_props as cobj_props}
    {#if cobj_props.show}
      <ComponentRenderByType jp_props={cobj_props}/>
    {/if}
  {/each}
{#if jp_props.inner_html}{@html jp_props.inner_html}{/if}
</Component>

""")




import jsexprs.macro_module as jsexprs_mm    
def publish_shadcn_component_render_svelte(target_module,
                                           dep_modules,
                                           ssh_client_manager):
    #install shadcn
    


    shadcn_components, shadcn_components_parts = list_shadcn_bind_value_components_in_module(target_module, dep_modules)
    if len(shadcn_components) == 0:
        return 




    shadcn_components_install_cmd  = " ".join([ kebab_lower(comp)  for comp in shadcn_components]
                                              )


                
    ssh_client_manager.exec_command("install shadcn components",
                                    f"""cd {bundler_dir}; export PATH={node_bin_path}:$PATH;
                                    
                                    pnpm dlx shadcn-svelte@latest add {shadcn_components_install_cmd} --yes;
                                    """)
                

    all_map_stmts = []
    for shadcn_comp, shadcn_comp_part in shadcn_components_parts:
        print(shadcn_comp, " ==> ", shadcn_comp_part)
        if shadcn_comp_part is None:
            all_map_stmts.append(f"{shadcn_comp.lower()} : {shadcn_comp}")

        else:
            all_map_stmts.append(f"{shadcn_comp.lower()}_{shadcn_comp_part.lower()} : {shadcn_comp}.{shadcn_comp_part}")

    component_map_body = ",\n ".join(all_map_stmts

                                     )
    
    def is_subpart_none(comp_label):
        """
        components like Badge .. do not have subpart;
        
        
        """
        for comp_label, comp_subpart in shadcn_components_parts:
            if comp_label == comp:
                if comp_subpart == None:
                    return True

                return False            
    all_component_import_stmts = []
    for comp in shadcn_components:
        if is_subpart_none(comp):
            all_component_import_stmts.append(f"""import {{ {comp} }} from "$lib/components/ui/{kebab_lower(comp)}/index.js";"""
            

                                              )
        else:
            all_component_import_stmts.append(f"""import * as  {comp}  from "$lib/components/ui/{kebab_lower(comp)}/index.js";""")
        
                    
    component_import_body = "\n".join(all_component_import_stmts
                                      )
    print ("component_map_body = ", component_map_body)
    print ("component_map_body = ", component_import_body)


    shadcn_component_render_src_str = shadcn_component_render_src_template.substitute(shadcn_component_map_stmt = component_map_body,
                                                                                                shadcn_component_import_stmt = component_import_body,
                                                                                      import_var_stmts = import_var_stmts
                                                                                                )


    shadcn_bind_value_component_render_src_template.substitute(shadcn_component_map_stmt = component_map_body,
                                                                                                shadcn_component_import_stmt = component_import_body,
                                                                                      import_var_stmts = import_var_stmts,
                                                               bind_var_label=bind_var_label,
                                                               

        )
    write_to_bundler_dir(shadcn_component_render_src_str,
                         "src/ShadcnBindValueComponent.svelte")
    

    



# from unittest.mock import patch
# import importlib
# import shadcnui_components
# import shadcnui_components as SCUI
# import sys
# import inspect
# from shadcnui_components.components import BindValueMixin


    
# def publish_shadcn_bind_value_components(mod_name,
#                                        dep_modules):
#     class ShadcnWrapper:
#         def __init__(self, original_component):
#             self._original = original_component
#             self.gen_component_description = False
#             self.needs_bind_value_component = False
#             if inspect.isfunction(original_component):
#                 id_assigner_func = original_component.__closure__[0].cell_contents
#                 comp_class = id_assigner_func.__closure__[0].cell_contents
            
#             elif inspect.isclass(original_component):
#                 comp_class = original_component


#             if issubclass(comp_class, BindValueMixin):
#                 self.needs_bind_value_component = True

#         def __call__(self, *args, **kwargs):
#             res =  self._original(*args, **kwargs)
#             if self.needs_bind_value_component:
#                 res.


            
#             return res
#         def __getattr__(self, name):
#             assert False


#     if mod_name in sys.modules:
#         del sys.modules[mod_name]

#     for dep_mod in dep_modules:
#         if dep_mod in sys.modules:
#             del sys.modules[dep_mod]
        
#     with patch('shadcnui_components.Alert', new=ShadcnWrapper(shadcnui_components.components.Alert)), \
#                   patch('shadcnui_components.Slider', new=ShadcnWrapper(shadcnui_components.Slider)):
#         target_mod = importlib.import_module(mod_name)
