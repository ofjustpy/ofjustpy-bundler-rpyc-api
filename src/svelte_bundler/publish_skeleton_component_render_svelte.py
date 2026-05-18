import sys
import importlib
from string import Template
from .helper_utils import write_to_bundler_dir, kebab_lower
from .config import bundler_dir, node_bin_path
from .skui_patch_hooks import list_skeleton_components_in_module

shadcn_component_map_stmt = ""
shadcn_component_import_stmt = ""


def publish_skeleton_component_render_svelte(target_module,
                                           
                                           dep_modules,
                                           import_var_stmts,
                                           ssh_client_manager):

    
    shadcn_components, shadcn_components_parts = list_shadcn_components_in_module(target_module, dep_modules)
    print("shadcn_components = ", shadcn_components)
    if len(shadcn_components) == 0:
        return False




    shadcn_components_install_cmd  = " ".join([ kebab_lower(comp)  for comp in shadcn_components]
                                              )
    print ("shadcn_components_install_cmd = ", shadcn_components_install_cmd)

    ssh_client_manager.exec_command("remove existing shadcn components",
                                    f"""cd {bundler_dir}; 

                                    rm -rf src/lib/components/ui/* """)
                
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



    write_to_bundler_dir(shadcn_component_render_src_str,
                         "src/ShadcnComponent.svelte")
    
    return True
