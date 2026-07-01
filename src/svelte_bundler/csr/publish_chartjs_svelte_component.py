from string import Template
from ..config import (hostname,
                     port,
                     username,
                     csr_bundle_style_css_dir as remote_svelte_bundle_dir 
                     )

from ..helper_utils import write_to_bundler_dir
# src_str="""
# <script>


# import { onMount } from 'svelte';
# 	import Chart from 'chart.js/auto';
# let data = [20, 100, 50, 12, 20, 130, 45];
# 	let labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

# 	// 1. Declare props using the Svelte 5 $props rune
# 	let { jp_props } = $props();

# 	// 2. DOM element reference replacing document.getElementById
# 	let canvasRef = $state(null);
# 	let chartInstance = null;

# 	// 3. The $effect rune handles both initial mounting and updates automatically
# 	onMount(() => {
# 		if (!canvasRef) return;

# 		// Log configuration for debugging (as in your original code)
# 		console.log("in Chart $effect");
# 		console.log("options", jp_props.cjs_cfg);

# 		// Initialize Chart.js using the template ref canvas canvasRef

# try {
# 			if (chartInstance) {
# 				chartInstance.destroy();
# 			}

# 			const ctx = canvasRef.getContext('2d');
# var chartInstance = new Chart(ctx, {
# 			options: {												
# 				maintainAspectRatio: false				
# 			},
# 			type: 'bar',
# 			data: {
# 				labels: labels,
# 				datasets: [
# 					{
# 						label: 'Unit Sales',
# 						data: data
# 					}
# 				]
# 			}
# 		});
	
# //chartInstance = new Chart(ctx, jp_props.cjs_cfg);
# 			console.log("✅ Chart.js initialized instance successfully.");
# 		} catch (error) {
# 			console.error("❌ CRITICAL: Chart.js failed to initialize component structure!");
# 			console.error("Error Message:", error.message);
# 			console.error("Stack Trace:", error.stack);
# 		}



# 		console.log("chart options", chartInstance.options);
# 		console.log("data", chartInstance.data);


# 	});
# </script>

# <canvas 
# 	bind:this={canvasRef} 
# 	id={jp_props.canvas_id} 
# 	class={jp_props.classes} 
# 	style={jp_props.style}
# />


# """

src_str="""
<script>
	import Chart from 'chart.js/auto';
	// 1. Declare props using the Svelte 5 $props rune
        //let { jp_props } = $props();
        let { jp_props, comp_ref = $bindable() } = $props();
	// 2. DOM element reference replacing document.getElementById
	let canvasRef = $state(null);
	let chartInstance = null;
export function getElement() {
        return canvasRef;
    }
/**
     * ✅ EXPORTED METHOD: Updates ChartJS configurations dynamically using a JSON path
     */
    export function update_chart_cfg(jsonPath, updatedValue) {
        if (!chartInstance) {
            console.warn("⚠️ Cannot update configuration: ChartInstance is not initialized yet.");
            return;
        }
        console.log("Inside update_chart_cfg = ", jsonPath, " ", updatedValue)
        let temp = chartInstance.config;
        let keys = jsonPath.split("/");

        if (keys[2] === "options") {
            temp = chartInstance.options;
        } else if (keys[2] === "data") {
            temp = chartInstance.data;
        } else {
            throw new Error(`Cannot deal with non-options/non-data path: ${jsonPath}`);
        }

        for (let i = 3; i < keys.length; i++) {
            if (i === keys.length - 1) {
                temp[keys[i]] = updatedValue;
                if (updatedValue) {
                    console.log("On evaluation: updatedValue = ", updatedValue);
                }
            } else {
                temp = temp[keys[i]];
                if (temp === undefined) {
                    throw new Error(`Invalid path structure: ${jsonPath}`);
                }
            }
        }

        // Trigger Chart.js to re-render the updated configurations visually
        chartInstance.update();
    }

	// 3. The $effect rune handles both initial mounting and updates automatically
	$effect(() => {
		if (!canvasRef) return;




		// Log configuration for debugging (as in your original code)
		console.log("in Chart $effect");
		console.log("options", jp_props.cjs_cfg);
		// Initialize Chart.js using the template ref canvas canvasRef

try {
			if (chartInstance) {
				chartInstance.destroy();
			}

			const ctx = canvasRef.getContext('2d');
	
                         chartInstance = new Chart(ctx, jp_props.cjs_cfg);
			
			console.log("✅ Chart.js initialized instance successfully.");

		} catch (error) {
			console.error("❌ CRITICAL: Chart.js failed to initialize component structure!");
			console.error("Error Message:", error.message);
			console.error("Stack Trace:", error.stack);
		}



		console.log("chart options", chartInstance.options);
		console.log("data", chartInstance.data);

		// 4. Cleanup function: automatically runs when the component unmounts
		// or right before jp_props changes and this effect re-runs
		return () => {
			if (chartInstance) {
				chartInstance.destroy();
				chartInstance = null;
			}
		};
	});
</script>

<canvas 
	bind:this={canvasRef} 
	id={jp_props.canvas_id} 
	class={jp_props.classes} 
	style={jp_props.style}
/>


"""

# src_str="""
# <script>
#   export let jp_props;
#   import { onMount, beforeUpdate } from "svelte";
#   import { Chart, registerables } from 'chart.js';
#   Chart.register(...registerables);
#   let all_charts = {};
#    onMount(() => {
#      console.log("in Chart.onMount");
#      console.log("options")
#      console.log(jp_props.cjs_cfg);

#      let canvasID = jp_props.canvas_id;
#      var ctx = document.getElementById(canvasID).getContext('2d');
#      //var chart = new Chart(ctx, {
#        // type: jp_props.chart_type,
#        // data: jp_props.chart_data,
#        // options: jp_props.chart_options
#        //type: jp_props.cjs_cfg.type,
# 	//data: jp_props.cjs_cfg.data,
# 	//options:jp_props.cjs_cfg.options
#      //});
#      var chart = new Chart(ctx, jp_props.cjs_cfg);
#      console.log("chart options");
#      console.log(chart.options);
#      console.log("data");
#      console.log(chart.data);
     
#      all_charts[jp_props.chart_name] = chart;
#    }
#           );
#   beforeUpdate(()=>{
#     if (all_charts[jp_props.chart_name] == null){
      
#     }
#     else{
#       console.log("destroy and recreate chart");
#       all_charts[jp_props.chart_name].destroy();
#       let canvasID = jp_props.canvas_id;
#       let ctx = document.getElementById(canvasID).getContext('2d');
#       var chart = new Chart(ctx, jp_props.cjs_cfg);
#       all_charts[jp_props.chart_name] = chart;
#       //console.log("options")
#       //console.log(jp_props.chart_options);
      
#     }
    
#   });
# </script>

# <!-- unable to fix width and height for 0px -->
# <!-- <canvas id={canvasID} class={jp_props.classes} style={jp_props.style} width={jp_props.width} height={jp_props.height}/> -->

# <canvas id={jp_props.canvas_id} class={jp_props.classes} style={jp_props.style}/>


# """

def publish_chartjs_svelte_component():

    # layerchart_component_render_cstr = src_template.substitute(
    #                                                 )
    write_to_bundler_dir(src_str , "src/ChartJSComponent.svelte",
                         target_bundler_dir = remote_svelte_bundle_dir
                         )
            
    pass
