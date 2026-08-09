import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The viewer is intentionally standalone: it reads everything it needs from /public at runtime, so
// the same build can serve any source-governed GLB by swapping model.config.json. Asset URLs in the
// config are document-relative, so one build works co-served under a district site or on its own.
export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    port: 5174,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
