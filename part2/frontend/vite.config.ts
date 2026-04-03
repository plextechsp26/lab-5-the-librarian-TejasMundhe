import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const flask = 'http://127.0.0.1:5000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/books': { target: flask, changeOrigin: true },
      '/members': { target: flask, changeOrigin: true },
      '/borrow': { target: flask, changeOrigin: true },
      '/return': { target: flask, changeOrigin: true },
      '/ping': { target: flask, changeOrigin: true },
    },
  },
});
