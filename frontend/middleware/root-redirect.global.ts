export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/contact') return navigateTo('/site/contact')
})
