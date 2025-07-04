import paramiko
import os
import sys
from string import Template
from .ssh_client_manager import SSHClientManager
import tempfile
from .config import (hostname,
                     port,
                     username,
                     bundler_base_directory
                     )

def kebab_lower(label):
    modstr = "".join(c if c.islower() else f"-{c.lower()}" for c in label[1:])
    return f"""{label[0].lower()}{modstr}"""

    

                        
import_preset_stmt = ""
import_themes_stmt = ""
include_tailwind_forms_stmt = ""

typography_presets_stmt = """
.preset-typo-display-4,
  .preset-typo-display-3,
  .preset-typo-display-2,
  .preset-typo-display-1,
  .preset-typo-headline,
  .preset-typo-title,
  .preset-typo-subtitle,
  .preset-typo-caption,
  .preset-typo-menu,
  .preset-typo-button {
    color: var(--heading-font-color);
    font-family: var(--heading-font-family);
    font-weight: var(--heading-font-weight);
    @variant dark {
      color: var(--heading-font-color-dark);
    }
  }

  /* Body */
  .preset-typo-body-1,
  .preset-typo-body-2,
  .preset-typo-caption,
  .preset-typo-menu,
  .preset-typo-button {
    color: var(--heading-font-color);
    @variant dark {
      color: var(--heading-font-color-dark);
    }
  }

  /* Unique Properties */
  .preset-typo-display-4 {
    font-size: var(--text-7xl);
    @variant lg {
      font-size: var(--text-9xl);
    }
  }
  .preset-typo-display-3 {
    font-size: var(--text-6xl);
    @variant lg {
      font-size: var(--text-8xl);
    }
  }
  .preset-typo-display-2 {
    font-size: var(--text-5xl);
    @variant lg {
      font-size: var(--text-7xl);
    }
  }
  .preset-typo-display-1 {
    font-size: var(--text-4xl);
    @variant lg {
      font-size: var(--text-6xl);
    }
  }
  .preset-typo-headline {
    font-size: var(--text-2xl);
    @variant lg {
      font-size: var(--text-4xl);
    }
  }
  .preset-typo-title {
    font-size: var(--text-xl);
    @variant lg {
      font-size: var(--text-3xl);
    }
  }
  .preset-typo-subtitle {
    font-size: var(--text-base);
    font-family: var(--heading-font-family);
    color: var(--color-surface-700-300);
    @variant lg {
      font-size: var(--text-xl);
    }
  }
  .preset-typo-body-1 {
    font-size: var(--text-xl);
    @variant lg {
      font-size: var(--text-3xl);
    }
  }
  .preset-typo-body-2 {
    font-size: var(--text-lg);
    @variant lg {
      font-size: var(--text-xl);
    }
  }
  .preset-typo-caption {
    font-size: var(--text-sm);
    color: var(--color-surface-700-300);
  }
  .preset-typo-menu {
    font-weight: bold;
  }
  .preset-typo-button {
    font-weight: bold;
  }
"""
app_css_template = Template("""
@import "tailwindcss";
$include_tailwind_forms_stmt
@import '@skeletonlabs/skeleton';
@source './node_modules/@skeletonlabs/skeleton-svelte/dist';
@import "tailwindcss";
@import "tw-animate-css";
@source "safelist.txt";
@source "safelist.txt";
$import_preset_stmt

$import_themes_stmt
@custom-variant dark (&:is(.dark *));

@import "tw-animate-css";

$shadcn_theme_stmt

$typography_presets_stmt





""")

shadcn_neutral_theme_stmt = """
:root {
  /* Skeleton UI's default color palette often has a `surface` scale for neutrals,
     and `primary`, `secondary`, `tertiary` scales for accent colors.
     The exact variable names might vary slightly in Skeleton UI's source;
     these are common conventions for frameworks using Tailwind CSS.
  */

  /* Radius (typically a direct value, not color-related) */
  --radius: 0.625rem;

  /* Background and Foreground */
  /* Skeleton UI typically uses surface-50 for very light backgrounds and surface-950 for dark foregrounds in light mode. */
  --background: var(--surface-50); /* Oklch(1 0 0) - Very light, almost white. Matches surface-50 well. */
  --foreground: var(--surface-950); /* Oklch(0.147 0.004 49.25) - Very dark, almost black. Matches surface-950 well. */

  /* Card and Popover (often match background/foreground or slightly darker/lighter surface shades) */
  --card: var(--surface-50); /* Oklch(1 0 0) - Same as background, common for cards/popovers. */
  --card-foreground: var(--surface-950); /* Oklch(0.147 0.004 49.25) - Same as foreground. */
  --popover: var(--surface-50); /* Oklch(1 0 0) - Same as background. */
  --popover-foreground: var(--surface-950); /* Oklch(0.147 0.004 49.25) - Same as foreground. */

  /* Primary Colors */
  /* This maps your shadcn primary to Skeleton's primary-500 (mid-range). */
  --primary: var(--primary-500); /* Oklch(0.216 0.006 56.043) - This is a dark, almost neutral primary. */
  --primary-foreground: var(--primary-50); /* Oklch(0.985 0.001 106.423) - A very light foreground for the dark primary. */

  /* Secondary Colors */
  /* This maps your shadcn secondary to Skeleton's secondary-50 (very light). */
  --secondary: var(--secondary-50); /* Oklch(0.97 0.001 106.424) - A very light secondary. */
  --secondary-foreground: var(--secondary-900); /* Oklch(0.216 0.006 56.043) - A dark foreground for the light secondary. */

  /* Muted Colors */
  /* As per your example, mapping to surface shades. */
  --muted: var(--surface-100); /* Oklch(0.97 0.001 106.424) - A slightly darker surface than background, good for muted. */
  --muted-foreground: var(--surface-600); /* Oklch(0.553 0.013 58.071) - A mid-dark surface for muted text. */

  /* Accent Colors */
  /* This maps your shadcn accent to Skeleton's secondary-100 (slightly darker than secondary-50). */
  --accent: var(--secondary-100); /* Oklch(0.97 0.001 106.424) - Often similar to muted or a slightly different neutral. */
  --accent-foreground: var(--secondary-900); /* Oklch(0.216 0.006 56.043) - Dark foreground for the accent. */

  /* Destructive Color */
  /* Skeleton UI might have a dedicated 'error' or 'danger' scale, or you can map to a specific shade like red-600 if available. */
  --destructive: var(--error-600); /* Oklch(0.577 0.245 27.325) - A vibrant red/destructive color. */
  /* Assuming --destructive-foreground exists in Skeleton's error scale or defaults to white/light. */
  --destructive-foreground: var(--surface-50);

  /* Border and Input */
  /* Often mapped to mid-range surface or primary/secondary shades for interactive elements. */
  --border: var(--surface-300); /* Oklch(0.923 0.003 48.717) - A light-mid gray. */
  --input: var(--surface-300); /* Oklch(0.923 0.003 48.717) - Often matches border for input fields. */
  --ring: var(--primary-400); /* Oklch(0.709 0.01 56.259) - A slightly desaturated primary for focus rings. */

  /* Chart Colors (These are usually unique and less likely to map directly to core theme colors) */
  /* You might map these to specific Skeleton UI colors if they match or keep them as direct Oklch values.
     For this example, we'll assume Skeleton provides specific chart color variables or you keep them as is. */
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);

  /* Sidebar Colors (often derived from surface or primary/secondary but can be distinct) */
  --sidebar: var(--surface-100); /* Oklch(0.985 0.001 106.423) - Light background for sidebar. */
  --sidebar-foreground: var(--surface-900); /* Oklch(0.147 0.004 49.25) - Dark text for sidebar. */
  --sidebar-primary: var(--primary-500); /* Oklch(0.216 0.006 56.043) - Primary color within sidebar. */
  --sidebar-primary-foreground: var(--primary-50); /* Oklch(0.985 0.001 106.423) - Foreground for sidebar primary. */
  --sidebar-accent: var(--secondary-100); /* Oklch(0.97 0.001 106.424) - Accent within sidebar. */
  --sidebar-accent-foreground: var(--secondary-900); /* Oklch(0.216 0.006 56.043) - Foreground for sidebar accent. */
  --sidebar-border: var(--surface-300); /* Oklch(0.923 0.003 48.717) - Border within sidebar. */
  --sidebar-ring: var(--primary-400); /* Oklch(0.709 0.01 56.259) - Ring within sidebar. */
}



@theme inline {
  /* Radius (for rounded-*) */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
 
  /* Colors */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-ring: var(--ring);
  --color-radius: var(--radius);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}


@layer base {
  * {
    @apply border-border;
  }
 
  body {
    @apply bg-background text-foreground;
  }
}


@custom-variant dark (&:is(.dark *));


"""


shadcn_component_map_stmt = ""
shadcn_component_import_stmt = ""
shadcn_component_render_src_template = Template("""
<script lang="ts">
  import { initComponentMapStore, addKVIdRef } from './store_componentMap.ts';
    export let jp_props;
  export let comp_ref;
  import ComponentRenderByType from './ComponentRenderByType.svelte';
  let other_ref = null;

$shadcn_component_import_stmt
    let components =  {
                      $shadcn_component_map_stmt
                       }

    let myself_ref;

  $$:if(comp_ref && jp_props.id !== undefined) myself_ref = comp_ref;
  $$:if(comp_ref && jp_props.id !== undefined) {
  addKVIdRef(jp_props.id, myself_ref);
  console.log("adding schadcn to KVIdref");
  console.log(jp_props.id);
  console.log(myself_ref);
  console.log(other_ref);
  
  
  }

  function eventHandlerWrapper(eventType) {
    return function (event) {
        if (jp_props.events.includes(eventType)) {
        eventHandler_CSR(props, event, false);
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
  
$$: descriptionObject = {
    ...jp_props.attrs,
    style: jp_props.style,
    class: jp_props.classes, 
  };

export function updateTwClass(twClassStr){
  descriptionObject.class=twClassStr;
  console.log("updating shadcn component : ", jp_props.html_tag);
  console.log(twClassStr);
}

  



</script>

<svelte:component this={components[jp_props.html_tag]} {...descriptionObject} bind:this={other_ref}>
{#if jp_props.text}{jp_props.text}{/if}
  {#each jp_props.object_props as cobj_props}
    {#if cobj_props.show}
      <svelte:component this={ComponentRenderByType} jp_props={cobj_props}/>
    {/if}
  {/each}
{#if jp_props.inner_html}{@html jp_props.inner_html}{/if}
  </svelte:component>

""")
preset_themes = [
    "catppuccin", "cerberus", "concord", "crimson", "fennec",
    "hamlindigo", "legacy", "mint", "modern", "mona",
    "nosh", "nouveau", "pine", "reign", "rocket",
    "rose", "sahara", "seafoam", "terminus", "vintage",
    "vox", "wintry"
]



bundler_dir = f"{bundler_base_directory}/skeletonui_with_shadcnui" 
def build_bundle(twsty_str,
                 font_families=[],
                 fontawesome_icons = [],
                 ui_library="skeletonui",
                 output_dir = "./",
                 use_tailwind_forms = True,
                 skui_themes = ["crimson"],
                 shadcn_components = [],
                 shadcn_components_parts = [],
                 skui_preset_import = True,
                 shadcn_theme = "neutral"
                 ):
    
    if skui_preset_import:
        import_preset_stmt = """@import '@skeletonlabs/skeleton/optional/presets';"""
    

    for theme in skui_themes:
        assert theme in preset_themes

    if use_tailwind_forms:
        include_tailwind_forms_stmt = """@plugin '@tailwindcss/forms';"""
    import_themes_stmt = "\n".join([f"""@import '@skeletonlabs/skeleton/themes/{theme}'; """ for theme in skui_themes]
                                   )

    # ========================= safelist.txt =========================
    safelist_svelte_str= "\n".join(twsty_str)

    # Create a temporary file and write the content
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(safelist_svelte_str)
        print(f"Data written to temporary file: {temp_file.name}")


    # ============================== end =============================

    # ========================= shadcn_theme =========================

    assert shadcn_theme == "neutral"
    shadcn_theme_stmt = shadcn_neutral_theme_stmt
    # ============================== end =============================

    # ============================ app.css ===========================
    app_css_str = app_css_template.substitute(import_preset_stmt=import_preset_stmt,
                                              import_themes_stmt=import_themes_stmt,
                                              include_tailwind_forms_stmt=include_tailwind_forms_stmt,
                                              shadcn_theme_stmt = shadcn_theme_stmt,
                                              typography_presets_stmt = typography_presets_stmt
                                              )
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as app_css_temp_file:
        app_css_temp_file.write(app_css_str)
        print(f"Data written to temporary file: {app_css_temp_file.name}")


    # ShadcnComponent.svelte
    all_map_stmts = []
    for shadcn_comp, shadcn_comp_part in shadcn_components_parts:
        print(shadcn_comp, " ==> ", shadcn_comp_part)
        if shadcn_comp_part is None:
            all_map_stmts.append(f"{shadcn_comp.lower()} : {shadcn_comp}")
                        
        else:
            all_map_stmts.append(f"{shadcn_comp.lower()}_{shadcn_comp_part.lower()} : {shadcn_comp}.{shadcn_comp_part}")

    # component_map_body = ",\n ".join(f"{shadcn_comp.lower()}_{shadcn_comp_part.lower()} : {shadcn_comp}.{shadcn_comp_part}" for shadcn_comp, shadcn_comp_part in shadcn_components_parts

    # )
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
        
                    
        pass
    # component_import_body = "\n". join(f"""import * as  {comp}  from "$lib/components/ui/{kebab_lower(comp)}/index.js";""" for comp in shadcn_components)

    component_import_body = "\n".join(all_component_import_stmts
        )
    print ("component_map_body = ", component_map_body)
    print ("component_map_body = ", component_import_body)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.svelte') as shadcn_component_render_temp_file:
        shadcn_component_render_temp_file.write(shadcn_component_render_src_template.substitute(shadcn_component_map_stmt = component_map_body,
                                                                                                shadcn_component_import_stmt = component_import_body

                                                                                                )
                                                )
        

    with SSHClientManager(hostname, port, username) as ssh_client_manager:
        ssh_client_manager.put_file(temp_file.name,
                                    f"{bundler_dir}/safelist.txt")
        
    
        ssh_client_manager.put_file(app_css_temp_file.name,
                                    f"{bundler_dir}/src/app.css")

        # Install ShadcnComponent.svelte
        
        ssh_client_manager.put_file(shadcn_component_render_temp_file.name,
                                    f"{bundler_dir}/src/ShadcnComponent.svelte")

        
        ssh_client_manager.exec_command("delete bundle",
                                        f"""cd {bundler_dir}/dist;

                                        rm bundler.iife.js bundle.css""")

        # install  shadcn components

        ssh_client_manager.exec_command("remove existing shadcn components",
                                        f"""cd {bundler_dir}; 

                                        rm -rf src/lib/components/ui/* """)

        if len(shadcn_components) > 0:

            
            shadcn_components_install_cmd  = " ".join([ kebab_lower(comp)  for comp in shadcn_components]
                                                      )
            print ("shadcn_components_install_cmd = ", shadcn_components_install_cmd)
            
            ssh_client_manager.exec_command("install shadcn components",
                                            f"""cd {bundler_dir}; export PATH=/home/kabiraatmonallabs/.nvm/versions/node/v24.2.0/bin:$PATH;

                                        pnpm dlx shadcn-svelte@latest add {shadcn_components_install_cmd} --yes """)


        ssh_client_manager.exec_command("build bundle",
                                        f"""cd {bundler_dir}; export PATH=/home/kabiraatmonallabs/.nvm/versions/node/v24.2.0/bin:$PATH;
                                        pnpm run build""")

        try:
            os.remove(f"{output_dir}/bundle.iife.js")
        except:
            pass

        try:
            os.remove(f"{output_dir}/bundle.iife.js.map")
        except:
            pass

        try:
            os.remove(f"{output_dir}/style.css")

        except:
            pass

        
        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js""",
                                    f"{output_dir}/bundle.iife.js"
                                    )
        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.iife.js.map""",
                                            f"{output_dir}/bundle.iife.js.map"
                                    )


        ssh_client_manager.get_file(f"""{bundler_dir}/dist/bundle.css""",
                                    f"{output_dir}/style.css"
                                    )
        
