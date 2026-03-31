"""
DOM Inspection Utilities
"""
import json

def get_dom_snapshot_script(selector: str = "body", depth: int = 3) -> str:
    """
    Generates a JS script to extract a simplified DOM tree.
    This runs inside the browser context.
    """
    # We use a recursive function in JS to traverse the DOM
    # and build a JSON-serializable structure.
    return f"""
    (function() {{
        const root = document.querySelector('{selector}');
        if (!root) return 'Element not found';

        function serialize(node, currentDepth) {{
            if (currentDepth > {depth}) return {{ type: 'text', content: '...' }};

            if (node.nodeType === Node.TEXT_NODE) {{
                const text = node.textContent.trim();
                return text ? {{ type: 'text', content: text }} : null;
            }}

            if (node.nodeType !== Node.ELEMENT_NODE) return null;

            // Skip script and style tags
            const tagName = node.tagName.toLowerCase();
            if (tagName === 'script' || tagName === 'style' || tagName === 'svg') {{
                return null;
            }}

            const el = {{
                tag: tagName,
                id: node.id || undefined,
                classes: node.className ? node.className.split(' ').filter(c => c) : undefined,
                children: []
            }};

            // Important attributes
            ['href', 'src', 'data-type', 'aria-label', 'role'].forEach(attr => {{
                if (node.hasAttribute(attr)) {{
                    el[attr] = node.getAttribute(attr);
                }}
            }});

            for (let i = 0; i < node.childNodes.length; i++) {{
                const child = serialize(node.childNodes[i], currentDepth + 1);
                if (child) el.children.push(child);
            }}

            // Collapse empty containers to reduce noise?
            // For now, keep them structure is important.

            return el;
        }}

        return JSON.stringify(serialize(root, 0));
    }})()
    """
