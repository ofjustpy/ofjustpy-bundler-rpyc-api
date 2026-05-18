// main.ts
import { mount } from 'svelte';
import './app.css'; // Your Tailwind/Shadcn global styles
import { scui_CSR_components } from './scui_csr_components.js';
import ComponentRenderByType from './ComponentRenderByType.svelte';

// Iterate over the JSON strings provided in the JS file
scui_CSR_components.forEach((jsonStr) => {
  try {
    const compData = JSON.parse(jsonStr);
    
    // 1. Identify the target ID from the JSON
    // The JSON has id: "/alert_1". We look for an element with that exact ID.
    const targetId = compData.id; 
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      // 2. Clear the placeholder content (optional, ensures clean slate)
      targetElement.innerHTML = '';

      // 3. Mount the Svelte component onto this specific element
      mount(ComponentRenderByType, {
        target: targetElement,
        props: {
          jp_props: compData
        }
      });
      
      console.log(`Mounted component ${targetId}`);
    } else {
      console.warn(`Target DOM element not found for ID: ${targetId}`);
    }

  } catch (e) {
    console.error("Error parsing component JSON or mounting:", e);
  }
});

