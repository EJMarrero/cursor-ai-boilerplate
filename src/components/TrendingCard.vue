<template>
  <div class="bg-white shadow rounded p-4" data-cy="trending-card">
    <h2 class="text-xl font-semibold mb-2">Trending Topic</h2>
    <p class="mb-2"><strong>Topic:</strong> {{ trending.topic }}</p>
    <p class="mb-2">
      <strong>URL:</strong>
      <a :href="trending.url" target="_blank" rel="noopener noreferrer" class="text-blue-600 underline">
        {{ trending.url }}
      </a>
    </p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  trending: {
    type: Object,
    required: true,
  }
})
</script>

<style scoped>
/* Estilos adicionales para TrendingCard si son necesarios */
</style> 