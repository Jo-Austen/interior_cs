<script setup>
import { ref, onMounted } from 'vue'
const posts = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/api/v1/posts')
    if (!res.ok) throw new Error('failed')
    posts.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section>
    <h2>最新文章</h2>
    <div v-if="loading">加载中…</div>
    <div v-else-if="error">出错了：{{ error }}</div>
    <ul v-else>
      <li v-for="p in posts" :key="p.slug">
        <strong>{{ p.title }}</strong>
        <div style="color:#666">{{ p.summary }}</div>
        <small v-if="p.published_at">发布于：{{ new Date(p.published_at).toLocaleString() }}</small>
      </li>
    </ul>
  </section>
</template>
