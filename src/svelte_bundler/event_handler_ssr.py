# ajax_event_handling = """
# // --- AJAX sender function ---
# function sendEventAjax(e) {
#   const data = {
#     event_data: {
#      event_type: e.type,
#       page_id : page_id,
#       data: event.data,
#       id: e.target?.id || null,
#       tag: e.target?.tagName || null,
#       value: e.target?.value || null,
#       text: e.target?.innerText || null
#     },
#     csrftoken: 'someothervalue'
#   };

#   fetch("/notify-event", {
#     method: "POST",
#     headers: {
#       "Content-Type": "application/json",
#       "X-CSRFToken": data.csrftoken
#     },
#     body: JSON.stringify(data),
#     keepalive: true
#   }).catch(err => {
#     console.warn("Initial AJAX send failed, retrying...", err);
#     setTimeout(() => {
#       fetch("/notify-event", {
#         method: "POST",
#         headers: {
#           "Content-Type": "application/json",
#           "X-CSRFToken": data.csrftoken
#         },
#         body: JSON.stringify(data),
#         keepalive: true
#       }).catch(err => console.error("Retry failed", err));
#     }, 1000);
#   });
# }

# // --- Generic global handler called from HTML ---
# function eventHandler(e) {
#   // prevent default if needed
#   // e.preventDefault();
#   sendEventAjax(e);
# }


# // --- Expose eventHandler globally for inline HTML calls ---
# window.eventHandler = eventHandler;
# """



ajax_event_handling="""
function applyDiffPatch(diff_patch_json) {
  try {
    const diffPatch = JSON.parse(diff_patch_json);

    if (diffPatch.type !== "diff_patch_update" || !diffPatch.data) {
      console.warn("Invalid diff_patch format");
      return;
    }

    const updates = diffPatch.data;

    for (const [elementId, details] of Object.entries(updates)) {
      const el = document.getElementById(elementId);
      if (!el) {
        console.warn(`Element with id '${elementId}' not found`);
        continue;
      }

      const domDict = details.domDict || {};

      // update classes
      if (domDict.hasOwnProperty('/classes')) {
        el.className = domDict["/classes"].trim();
        console.log(`Updated classes for ${elementId}:`, el.className);
      }

      // extend this section for future props like text, style, etc.
    }

  } catch (err) {
    console.error("Error applying diff_patch:", err);
  }
}


async function sendEventAjax(e) {
    const data = {
    event_data: {
     event_type: e.type,
      page_id : page_id,
      data: e.data,
      id: e.target?.id || null,
      tag: e.target?.tagName || null,
      value: e.target?.value || null,
      text: e.target?.innerText || null
    },
    csrftoken: 'someothervalue'
  };

  async function handleResponse(resp) {
    if (!resp.ok) throw new Error(`HTTP error ${resp.status}`);
    const result = await resp.json();
    console.log("✅ Server response:", result);
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
  await sendEventAjax(e);
}


// --- Expose eventHandler globally for inline HTML calls ---
window.eventHandler = eventHandler;
"""
