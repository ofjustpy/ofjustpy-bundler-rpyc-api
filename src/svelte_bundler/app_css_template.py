from string import Template

# layerchart_theme_import_stmt = """
# @import '@layerstack/tailwind/core.css';
# /* 3. All Skeleton themes ported to LayerStack */
# @import '@layerstack/tailwind/themes/skeleton.css';
# """
layerchart_theme_import_stmt = ""


app_css_template = Template("""
@import "tailwindcss";

@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

$layerchart_theme_import_stmt

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.129 0.042 264.695);
  --card: oklch(0.95 0.05 240); /* A light blue */
  --card-foreground: oklch(0.2 0.07 240); /* A darker blue for text */
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.129 0.042 264.695);
  --primary: oklch(0.208 0.042 265.755);
  --primary-foreground: oklch(0.984 0.003 247.858);
  --secondary: oklch(0.968 0.007 247.896);
  --secondary-foreground: oklch(0.208 0.042 265.755);
  --muted: oklch(0.968 0.007 247.896);
  --muted-foreground: oklch(0.554 0.046 257.417);
  --accent: oklch(0.968 0.007 247.896);
  --accent-foreground: oklch(0.208 0.042 265.755);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.929 0.013 255.508);
  --input: oklch(0.929 0.013 255.508);
  --ring: oklch(0.704 0.04 256.788);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.984 0.003 247.858);
  --sidebar-foreground: oklch(0.129 0.042 264.695);
  --sidebar-primary: oklch(0.208 0.042 265.755);
  --sidebar-primary-foreground: oklch(0.984 0.003 247.858);
  --sidebar-accent: oklch(0.968 0.007 247.896);
  --sidebar-accent-foreground: oklch(0.208 0.042 265.755);
  --sidebar-border: oklch(0.929 0.013 255.508);
  --sidebar-ring: oklch(0.704 0.04 256.788);
}

.dark {
  --background: oklch(0.129 0.042 264.695);
  --foreground: oklch(0.984 0.003 247.858);
  --card: oklch(0.208 0.042 265.755);
  --card-foreground: oklch(0.984 0.003 247.858);
  --popover: oklch(0.208 0.042 265.755);
  --popover-foreground: oklch(0.984 0.003 247.858);
  --primary: oklch(0.929 0.013 255.508);
  --primary-foreground: oklch(0.208 0.042 265.755);
  --secondary: oklch(0.279 0.041 260.031);
  --secondary-foreground: oklch(0.984 0.003 247.858);
  --muted: oklch(0.279 0.041 260.031);
  --muted-foreground: oklch(0.704 0.04 256.788);
  --accent: oklch(0.279 0.041 260.031);
  --accent-foreground: oklch(0.984 0.003 247.858);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.551 0.027 264.364);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.208 0.042 265.755);
  --sidebar-foreground: oklch(0.984 0.003 247.858);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.984 0.003 247.858);
  --sidebar-accent: oklch(0.279 0.041 260.031);
  --sidebar-accent-foreground: oklch(0.984 0.003 247.858);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.551 0.027 264.364);
}

@theme inline {
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
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
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""

)
from .helper_utils import write_to_bundler_dir
def build_app_css():
    app_css_template = Template("""@import "tailwindcss";""")
    app_css_str = """
@import "tailwindcss";
    @plugin "@tailwindcss/typography";
    @import '@skeletonlabs/skeleton';
@import '@skeletonlabs/skeleton/optional/presets';
@import '@skeletonlabs/skeleton/themes/cerberus';
@import '@skeletonlabs/skeleton/themes/seafoam';    


@source '../node_modules/@skeletonlabs/skeleton-svelte/dist';
@source "safelist.txt";    

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
    write_to_bundler_dir(app_css_str, "src/app.css")



   

        
