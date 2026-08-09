import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The viewer is intentionally standalone: it reads everything it needs from /public at runtime, so
// the same build can serve any source-governed GLB by swapping model.config.json. Asset URLs in the
// config are document-relative, so one build works co-served under a district site or on its own.
export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    // 5173 is the Manhattan Bridge viewer and 5174 the Brooklyn Bridge viewer. These repos sit
    // side by side and get run together, so each bridge owns its own port and strictPort makes a
    // collision fail loudly rather than silently serving a different bridge on the URL you expect.
    port: 5175,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
