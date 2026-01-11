import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Proxy /api to the local backend during development to avoid CORS and use same relative paths.
    // Uses VITE_API_URL if available (falls back to http://127.0.0.1:8000).
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
    },
  },
})
