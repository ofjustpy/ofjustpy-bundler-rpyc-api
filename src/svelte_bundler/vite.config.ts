import { defineConfig } from 'vite'
import tailwindcss from "@tailwindcss/vite";

import path from "path";

// https://vite.dev/config/
export default defineConfig({

  plugins: [ tailwindcss(),
  ],
  resolve: {
    alias: {
      $lib: path.resolve("./src/lib"),
    },
  },
    build: { 
	   sourcemap: true,
    lib: {
      entry: 'src/main.ts', // Specify the entry file for the bundle
      name: 'jpComponentBuilder', // Specify the global variable name for the bundle
      formats:['iife'],
      fileName: 'bundle', // Specify the name of the bundle file
    },
    rollupOptions: {
      output: {
      },
    },
  },
})