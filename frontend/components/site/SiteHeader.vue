<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'
import { computed } from 'vue';
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)

onMounted(() => {
  const onScroll = () => (scrolled.value = window.scrollY > 50)
  window.addEventListener('scroll', onScroll)
  onUnmounted(() => window.removeEventListener('scroll', onScroll))
})
</script>

<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4 transition-all',
      scrolled
        ? 'bg-white/60 backdrop-blur-md text-gray-900 shadow-sm'
        : 'bg-transparent text-black'
    ]">
    <NuxtLink to="/" class="font-extrabold text-xl tracking-tight">INTERIOR&nbsp;CO.</NuxtLink>
    <NuxtLink to="/site/contact" class="text-sm font-medium hover:opacity-80">CONTACT&nbsp;US</NuxtLink>
  </header>
</template>


