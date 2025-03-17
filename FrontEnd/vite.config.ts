import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import path from 'path';
export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Asegúrate de que 'src' sea la carpeta correcta
    },
  },
})