from string import Template

# <svelte:component this={components[jp_props.html_tag]} {...descriptionObject} data={chartData} series = {series} bind:this={other_ref}>
# {#if jp_props.text}{jp_props.text}{/if}
#   {#each jp_props.object_props as cobj_props}
#     {#if cobj_props.show}
#       <svelte:component this={ComponentRenderByType} jp_props={cobj_props}/>
#     {/if}
#   {/each}
# {#if jp_props.inner_html}{@html jp_props.inner_html}{/if}
#   </svelte:component>

# <Chart.Container config={chartConfig} class="min-h-[200px] w-full">
#   <svelte:component this={components[jp_props.html_tag]}
#     data={chartData}
#     xScale={scaleBand().padding(0.25)}
# {...descriptionObject}   
#     axis="x"
#     seriesLayout="group"
#     tooltip={false}
#     series={series}>
#   </svelte:component>
# </Chart.Container>


  # <svelte:component this={components[jp_props.html_tag]}
    
# {...descriptionObject}   
#     xScale={scaleBand().padding(0.25)}
# >

#   </svelte:component>
  
layerchart_component_render_src_template = Template("""

<script lang="ts">
    export let jp_props;
      let other_ref = null;
  import ComponentRenderByType from './ComponentRenderByType.svelte';
import * as  Chart  from "$$lib/components/ui/chart/index.js";
  import * as Card from "$$lib/components/ui/card/index.js";
import { scaleBand } from "d3-scale";
import jsonpointer from 'jsonpointer';
import { AreaChart } from "layerchart";
import { BarChart } from "layerchart";
import TrendingUpIcon from "@lucide/svelte/icons/trending-up";
  import { curveNatural } from "d3-shape";
  import { scaleUtc } from "d3-scale";


  import ts from 'typescript';

    let components =  {
                          areachart : AreaChart,
barchart: BarChart
                       }

  let d3_assest_name_map = $d3_assest_name_map_stmt

  
$$: descriptionObject = {
    ...jp_props.attrs,
    style: jp_props.style,
    class: jp_props.classes, 
  };
console.log("from layerchart");
console.log(jp_props);
$$: console.log("Reactive descriptionObject:", descriptionObject);
const tsFnString = '(v: Date) => v.toLocaleDateString("en-US", { month: "short" })';


const transpiled = ts.transpileModule(tsFnString, {
  compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2020 }
}).outputText;

const fn = eval(transpiled);
console.log(fn(new Date())); // e.g., "Jul"

console.log("in layerchart: eval");
console.log(fn);

console.log("jsmap paths");
console.log(jp_props.jsd3map_paths);

jp_props.jsexpr_paths.forEach(path => {
      try {
        jsonpointer.set(jp_props.attrs, path, "modified");
        console.log(`Successfully modified path: $${path} (JSON Pointer: $${path})`);
      } catch (e) {
        console.error(`Error modifying path: $${path} (JSON Pointer: $${path})`, e);
      }
    });


jp_props.jsd3map_paths.forEach(item => {
    // Each item in jp_props.jsd3map_paths is an array.
    // The first element of this inner array is the path.
    const path = item[0]; 
    console.log(path);
    console.log(item[1]);
    console.log(item[1][0]);
    console.log(item[1][1]);
});

jp_props.jsd3map_paths.forEach(aitem => {
   let path; // Declare path here
   let d3module_label; // Declare d3module_label
   let d3var_label; // Declare d3var_label
      try {
        path = aitem [0]
        d3module_label = aitem[1][0]
        d3var_label = aitem[1][1]
        console.log("d3 object");
        console.log(d3var_label);
        console.log(d3_assest_name_map[d3var_label] );

      } catch (e) {
path = aitem [0]
        console.error(`Error modifying path: $${path} (JSON Pointer: $${path})`, e);
      }
    });
const chartConfig = {
    desktop: { label: "Desktop", color: "var(--chart-1)" },
  } satisfies Chart.ChartConfig;


console.log("jp_props.attrs = ", jp_props.attrs);
</script>



<svelte:component this={components[jp_props.html_tag]} {...descriptionObject}   
data = {chartData}
        xScale={scaleUtc()}
        series={[
          {
            key: "desktop",
            label: "Desktop",
            color: chartConfig.desktop.color,
          },
        ]}
        props={{
          area: {
            curve: curveNatural,
            "fill-opacity": 0.4,
            line: { class: "stroke-1" },
            motion: "tween",
          },
          xAxis: {
            format: (v: Date) => v.toLocaleDateString("en-US", { month: "short" }),
          },
        }}
      >
        {#snippet tooltip()}
          <Chart.Tooltip
            labelFormatter={(v: Date) =>
              v.toLocaleDateString("en-US", { month: "long" })}
            indicator="line"
          />
        {/snippet}
      </svelte:component>
""")

def write_layerchart_svelte_component(d3_assests, ssh_client_manager):
    map_entries = [
        f"  {component_name}: {component_name}"
        for module_name, component_name in d3_assests
    ]

    # Join all entries with a comma and wrap in curly braces for a JS object literal
    d3_assest_name_map_stmt = "{\n" + ",\n".join(map_entries) + "\n}"
    print("d3_assest_name_map_stmt = ", d3_assest_name_map_stmt)
           
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.svelte') as layerchart_component_render_temp_file:
        layerchart_component_render_temp_file.write(layerchart_component_render_src_template.substitute(d3_assest_name_map_stmt = d3_assest_name_map_stmt
                                                                                                        )

                                                    )

    print (layerchart_component_render_temp_file.name)

    ssh_client_manager.put_file(layerchart_component_render_temp_file.name,
                                f"{bundler_dir}/src/LayerChartComponent.svelte")
            
    pass
# assumes layerchart is already installed via npm
