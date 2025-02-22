<template>
  <div class="bg-white shadow rounded p-4" data-cy="review-card">
    <h2 class="text-xl font-semibold mb-2">Opinión</h2>
    <p class="mb-2">{{ opinion.opinion_limpia }}</p>
    <div class="border-t pt-2">
      <p><strong>Sentimiento:</strong> {{ opinion.sentimiento }}</p>
      <!-- <p>
        <strong>Temas:</strong>
        
        {{ opinion.temas ? opinion.temas.join(', ') : 'N/A' }}
      </p>
      <p><strong>Categoría:</strong> {{ opinion.categoria }}</p> -->
    </div>
  </div>
</template>

<script setup>
// Se define la propiedad 'opinion' que contendrá la reseña y su análisis
import { defineProps } from 'vue'

const props = defineProps({
  opinion: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
/* Puedes agregar estilos personalizados aquí */
</style> 