if (details.attrs) {
        for (const [attrPath, value] of Object.entries(details.attrs)) {
          // Remove leading slash from attribute name (e.g., "/disabled" -> "disabled")
          const attrName = attrPath.startsWith('/') ? attrPath.substring(1) : attrPath;
          
          if (value === "False" || value === false) {
            el.removeAttribute(attrName);
          } else {
            // Set attribute (works for "True", strings, or numbers)
            el.setAttribute(attrName, value === "True" ? "" : value);
          }
          console.log(`Updated attr '${attrName}' for ${elementId} to:`, value);
        }
      }
