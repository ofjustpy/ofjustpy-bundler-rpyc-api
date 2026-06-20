from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

from ..helper_utils import write_to_bundler_dir
layerchart_component_render_src_template = Template("""

<script lang="ts">
  import { AreaChart } from 'layerchart';
import { BarChart } from 'layerchart';
import './user_dataset.js';
    export let jp_props;
      let other_ref = null;
  import ComponentRenderByType from './ComponentRenderByType.svelte';
    let components =  {
                          $kv_label_to_layerchart_comp_map
                       }
  
$$: descriptionObject = {
    ...jp_props.attrs,
    style: jp_props.style,
    class: jp_props.classes, 
  };

// 2. Safely grab properties directly from the window scope
    $$: resolvedRefs = (() => {
        const refs = {};
        for (const [propKey, globalKey] of Object.entries(jp_props.attrs_refs || {})) {
            if (typeof window !== 'undefined' && globalKey in window) {
                refs[propKey] = window[globalKey];
            } else {
                console.warn(`[LayerChart] Dynamic variable "$${globalKey}" not found on window object.`);
            }
        }
        return refs;
    })();

console.log("from layerchart");
console.log(jp_props);
$$: console.log("Reactive descriptionObject:", resolvedRefs);


</script>



<svelte:component this={components[jp_props.html_tag]} {...descriptionObject} {...resolvedRefs}>
      </svelte:component>
""")

#. TODO: we are skipping the import stmt for now
def publish_layerchart_svelte_component(kv_label_to_layerchart_comp_map):

    layerchart_component_render_cstr = layerchart_component_render_src_template.substitute(kv_label_to_layerchart_comp_map = kv_label_to_layerchart_comp_map

                                                    )
    write_to_bundler_dir(layerchart_component_render_cstr , "src/LayerchartComponent.svelte",
                         target_bundler_dir = remote_svelte_bundle_dir
                         )
        

            
    pass
# assumes layerchart is already installed via npm
