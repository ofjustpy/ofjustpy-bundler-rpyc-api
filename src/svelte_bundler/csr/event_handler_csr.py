
ajax_event_handling="""
import { componentMapStore, addKVIdRef } from './componentMap.svelte.js';
export function applyDiffPatch(diff_patch_json) {
    const diffPatch = JSON.parse(diff_patch_json);
    applyDiffPatchImpl(diffPatch);
}


export function applyDiffPatchImpl(diffPatch){
    try{
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
  } else {
    console.log(`component element <svelte-component id="${elementId}"> (DOM element not exposed)`);
  }
  const domDict = details.domDict || {};
// Loop through each key/value pair inside domDict
for (const [key, value] of Object.entries(domDict)) {
  
  switch (key) {
    case '/classes':
      // compRef/el.className = value.trim();
      console.log(`Update ignored classes for ${elementId}:`, el.className);
      break;

    case '/text':
      // compRef/el.innerText = value;
      console.log(`Update ignore text for ${elementId}:`, el.innerText);
      break;

    default:
      // If the key is not explicitly '/classes' or '/text', treat it as a chart config update
      if (isComponent && typeof compRef.update_chart_cfg === 'function') {
        console.log(`Forwarding configuration update to chart [${key}]:`, value);
        compRef.update_chart_cfg(key, value);
      } else {
        console.warn(`Unrecognized domDict property '${key}' for non-chart element ${elementId}`);
      }
      break;
  }
}





  } else {
   const el = document.getElementById(elementId);
      if (!el) {
        console.warn(`Element with id '${elementId}' not found`);
        continue;
      }

  const domDict = details.domDict || {};
      // update classes
      if (domDict.hasOwnProperty('/classes')) {
        el.className = domDict["/classes"].trim();
      }
     if (domDict.hasOwnProperty('/text')) {
        el.innerText = domDict["/text"];
      }
    // extend this section for future props like text, style, etc.
      const attrs = details.attrs || {};
      for  (var attr in attrs){
      if (attr === "/disabled"){
               if (attrs[attr] === "False") {
                el.removeAttribute("disabled");
               }
              if (attrs[attr] === "True") {
                 el.setAttribute("disabled", "");
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
     event_type: e.type ?? null,
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
  // Handle redirect directive if present
  if (result.redirect_to_url) {
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

// Map to track active hover timers and states per element
const activeHoverStates = new Map();
const debounceTimers = new Map();

function eventHandler(e) {


  // Always use currentTarget (the element bound to the listener) to maintain a single identity
  const element = e.currentTarget || e.target;
  if (!element) return;

  const eventType = e.type;

  // Handle Mouse Enter / Mouse Over (Hover Rest Detection)
  if (eventType === 'mouseenter' || eventType === 'mouseover') {
      e.stopPropagation();
    // Clear any existing pending leave or enter timer for this element
    if (activeHoverStates.has(element)) {
      clearTimeout(activeHoverStates.get(element).timer);
    }

    const syntheticEvent = createSyntheticEvent(e, element);

    // Set a delay threshold (e.g., 300ms) to ensure the mouse has actually rested
    const timer = setTimeout(() => {
      sendEventAjax(syntheticEvent);
      // Mark as currently hovered
      const state = activeHoverStates.get(element) || {};
      activeHoverStates.set(element, { ...state, isHovered: true, timer: null });
    }, 300);

    activeHoverStates.set(element, { isHovered: false, timer });
    return;
  }

  // Handle Mouse Leave / Mouse Out
  if (eventType === 'mouseleave' || eventType === 'mouseout') {
   e.stopPropagation();
    const currentState = activeHoverStates.get(element);

    if (currentState) {
      clearTimeout(currentState.timer);

      // If hover rested long enough to fire enter, fire leave after brief delay
      if (currentState.isHovered) {
        const syntheticEvent = createSyntheticEvent(e, element);
        
        const timer = setTimeout(() => {
          sendEventAjax(syntheticEvent);
          activeHoverStates.delete(element);
        }, 100);

        activeHoverStates.set(element, { ...currentState, timer });
      } else {
        // Mouse left before the hover delay threshold; cancel enter entirely
        activeHoverStates.delete(element);
      }
    }
    return;
  }

  // Standard debouncing for non-hover events (e.g., clicks)
  handleStandardEvent(e, element);
}

function createSyntheticEvent(e, element) {
  return {
    type: e.type,
    data: e.data || null,
    target: {
      id: e.target?.id || null,
      tagName: e.target?.tagName || null,
      value: e.target?.value || null,
    },
    currentTarget: {
      id: element.id || null,
      tagName: element.tagName || null,
      value: element.value || null,
    }
  };
}

function handleStandardEvent(e, element) {
  console.log("handling standard event");
  const eventKey = `${element.id || 'global'}:${e.type}`;
  if (debounceTimers.has(eventKey)) {
    clearTimeout(debounceTimers.get(eventKey));
  }

  const syntheticEvent = createSyntheticEvent(e, element);
  const delay = e.type === 'click' ? 50 : 250;

  const timer = setTimeout(() => {
    sendEventAjax(syntheticEvent);
    debounceTimers.delete(eventKey);
  }, delay);

  debounceTimers.set(eventKey, timer);
}

window.eventHandler = eventHandler;








//async function eventHandler(e) {
//  // prevent default if needed
//  // e.preventDefault();
//  const el = event.currentTarget;
//  console.log("Current Target ID:", el.id);
//  e.stopPropagation();
//  await sendEventAjax(e);
//}



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
