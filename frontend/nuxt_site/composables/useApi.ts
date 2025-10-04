// composables/useApi.ts
// import { $fetch, type FetchOptions } from 'ofetch'          // Nuxt 内置 ofetch            // ✅ 正确的 Nuxt 3 导入

// type J = 'json'
// type Opts = FetchOptions<J>

// /** 简单的 URL join，避免出现 // 或漏 / */
// function joinURL(base = '', path = '') {
//   if (!base) return path
//   if (!path) return base
//   const b = base.endsWith('/') ? base.slice(0, -1) : base
//   const p = path.startsWith('/') ? path : `/${path}`
//   return `${b}${p}`
// }

// /**
//  * 统一封装 API 调用。
//  * 自动读取 nuxt.config.ts -> runtimeConfig.public.apiBase
//  * 例如：const { get, post } = useApi(); await get('/users')
//  */
// export const useApi = () => {
//   const { public: pub } = useRuntimeConfig()
//   const base = pub?.apiBase || ''   // 允许为空（例如同域 / 反向代理）

//   /**
//    * GET
//    */
//   const get = async <T = any>(path: string, options: Opts = {}) => {
//     return await $fetch<T>(joinURL(base, path), {
//       method: 'GET',
//       ...options,
//     })
//   }

//   /**
//    * POST（自动加 content-type）
//    */
//   const post = async <T = any>(path: string, body?: any, options: Opts = {}) => {
//     return await $fetch<T>(joinURL(base, path), {
//       method: 'POST',
//       body,
//       headers: {
//         'content-type': 'application/json',
//         ...(options.headers || {}),
//       },
//       ...options,
//     })
//   }

//   /**
//    * PUT
//    */
//   const put = async <T = any>(path: string, body?: any, options: Opts = {}) => {
//     return await $fetch<T>(joinURL(base, path), {
//       method: 'PUT',
//       body,
//       headers: {
//         'content-type': 'application/json',
//         ...(options.headers || {}),
//       },
//       ...options,
//     })
//   }

//   /**
//    * DELETE
//    */
//   const del = async <T = any>(path: string, options: Opts = {}) => {
//     return await $fetch<T>(joinURL(base, path), {
//       method: 'DELETE',
//       ...options,
//     })
//   }

//   return { get, post, put, del }
// }
// function useRuntimeConfig(): { public: any } {
//     throw new Error('Function not implemented.')
// }

