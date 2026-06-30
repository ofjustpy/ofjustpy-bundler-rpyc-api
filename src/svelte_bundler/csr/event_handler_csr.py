
ajax_event_handling="""
import { componentMapStore, addKVIdRef } from './componentMap.svelte.js';
function applyDiffPatch(diff_patch_json) {
  try {
    const diffPatch = JSON.parse(diff_patch_json);

    if (diffPatch.type !== "diff_patch_update" || !diffPatch.data) {
      console.warn("Invalid diff_patch format");
      return;
    }

    const updates = diffPatch.data;

    for (const [elementId, details] of Object.entries(updates)) {
      const isComponent = Object.prototype.hasOwnProperty.call(componentMapStore.current, elementId);
      if (isComponent) {
      const compRef = componentMapStore.current[elementId];

  // Try to find the actual underlying DOM element wrapper (commonly .element or .dom depending on your component setup)

  const domNode =  compRef.getElement()
  

  if (domNode && domNode.tagName) {
    console.log(`component element <${domNode.tagName.toLowerCase()} id="${domNode.id}">`);
  } else {
    console.log(`component element <svelte-component id="${elementId}"> (DOM element not exposed)`);
  }
  const domDict = details.domDict || {};
      // update classes
if (domDict.hasOwnProperty('/classes')) {
  // el.className = domDict["/classes"].trim();
  console.log(`Update ignored classes for ${elementId}:`, el.className);
} else if (domDict.hasOwnProperty('/text')) {
  // el.innerText = domDict["/text"];
  console.log(`Update ignore text for ${elementId}:`, el.innerText); // Fixed original typo here (changed classes to text)
} else {
// there should be more checks to see if this is for updateChartConfig

}




  } else {
   const el = document.getElementById(elementId);
      if (!el) {
        console.warn(`Element with id '${elementId}' not found`);
        continue;
      }
  console.log(`Processing regular element <${el.tagName.toLowerCase()} id="${el.id}">`);
  const domDict = details.domDict || {};
      // update classes
      if (domDict.hasOwnProperty('/classes')) {
        el.className = domDict["/classes"].trim();
        console.log(`Updated classes for ${elementId}:`, el.className);
      }
     if (domDict.hasOwnProperty('/text')) {
        el.innerText = domDict["/text"];
        console.log(`Updated classes for ${elementId}:`, el.className);
      }
    // extend this section for future props like text, style, etc.
      const attrs = details.attrs || {};
      for  (var attr in attrs){
      if (attr === "/disabled"){
               if (attrs[attr] === "False") {
                el.removeAttribute("disabled");
                console.log(`remove disabled ${elementId}`);
               }
              if (attrs[attr] === "True") {
                 el.setAttribute("disabled", "");
                 console.log(`set disabled ${elementId} `);
              }
      } 

     }
}
    }

  } catch (err) {
    console.error("Error applying diff_patch:", err);
  }
}


async function sendEventAjax(e) {
    const currentEl = e.currentTarget;
    const data = {
    event_data: {
     event_type: e.type,
      page_id : pageConfig.id,
      data: e.data,
      id: currentEl?.id || null,
      tag: currentEl?.tagName || null,
      value: currentEl?.value || null,
      text: currentEl?.innerText || null


    },
    csrftoken: 'someothervalue'
  };

  async function handleResponse(resp) {
    if (!resp.ok) throw new Error(`HTTP error ${resp.status}`);
    const result = await resp.json();
    console.log("✅ Server response:", result);
  // Handle redirect directive if present
  if (result.redirect_to_url) {
    console.log("🔗 Redirecting to:", result.redirect_to_url);
    window.location.href = result.redirect_to_url;
    // Optional: Return a promise that never resolves to stop further execution 
    // while the browser handles the page tear-down/load.
    return new Promise(() => {});
  }

    if (result.diff_patch) {
    applyDiffPatch(result.diff_patch);
   }


    return result;
  }
    // actual POST request logic
  async function doFetch() {
    return fetch("/notify-event", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrftoken,
      },
      body: JSON.stringify(data),
      keepalive: true,
    });
  }
      try {
    const resp = await doFetch();
    await handleResponse(resp);
  } catch (err) {
    console.warn("Initial AJAX send failed, retrying...", err);

    // retry once after 1 second
    setTimeout(async () => {
      try {
        const retryResp = await doFetch();
        await handleResponse(retryResp);
      } catch (retryErr) {
        console.error("Retry failed:", retryErr);
      }
    }, 1000);
  }
    
}
async function eventHandler(e) {
  // prevent default if needed
  // e.preventDefault();
  const el = event.currentTarget;
  console.log("Current Target ID:", el.id);
  await sendEventAjax(e);
}



// Track page ready event when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Page is ready, sending page_ready event...");
if (typeof pageConfig !== "undefined" && pageConfig.hasPageReady === true) {
  // Construct a mock event object that matches what sendEventAjax expects
  const mockEvent = {
    type: "page_ready",
    currentTarget: document.body, // or document.documentElement
    data: {
      url: window.location.href,
      referrer: document.referrer,
      timestamp: Date.now()
    }
  };

  // Trigger the AJAX call
  sendEventAjax(mockEvent);
}
});


// --- Expose eventHandler globally for inline HTML calls ---
window.eventHandler = eventHandler;
"""
