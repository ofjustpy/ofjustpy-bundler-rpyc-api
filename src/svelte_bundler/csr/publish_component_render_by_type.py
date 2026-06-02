from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

component_render_by_type_template = Template("""
<script lang="ts">
   import Htmlcomponents from './Htmlcomponents.svelte';
   import PlainTextComponent from './PlainTextComponent.svelte';
   import SVGComponent from './SVGComponent.svelte';

   let components = { 'html_component': Htmlcomponents,
                      'svg_component': SVGComponent,
                      'plaintext_component': PlainTextComponent,
                      $component_map_jsstr
                    }
                    ;
   export let jp_props;
   let comp_ref;


   
</script>

<svelte:component this={components[jp_props.vue_type]} bind:this={comp_ref} jp_props={jp_props} comp_ref={comp_ref}  />

"""
    )


    

from ..helper_utils import write_to_bundler_dir

def publish_component_render_by_type(enable_svg_components=False,
                                     enable_fontawesome_components = False,
                                     enable_shadcn_components = True,
                                     enable_shadcn_bindvalue_components = False,
                                     enable_skeleton_components = False,
                                     enable_lucide_icons_components = False,
                                     enable_shadcn_layerchart_components=False):
    component_map_stmts = []
    component_import_stmts = []
    if enable_svg_components:
        component_map_stmts.append("'svg_component': SVGComponent")
        component_import_stmts.append("import SVGComponent from './SVGComponent.svelte';")

    if enable_shadcn_components:
        component_map_stmts.append("'shadcnui_component': ShadcnComponent")
        component_import_stmts.append("import ShadcnComponent from './ShadcnComponent.svelte';")

    if enable_shadcn_bindvalue_components:
        component_map_stmts.append("'shadcnui_bind_value_component': ShadcnComponentBindValue")
        component_import_stmts.append("import ShadcnComponentBindValue from './ShadcnBindValueComponent.svelte';")


    if enable_lucide_icons_components:
        component_map_stmts.append("'lucide_component': LucideComponent,")
        component_import_stmts.append("import LucideComponent from './LucideComponent.svelte';;")

        
        
    component_import_jsstr = "\n".join(component_import_stmts)
    component_map_jsstr = "\n".join(component_map_stmts)

    component_render_by_type_str = component_render_by_type_template.substitute(component_map_jsstr = component_map_jsstr,
                                                 component_import_jsstr = component_import_jsstr
                                                 )
    write_to_bundler_dir(component_render_by_type_str , "src/ComponentRenderByType.svelte",
                         target_bundler_dir = remote_svelte_bundle_dir
                         )
