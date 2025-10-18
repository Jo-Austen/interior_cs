import { defineNuxtConfig } from 'nuxt/config'
import path from 'node:path' // 导入 path 模块
import process from 'node:process'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  modules: ['@nuxt/ui', '@nuxt/icon'],
  css: [
    path.join(process.cwd(), 'assets/css/main.css') 
  ],
  // Tailwind v4 要这个 PostCSS 插件（不再使用 @nuxtjs/tailwindcss 模块）, 使用相对路径获取有问题，以上改为绝对路径
  postcss: { plugins: { '@tailwindcss/postcss': {} } },
  devtools: { enabled: true }
})

