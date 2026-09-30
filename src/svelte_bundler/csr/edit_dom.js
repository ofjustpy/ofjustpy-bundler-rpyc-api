// Applies TDL change history (JSON) directly to the DOM.
//
//   [{"type": "CreateNodeChange", "node_id": "/po_89"},
//    {"type": "AppendChildChange", "node_id": "/po_89", "parent_id": "/po_78", "index": 1}]

export class DomEditApplier {
  /**
   * @param {ParentNode} container  where to look up pre-existing elements (e.g. the root
   *                                div, whose id is your TDL root_id). Defaults to document.
   */
  constructor(container = document) {
    this.container = container;
    // Created-but-not-yet-attached divs live here so parents/children can be
    // resolved before they are in the document.
    this.elements = new Map();
  }

  /** Find an element by id: our own map first, then anything already in the DOM. */
  get(id) {
    if (this.elements.has(id)) return this.elements.get(id);
    // getElementById takes ids like "/po_89" as-is; no CSS escaping needed.
    const el = (this.container.getElementById?.(id)) ??
      document.getElementById(id);
    if (el) this.elements.set(id, el);
    return el ?? null;
  }

  /** Apply an array of changes, in order. Safe to call repeatedly with new batches. */
  apply(changes) {
    for (const change of changes) {
      const handler = this.handlers[change.type];
      if (handler) handler.call(this, change);
      else console.warn(`Unhandled change type: ${change.type}`);
    }
  }

  // Add a method here for each new change type.
  handlers = {
      CreateNodeChange({ node_id }) {
      if (this.get(node_id)) {
        console.warn(`Node ${node_id} already exists; skipping create`);
        return;
      }
	  const el = document.createElement('div');
	  el.id = node_id;
	  // Attach event handlers
	  el.addEventListener('mouseleave', (event) => this.eventHandler(event));
	  el.addEventListener('mouseenter', (event) => this.eventHandler(event));
	  el.addEventListener('click', (event) => this.eventHandler(event));
	  this.elements.set(node_id, el);
    },

    AppendChildChange({ node_id, parent_id, index }) {
      const el = this.get(node_id);
      const parent = this.get(parent_id);
      if (!el || !parent) {
        console.warn(`Cannot append ${node_id} to ${parent_id}: element not found`);
        return;
      }
      if (el === parent || el.contains(parent)) {
        console.warn(`Skipping ${node_id} -> ${parent_id}: would create a cycle`);
        return;
      }

      // Detach first so `index` counts the parent's *remaining* children
      // (this also makes moving within the same parent behave predictably).
      el.remove();

      const at = index == null
        ? parent.children.length
        : Math.max(0, Math.min(index, parent.children.length));

      // insertBefore(x, null) appends, so this covers index == length too.
      parent.insertBefore(el, parent.children[at] ?? null);
    },
  };
}
